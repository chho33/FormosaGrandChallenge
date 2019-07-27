from django.views.generic import TemplateView 
from django.views.decorators.cache import never_cache
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Message, MessageSerializer

#from ailabs_asr import KgbAsrDecoder
#from asr_settings import asr_base_dir

import shutil
import os
from time import sleep
import pathlib
import json
import redis
import speech_recognition as sr
recog = sr.Recognizer()

# redis
redis_host = "localhost"
redis_port = 6379
redis_db = 0

# wav types
wav_files = ["context.wav","question.wav","choices.wav"]

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

# Set asr decoder
#decoder_dir = pathlib.PurePosixPath(asr_base_dir).joinpath('ailabs_asr/nnet3_adapt')
#decoder = KgbAsrDecoder(decoder_dir=decoder_dir)

def asr_passage(passage_path):
    passage = decoder.decode(passage_path,False)
    return passage

def asr_question_choices(passage, question_path, choices_path):
    fd, new_fst = decoder.make_adapt_fst(passage)
    if new_fst is None:
        question = decoder.decode(question_path, False)
        choices = decoder.decode(choices_path, True)
    else:
        question = decoder.decode(question_path, False, new_fst)
        choices = decoder.decode(choices_path, True, new_fst)
        os.close(fd)
        os.remove(new_fst)
    return question, choices

def asr_passage(passage_path):
    with sr.AudioFile(passage_path) as source:
        speech = recog.record(source)
        #speech = sr.AudioData(speech, 16000, 2)
        result = recog.recognize_google(speech,language='zh-tw')
    return result 

def asr_question_choices(passage, question_path, choices_path):
    with sr.AudioFile(question_path) as source:
        speech = recog.record(source)
        #speech = sr.AudioData(speech, 16000, 2)
        q_result = recog.recognize_google(speech,language='zh-tw')
    with sr.AudioFile(choices_path) as source:
        speech = recog.record(source)
        #speech = sr.AudioData(speech, 16000, 2)
        c_result = recog.recognize_google(speech,language='zh-tw')
    return q_result, c_result

def check_audios_rd(rd,key,audio):
    if rd.exists(key):
        rd.lpush(key,audio)
        data = rd.lrange(key,0,2)
        if len(data) == 3:
            # do asr 
            result = ''
            rd.delete(key)
            return result 
    else:
        rd.lpush(key,audio)

def check_audios(wav_dir):
    if_finish = True
    for wav in wav_files: 
        wav_file = pathlib.Path(wav_dir) / wav
        if_finish *= wav_file.exists()
    context_txt = pathlib.Path(wav_dir) / "context.txt"
    if_finish *= context_txt.exists()
    return if_finish

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    #queryset = Message.objects.all()
    #serializer_class = MessageSerializer

class UploadView(APIView):

    def post(self, request):
        forms = request.POST
        file_type = forms["fileType"] 
        key = forms["key"] 
        #rd = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        audio = request.FILES['file'].read() 

        # step1: save wav 
        wav_dir = pathlib.PurePosixPath('tmp').joinpath(key)
        pathlib.Path(wav_dir).mkdir(parents=True,exist_ok=True)    
        wav_file = '%s/%s.wav'%(wav_dir,file_type)
        with default_storage.open(wav_file, 'wb+') as destination:
            destination.write(audio)

        # step2: asr, save text, return text 
        if file_type == "context":
            result = asr_passage(wav_file)
            with open("%s/%s.txt"%(wav_dir,"context"), "w") as f:
                f.write(result)
            #audio = sr.AudioData(audio, 16000, 2)
            #result = recog.recognize_google(audio,language='zh-tw')
            return Response([{"fileType":file_type,"result":result}]) 
        elif file_type == "question":
            return Response(0) 
        elif file_type == "choices":
            waiting = 0
            while not check_audios(wav_dir):
                if waiting >= 300:
                    raise TimeoutError 
                sleep(0.5) 
                waiting += 0.5
            with open("%s/%s.txt"%(wav_dir,"context"), "r") as f:
                passage = f.read().strip()
            question_wav_file = '%s/%s.wav'%(wav_dir,"question")
            q_result, c_result = asr_question_choices(passage, question_wav_file, wav_file)
            shutil.rmtree(wav_dir)
            return Response([{"fileType":"question","result":q_result},
                             {"fileType":"choices", "result":c_result},
            ]) 

class AnswerView(APIView):

    def post(self, request):
        data = json.loads(request.body)
        context_text = data["context_text"]
        question_text = data["question_text"]
        choices_text = data["choices_text"]
        result = "%s %s %s "%(context_text,question_text,choices_text)
        return Response({"result":result}) 
