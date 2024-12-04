# run.py

import os
import asyncio
from django.core.management import execute_from_command_line
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# Функция для запуска Django
def run_django():
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

# Функция для запуска бота
async def on_startup(dp):
    print("Бот запущен!")

async def on_message(message: types.Message):
    await message.reply("Привет!")

async def run_bot():
    bot = Bot(token='YOUR_BOT_TOKEN')
    dp = Dispatcher(bot)

    dp.register_message_handler(on_message)

    await executor.start_polling(dp, on_startup=on_startup)

# Запуск в asyncio
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, run_django)
    loop.run_until_complete(run_bot())
