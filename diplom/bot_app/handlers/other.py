
import logging
import string
import json
from aiogram import  Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# и импорт из файлов
from bot_app import text


# Создание базового логирования
logging.basicConfig(filename='errors.log', level=logging.INFO)


router_other = Router()


#----------------OTHER------------------------

# хендлер, который удаляет плохие слова
@router_other.message() # пустой хендлер в конец!!!
async def echo_send(message: Message, state: FSMContext):
    await state.clear()
    logging.info('Сработал ценз')
    # генератор множества    
    with open('cenz/cenz.json', 'r') as file:
            bad_words = set(json.load(file))

    # Генератор множества
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(bad_words) != set():
        await message.reply('Не ругайся 💔')
        await message.delete()
    else:
        await message.answer('Извините, я не понимаю это сообщение.' + text.help)



# в конце, ответ на любое несистемное сообщение
@router_other.message() 
async def all_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('👩 Если у вас остались вопросы, напишите мне @clevereej')
    

#----------------END-OTHER------------------------