
import logging
import os
import requests
import string
import json
from aiogram import  Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asgiref.sync import sync_to_async
# и импорт из файлов
from sign_in.models import CustomUser
import bot_app.keyboards as kb
from bot_app import text
from bot_app.config import ADMIN





router_client = Router()

host = 'http://127.0.0.1:8000/bot/'

#-----------------CLIENT--------------------

# вызываем появление приветственной клавиатуры при открытии бота при команде /start
@router_client.message(CommandStart())
async def start(message: Message):
    # добавляем клиента в базу данных
    telegram_user, created = await CustomUser.objects.aget_or_create(id=message.from_user.id, username=message.from_user.username)
    await sync_to_async(telegram_user.get_user)()
    welcome_message = f"Добро пожаловать, {message.from_user.username}! ❤️ " + text.start
    await message.answer(welcome_message)

    if created:
        logging.info("New user created")
    else:
        logging.info("User already exists")
    await message.answer(reply_markup=kb.ik_button_info_store())  
    
    
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")
    
# команда help
@router_client.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "Это бот, который поможет вам с различными задачами. Вот некоторые команды, которые вы можете использовать:\n"
        "/start - начать работу с ботом\n"
        "/help - получить помощь\n"
        "/info - получить информацию о боте\n"
        "/profile - посмотреть ваш профиль\n"
        # Добавьте другие необходимые команды
    )
    await message.answer(help_text)
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")

# Command to show user profile
@router_client.message(Command("profile"))
async def profile_command(message: Message):
    from sign_in.models import CustomUser
    telegram_user = await CustomUser.objects.aget(chat_id=message.from_user.id)
    profile_info = (
        f"Ваш профиль:\n"
        f"Имя: {telegram_user.username}\n"
        f"ID Чата: {telegram_user.chat_id}\n"
        # Добавьте другие поля, если есть
    )
    await message.answer(profile_info)

# Displays information about the bot
@router_client.message(Command("info"))
async def info_command(message: Message):
    info_text = "Этот бот предназначен для помощи пользователям в различных задачах."
    await message.answer(info_text)

# прописываем простые фильтры
@router_client.message(F.text == 'Привет') 
async def hello(message: Message):
    await message.answer('👩 И тебе привет')
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")

@router_client.message(F.text == 'Как дела?') 
async def how_a_u(message: Message):
    await message.answer('👩 Рада, что тебя заинтересовал мой космический магазин')
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")

@router_client.message(F.text == 'Пока') 
async def bay(message: Message):
    await message.answer('Скучаю 💔')
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")

@router_client.message(F.text == ' ') 
async def none(message: Message):
    await message.answer('🚀')
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")
    
    
# обработчик кнопки информация об магазине
@router_client.message(F.text == 'Информация о магазине')
async def store_info(message: Message):
    await message.answer(text.info, reply_markup = kb.ik_button_info_store)
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")

# обработчик кнопки информация о магазине
# если нажать часы работы
@router_client.message(F.data == 'grafik')
async def grafik(message: Message):
    await message.answer(text.grafik_info, reply_markup = kb.ik_button_info_store)
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")

# обработчик кнопки информация о магазине
# если нажать адрес
@router_client.message(F.data == 'adress')
async def adress(message: Message):
    await message.answer(text.adress_info, reply_markup = kb.ik_button_info_store)
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")

# обработчик кнопки информация о магазине
# если нажать доставка
@router_client.message(F.data == 'delivery')
async def delivery(message: Message):
    await message.answer(text.delivery_info, reply_markup = kb.ik_button_info_store)
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")









# обработчик кнопки Связь с оператором
@router_client.message(F.text == 'Связь с оператором')
async def connect(message: Message):
    await message.answer(f"Уважаемый, {message.from_user.username}! Оператор подключится в ближайшее время! ")
    await message.answer()
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")



# обработчик кнопки Каталог товаров
@router_client.message(F.text == 'Каталог товаров')
async def show_items(message: Message):
    try:
        # Отправляем запрос на получение инлайн-клавиатуры
        inline_keyboard = await kb.inline_store()
        await message.answer(reply_markup=inline_keyboard)

        # Отправка данных на Django API
        response = requests.post(host, json={'user_id': message.from_user.id})
        if response.status_code == 200:
            await message.reply("Данные успешно отправлены на сервер.")
        else:
            await message.reply("Ошибка при отправке данных.")
    except Exception as e:
        logging.error(f"Error in show_items: {e}")  # Логируем ошибку
        await message.reply("Произошла ошибка при загрузке каталога. Пожалуйста, попробуйте позже.")


    

