from django.views.generic import TemplateView 
from django.views.decorators.cache import never_cache
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Message, MessageSerializer

import json
import speech_recognition as sr
r = sr.Recognizer()

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    #queryset = Message.objects.all()
    #serializer_class = MessageSerializer

class UploadView(APIView):

    def post(self, request):
        forms = request.POST
        audio = request.FILES['file'].read() 
        # if want write 
        # from django.core.files.storage import default_storage
        # with default_storage.open('tmp/hehe.wav', 'wb+') as destination:
        #     destination.write(audio)
        audio = sr.AudioData(audio, 16000, 2)
        result = r.recognize_google(audio,language='zh-tw')
        return Response({"result":result}) 

class AnswerView(APIView):

    def post(self, request):
        data = json.loads(request.body)
        context_text = data["context_text"]
        question_text = data["question_text"]
        choices_text = data["choices_text"]
        result = "%s %s %s "%(context_text,question_text,choices_text)
        return Response({"result":result}) 
