from django.views.generic import TemplateView 
from django.views.decorators.cache import never_cache
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Message, MessageSerializer

import json
import redis
import speech_recognition as sr
r = sr.Recognizer()

# redis
redis_host = "localhost"
redis_port = 6379
redis_db = 0

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

def check_audios(rd,key,audio):
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

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    #queryset = Message.objects.all()
    #serializer_class = MessageSerializer

class UploadView(APIView):

    def post(self, request):
        forms = request.POST
        key = forms["fileType"] 
        rd = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        audio = request.FILES['file'].read() 
        # if want write 
        # from django.core.files.storage import default_storage
        # with default_storage.open('tmp/hehe.wav', 'wb+') as destination:
        #     destination.write(audio)
        audio = sr.AudioData(audio, 16000, 2)
        result = check_audios(rd,key,audio)
        result = r.recognize_google(audio,language='zh-tw')
        return Response([{"fileType":key,"result":result}]) 

class AnswerView(APIView):

    def post(self, request):
        data = json.loads(request.body)
        context_text = data["context_text"]
        question_text = data["question_text"]
        choices_text = data["choices_text"]
        result = "%s %s %s "%(context_text,question_text,choices_text)
        return Response({"result":result}) 