# обработчик кнопки ТОВАР
# сделать так, чтобы после срабатывания инлайн клавиатуры, в ней появлялась другая инлайн клавиатура
@router_client.callback_query(F.data == f'choose_Spacestore.title') 
async def product(call: CallbackQuery, state: FSMContext):
    try:
        # Изменяем текст сообщения и показываем новую инлайн-клавиатуру
        await call.message.edit_text(reply_markup=await kb.ik_button_catalog())
        
        # Отправка данных на Django API
        response = requests.post(host, json={'user_id': call.from_user.id})
        if response.status_code == 200:
            await call.reply("Данные успешно отправлены на сервер.")
        else:
            await call.reply("Ошибка при отправке данных.")
    except Exception as e:
        logging.error(f"Error in product callback: {e}")  # Логируем ошибку
        await call.reply("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.")







        
# обработчик кнопки Каталог товаров
# если нажать Подробное описание
@router_client.message(F.data == 'description')
async def description(call: CallbackQuery, state: FSMContext):
    from spacestore.models import Spacestore
    await call.answer(Spacestore.object.description) 
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': call.from_user.id})
    if response.status_code == 200:
        await call.reply("Данные успешно отправлены на сервер.")
    else:
        await call.reply("Ошибка при отправке данных.")








# обработчик кнопки Каталог товаров
# если нажать Купить

class Reg(StatesGroup):
    name = State()
    adress = State()
    pay = State()
    phone_number = State()


@router_client.message(F.data == 'buy')
async def buy(message: types.Message, state: FSMContext):
    await message.answer('Заполните небольшую форму для покупки товара: ') 
    await message.answer('Введите Ваше имя:') 
    await state.set_state(Reg.name)

# Ловит, сохраняет имя и спрашивает адрес
@router_client.message(Reg.name)
async def reg_2(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer('Напишите адресс доставки, включая город и индекс:')
    await state.set_state(Reg.adress)

# Сохраняет адрес и спрашивает способ оплаты
@router_client.message(Reg.adress)
async def reg_3(message: types.Message, state: FSMContext):
    adress = message.text 
    await state.update_data(adress=adress)
    await message.answer('Каким способом вам будет удобно платить? Можно оплатить товар при получении наличными или картой курьеру.', reply_markup = kb.payment_options())
    await state.set_state(Reg.pay) # добавить сюда клавиатуру с двумя кнопками ответа

# Сохраняет способ оплаты и спрашивает номер телефона
@router_client.message(Reg.pay)
async def reg_4(message: types.Message, state: FSMContext):  
    pay = message.text
    await state.update_data(pay=pay)
    await message.answer('Напишите свой номер для связи.начиная с +: ')
    await state.set_state(Reg.phone_number)
    
# Сохраняет номер телефона и создает блок данных
@router_client.message(Reg.phone_number)
async def reg_7(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not phone_number.startswith("+"):
        phone_number = phone_number
    await state.update_data(phone_number=phone_number)

    # Получаем данные пользователя 
    data = await state.get_data()
    name = data.get('name')
    adress = data.get('adress')
    pay = data.get('pay')
    phone_number = data.get('phone_number')
    
    # Формируем читаемое сообщение 
    order_info = (
        f"Оформлен заказ от {message.from_user.username} - {name}, на {product} .\n"
        f"Данные:\n"
        f"- Адрес: {adress}\n"
        f"- Способ оплаты: {pay}\n"
        f"- Номер: {phone_number}\n"
        f"Для вызова меню напишите /start"
    )
    # отправляем сообщение клиенту
    await message.answer(order_info)
    await message.answer('Спасибо за ваш заказ! Мы свяжемся с вами в ближайшее время.')
    
    # отправляем сообщение администратору 
    #await bot.send_message(ADMIN, f"Новое сообщение: {order_info}")
  
    # Отправка данных на Django API
    response = requests.post(host, json={'user_id': message.from_user.id})
    if response.status_code == 200:
        await message.reply("Данные успешно отправлены на сервер.")
    else:
        await message.reply("Ошибка при отправке данных.")

    # Завершаем состояние
    await state.finish()
    # Заканчиваем состояние
    await state.clear()


'''----------------КОНЕЦ ОФОРМЛЕНИЯ ЗАКАЗА-------------'''   
    



#----------------OTHER------------------------

# хендлер, который удаляет плохие слова
@router_client.message() # пустой хендлер в конец!!!
async def echo_send(message: Message):
    # генератор множества
    if {i.lower().translate(str.maketrans('', '', string.punctuation )) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.cenz.json')))) != set():
        await message.reply('Не ругайся 💔')
        await message.delete()
    else:
        await message.answer('Извините, я не понимаю это сообщение.' + text.help) 


#----------------END-OTHER------------------------


# в конце, ответ на любое несистемное сообщение
@router_client.message() 
async def all_message(message: Message):
    await message.answer('👩 Если у вас остались вопросы, напишите мне @clevereej')
    
#-----------------END-CLIENT--------------------
