#-------------Создание телеграм бота на библиотеке AIOGRAM 3--------------

#------------------------------Импортирование-----------------------------
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter
import asyncio
import sys
import os
import io


# Установка пути к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Установите переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')

# Импортируем Django и настраиваем его
import django
django.setup()


# Создание базового логирования
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("errors.log"), logging.StreamHandler()])
# установить кодировку в UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Установка пути к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем конфигурацию
from config import TOKEN_API, ADMIN

# Использовать пользовательский сервер API
#session = AiohttpSession(proxy='http://127.0.0.1:8010/')

'''8010
8080'''

# Инициализация бота
# инициируем объект бота, передавая ему parse_mode=ParseMode.HTML по умолчанию
# Благодаря такой инициации наш бот по умолчанию будет считывать HTML теги с сообщений
bot = Bot(token=TOKEN_API)
'''session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML)'''


storage = MemoryStorage()

# Инициализация диспетчера
dp = Dispatcher(storage=storage)

# Установка хранилища для диспетчера
dp.update.storage = storage

# Импортируем роутеры из других модулей
from bot_app.handlers.client import router_client
from bot_app.handlers.admin import router_admin
from bot_app.handlers.sign_in import router_sign_in
from bot_app.handlers.other import router_other

# Регистрация роутеров
dp.include_router(router_client)
dp.include_router(router_admin)
dp.include_router(router_sign_in)  
dp.include_router(router_other)    






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
        logging.info('запущена функция старта')
        await dp.start_polling(bot)
        logging.info('Бот запущен')
    except Exception as e:
        logging.error(f'Ошибка в основном цикле: {e}')
        await stop_bot()
    '''finally:
        await bot.close()
        await bot.session.close()  # Закрываем сессию
        logging.info('Бот остановлен')  # Закрываем бота
        await storage.close()  # Закрываем хранилище'''


if __name__=='__main__':
    # Запуск в asyncio
    loop = asyncio.get_event_loop()
    logging.info('Запуск асинкио')
    loop.run_until_complete(main())  # Запускаем бота
    logging.info('Запуск бота завершен')
    
    # cd bot_app
    # python run.py


    

