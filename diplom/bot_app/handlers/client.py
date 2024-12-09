
import logging
import os
import httpx
from aiogram import  Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from django.conf import settings
# и импорт из файлов
from spacestore.models import get_items_from_db, get_item_description_from_db, get_item_title_from_db
from sign_in.models import CustomUser
from bot_app.models import Notification
import bot_app.keyboards as kb
from bot_app import text
from bot_app.config import ADMIN

# Создание базового логирования
logging.basicConfig(filename='errors.log', level=logging.INFO)


router_client = Router()





#-----------------CLIENT--------------------

# вызываем появление приветственной клавиатуры при открытии бота при команде /start
@router_client.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    logging.info('Сработала команда старт')
    
    # добавляем клиента в базу данных
    '''telegram_user, created = await CustomUser.objects.aget_or_create(
        id=message.from_user.id,
        username=message.from_user.username
    )'''
    telegram_user, created = await Notification.objects.aget_or_create(
        user_id=message.from_user.id
    )
    logging.info('Клиент добавлен в базу данных')
    
    welcome_message = f"Добро пожаловать, {message.from_user.username}! ❤️ " + text.start
    await message.answer(welcome_message)
    logging.info('Отправлено приветственное письмо')

    if created:
        logging.info("Создан новый пользователь")
    else:
        logging.info("Пользователь не создан, так как уже был создан")
    
    await message.answer(text="Выберите пункт меню:", reply_markup=kb.main_menu)  
    
    
# команда help
@router_client.message(Command("help"))
async def help_command(message: Message, state: FSMContext):
    await state.clear()
    logging.info('Сработала команда хелп')
    help_text = (
        "Это бот, который поможет вам. Вот некоторые команды, которые вы можете использовать:\n"
        "/start - начать работу с ботом\n"
        "/help - получить помощь\n"
        "/info - получить информацию о боте\n"
        # Добавьте другие необходимые команды
    )
    await message.answer(help_text)
    logging.info('Отправлен текст хелп')
    


# Displays information about the bot
@router_client.message(Command("info"))
async def info_command(message: Message, state: FSMContext):
    await state.clear()
    logging.info('Сработала команда инфо')
    info_text = "Этот бот предназначен для покупки товаров из космического магазина."
    await message.answer(info_text)
    logging.info('Отправлен текст инфо')

    
# обработчик кнопки информация об магазине
@router_client.message(F.text == 'Информация о магазине')
async def store_info(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text.info, reply_markup = kb.ik_button_info_store)
   

# обработчик кнопки информация о магазине
# если нажать часы работы
@router_client.callback_query(F.data == 'grafik')
async def grafik(callback_query: CallbackQuery):
    message = callback_query.message
    logging.info('Сработала кнопка график')
    await message.answer(text.grafik_info, reply_markup = kb.ik_button_info_store)
  

# обработчик кнопки информация о магазине
# если нажать адрес
@router_client.callback_query(F.data == 'adress')
async def adress(callback_query: CallbackQuery):
    message = callback_query.message
    logging.info('Сработала кнопка адрес')
    await message.answer(text.adress_info, reply_markup = kb.ik_button_info_store)
  

# обработчик кнопки информация о магазине
# если нажать доставка
@router_client.callback_query(F.data == 'delivery')
async def delivery(callback_query: CallbackQuery):
    message = callback_query.message
    logging.info('Сработала кнопка доставки')
    await message.answer(text.delivery_info, reply_markup = kb.ik_button_info_store)
 








# обработчик кнопки Связь с оператором
@router_client.message(F.text == 'Связь с оператором')
async def connect(message: Message, state: FSMContext):
    await state.clear()
    logging.info('Сработала кнопка связь с оператором')
    await message.answer(f"Уважаемый, {message.from_user.username}! Оператор подключится в ближайшее время! ")


# обработчик кнопки Каталог товаров
@router_client.message(F.text == 'Каталог товаров')
async def show_items(message: Message, state: FSMContext):
    await state.clear()
    logging.info('Сработала кнопка покупки товаров')
    
    store = await get_items_from_db()  # Получаем товары из базы данных
    logging.info(f"Полученные товары: {store}") 

    for item in store:
        logging.info(f"Обрабатываем товар: {item.title}, Фото: {item.photo}, Цена: {item.cost}")
        if item.photo and item.title and item.cost is not None:
            # Создаем клавиатуру отдельно
            photo_path = f'{settings.MEDIA_ROOT}/{item.photo}'
            # Проверяем, существует ли файл
            if os.path.exists(photo_path):
                photo_file = FSInputFile(photo_path)
                await message.answer_photo(
                            photo=photo_file,
                            caption=f"{item.title}\nЦена: {item.cost} руб.",
                            reply_markup=kb.create_catalog_keyboard(item.id) 
                    )
                
    logging.info('Отправлены товары с кнопками')





        
# обработчик кнопки Каталог товаров
# если нажать Подробное описание
@router_client.callback_query(F.data.startswith('description_'))
async def description(call: CallbackQuery, state: FSMContext):
    logging.info('Сработала кнопка описания товаров')
    
    # Извлекаем идентификатор товара из callback_data
    product_id = call.data.split('_')[1]  # Получаем идентификатор товара
    product_description = await get_item_description_from_db(int(product_id))  # Получаем описание товара
    
    await call.message.answer(product_description)  # Отправляем описание
    await call.answer()






# обработчик кнопки Каталог товаров
# если нажать Купить

class Reg(StatesGroup):
    title = State()
    name = State()
    adress = State()
    pay = State()
    phone_number = State()


@router_client.callback_query(F.data.startswith('buy_'))
async def description(call: CallbackQuery, state: FSMContext):
    # Извлекаем идентификатор товара из callback_data
    product_id = call.data.split('_')[1]  # Получаем идентификатор товара
    title = await get_item_title_from_db(int(product_id))  # Получаем описание товара
    await state.update_data(title=title)
    logging.info('Запустился процесс покупки товара')
    await call.message.answer('Заполните небольшую форму для покупки товара: ') 
    await call.message.answer('Введите Ваше имя:') 
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
    await message.answer('Каким способом вам будет удобно платить? Можно оплатить товар при получении наличными или картой курьеру.')
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
    await state.update_data(phone_number=phone_number)

    # Получаем данные пользователя 
    data = await state.get_data()
    title = data.get('title')
    name = data.get('name')
    adress = data.get('adress')
    pay = data.get('pay')
    phone_number = data.get('phone_number')
    
    # Формируем читаемое сообщение 
    order_info = (
        f"Оформлен заказ от {message.from_user.username} - {name}, на {title}.\n"
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
    '''await bot.send_message(ADMIN, f"Новое сообщение: {order_info}")
    logging.info('Сообщение отправлено администратору')'''

    # Завершаем состояние
    await state.set_state(None)  # Устанавливает состояние в None


'''----------------КОНЕЦ ОФОРМЛЕНИЯ ЗАКАЗА-------------'''   
    

#-----------------END-CLIENT--------------------
