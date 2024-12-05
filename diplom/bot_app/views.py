# views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

# Создание базового логирования
logging.basicConfig(filename='errors.log', level=logging.INFO)
logger = logging.getLogger(__name__)

class BotDataView(APIView):
    def post(self, request):
        data = request.data
        logger.info('Обработка данных от бота')
        
        if 'message' in data:
            response_message = f"Received message: {data['message']}"
            logger.info('Сообщение успешно обработано')
        else:
            logger.warning("No message received in the request data.")
            response_message = "No message received."

        response_data = {
            'status': 'success',
            'response': response_message
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    def get(self, request):
        logger.info('Обработка GET-запросов')
        context = {}
        return render(request, 'bot.html', context)

