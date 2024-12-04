#-------------Создание телеграм бота на библиотеке AIOGRAM 3--------------

#------------------------------Импортирование-----------------------------
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
import sys
import os

# Импортируем Django и инициализируем приложение
import django
from django.core.management import execute_from_command_line
from django.conf import settings
from django.apps import apps
import asyncio
import logging

# Установка пути к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Установка переменной окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')

# Инициализация Django
django.setup()

# Получаем WSGI-приложение
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Импортируем конфигурацию
from config import TOKEN_API, ADMIN

# Создание базового логирования
logging.basicConfig(level=logging.INFO)

# Использовать пользовательский сервер API
session = AiohttpSession(proxy='http://127.0.0.1:8000/')



# Инициализация бота
# инициируем объект бота, передавая ему parse_mode=ParseMode.HTML по умолчанию
# Благодаря такой инициации наш бот по умолчанию будет считывать HTML теги с сообщений
bot = Bot(token=TOKEN_API, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

storage = MemoryStorage()

# Инициализация диспетчера
dp = Dispatcher()

# Установка хранилища для диспетчера
dp.update.storage = storage

# Импортируем роутеры из других модулей
from bot_app.handlers.client import router_client as client_router
from bot_app.handlers.admin import router_admin as admin_router
#from bot_app.handlers.errors import router_errors as errors_router
#from bot_app.handlers.sign_in import router_sign_in as sign_in_router

# Регистрация роутеров
dp.include_router(client_router)
dp.include_router(admin_router)
#dp.include_router(errors_router)
#dp.include_router(sign_in_router)    






# Функция, которая выполнится когда бот запустится
async def start_bot():
    try:
        await bot.send_message(ADMIN, f'Я запущен🥳')
    except Exception as e:
        logging.error(f'Ошибка при отправке сообщения об старте: {e}')

# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    try:
        await bot.send_message(ADMIN, 'Бот остановлен😔')
    except Exception as e:
        logging.error(f'Ошибка при отправке сообщения о завершении: {e}')


# Функция для запуска бота
async def main():
    # Запуск бота
    try:
        await start_bot()
        await dp.start_polling()
    except Exception as e:
        logging.error(f'Ошибка в основном цикле: {e}')
        await stop_bot()
    finally:
        await bot.close()  # Закрываем бота
        await storage.close()  # Закрываем хранилище


# Функция для запуска Django
async def run_django():
    try:
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
    except Exception as e:
        logging.error(f'Ошибка при запуске Django: {e}')

if __name__=='__main__':
    # Запуск в asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(run_django())  # Запускаем Django в фоновом режиме
    loop.run_until_complete(main())  # Запускаем бота
    
    # cd bot_app
    # python run.py


    

