# views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
import logging

# Создание базового логирования
logging.basicConfig(filename='errors.log', level=logging.INFO)
# создает экземпляр логгера для текущего модуля
logger = logging.getLogger(__name__)


# Django REST Framework сериализаторы для валидации входящих данных. Это поможет избежать ошибок и упростит код
class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)

# Наследуется от APIView и обрабатывает POST и GET запросы
class BotDataView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        logger.info('Обработка данных от бота')
        if serializer.is_valid():
            message = serializer.validated_data['message']
            response_message = f"Received message: {message}"
            logger.info('Сообщение успешно обработано')
            return Response({'status': 'success', 'response': response_message}, status=status.HTTP_200_OK)
        else:
            logger.warning("Invalid data received.")

            return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
     
     
    
    def get(self, request):
        logger.info('Обработка GET-запросов')
        context = {}
        return render(request, 'bot.html', context)


