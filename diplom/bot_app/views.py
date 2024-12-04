from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

class BotDataView(APIView):
    def post(self, request):
        # Обработка данных от бота
        data = request.data
        
        # Пример обработки данных
        if 'message' in data:
            response_message = f"Received message: {data['message']}"
        else:
            logger.warning("No message received in the request data.")
            response_message = "No message received."

        # Формируем ответ
        response_data = {
            'status': 'success',
            'response': response_message
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    def get(self, request):
        # Если нужно обработать GET-запросы, можно добавить логику здесь
        context = {}
        return render(request, 'bot.html', context)
