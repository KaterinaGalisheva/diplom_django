'''import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError
from asgiref.sync import sync_to_async

from aiogram import Router, types
from aiogram.dispatcher import FSMContext

from main import dp
from const_texts import *

from robot.models import TelegramUser
from robot.states import UserRegister
from robot.keyboards.default import make_buttons, contact_request_button
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
import re



router_sign_in = Router()

-----------------------------------------------------------------------------------

Инлайн-клавиатура проверки заполнения данных:

def check_data():
    kb_list = [
        [InlineKeyboardButton(text="✅Все верно", callback_data='correct')],
        [InlineKeyboardButton(text="❌Заполнить сначала", callback_data='incorrect')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


    -------------------------------------------------------------------------------------------------





# Функция extract_number извлекает число из текста. Полезно на случай если пользователь вместо "20" будет писать "мне 20 лет". Данная функция достанет 20 и сразу трансформирует это запись в int.
def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None


class Form(StatesGroup):
    username = State()
    email = State()
    password1 = State()
    password2 = State()
    
router_sign_in = Router()!!!!!!!!!!! bcghfdbnm dtplt
@questionnaire_router.message(Command('start_questionnaire'))
async def start_questionnaire_process(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer('Привет. Напиши как тебя зовут: ')
    await state.set_state(Form.username)

    
@questionnaire_router.message(F.text, Form.username)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer('Теперь напиши свой email: ')
    await state.set_state(Form.email)

@questionnaire_router.message(F.text, Form.email)
async def capture_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer('Теперь напиши пароль более 6 символов: ')
    await state.set_state(Form.password1)

    
@questionnaire_router.message(F.text, Form.password1)
async def capture_password1(message: Message, state: FSMContext):
    await state.update_data(password1=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        await message.answer('Повтори пароль: ')
        await state.set_state(Form.password2)


@questionnaire_router.message(F.text, Form.password2)
async def capture_password2(message: Message, state: FSMContext):
    await state.update_data(password2=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        

# проверка данных
@questionnaire_router.message(F.text, Form.about)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(about=message.text)

    data = await state.get_data()

    caption = f'Пожалуйста, проверьте все ли верно: \n\n' \
              f'<b>Полное имя</b>: {data.get("username")}\n' \
              f'<b>email</b>: {data.get("email")}\n' \
              f'<b>password1</b>: {data.get("password1")}\n' \
              f'<b>password2</b>: {data.get("password2")}'

    await message.answer(caption=caption, reply_markup=check_data())
    await state.set_state(Form.check_state)

# сохраняем данные
@questionnaire_router.callback_query(F.data == 'correct', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    # Создание пользователя
            user = CustomUser(username=username, email=email)
            user.set_password(password1)  # Хешируем пароль
            user.save()
    await call.answer('Данные сохранены')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Благодарю за регистрацию. Ваши данные успешно сохранены!')
    await state.clear()


    # запускаем анкету сначала
@questionnaire_router.callback_query(F.data == 'incorrect', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Запускаем сценарий с начала')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Привет. Для начала Укажи свое имя: ')
    await state.set_state(Form.username)





        

------------- ОЧЕНЬ ВАЖНО!!!!!!!!!---------------

Пользователь заполняет анкету, а после передумывает. Нажимает через командное меню /start, а у него ничего не происходит. Дело в том, что сценарий, который мы запустили, не завершился.

Бывает, что происходит. В таком случае вместо имени бот записывает имя «/start», после отправляет новый вопрос «Введи возраст». Пользователь снова жмет /start, и это все идет до момента, пока пользователь не удаляет бота и не считает, что его делали некомпетентные люди.

Чтобы эту проблему избежать, стоит в своей архитектуре закладывать возможность выхода из сценария анкетирования. Лично я всегда закладываю в команде /start и в прочих командах (в их хендлерах) сброс сценария. Для этого необходимо следующее:

async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

В таком случае вы автоматически ставите закрытие сценария анкетирования, и пользователь, нажав на старт, просто получит сброс данных.

Также советую добавлять возможность выхода по клику на кнопку клавиатуры. Это может быть текстовая кнопка с надписью «Отмена» или инлайн-кнопка с call_data = cancel, а далее просто обработчик, который будет закрывать (очищать) хранилище, тем самым выбивая пользователя из сценария.

-------------------------------------------------------------------------------------------

'''























































