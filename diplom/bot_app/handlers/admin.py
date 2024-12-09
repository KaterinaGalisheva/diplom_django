from datetime import datetime, timedelta
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

import bot_app.keyboards as kb
from bot_app.config import ADMIN
from sign_in.models import CustomUser, get_users_from_db, get_user_from_db, delete_user
from bot_app.models import Notification, get_users_to_sending_message_from_db

router_admin = Router()

host = 'http://127.0.0.1:8000/bot/'

#-----------------ADMIN-----------------------






@router_admin.message(Command('admin'))
async def admin(message: Message):
    if message.from_user.id == ADMIN:
        await message.answer("Панель Администратора", reply_markup=kb.admin_panel)
    else:
        await message.answer("Вы не являетесь Админом!", reply_markup=None)

# обработчик кнопки Клиенты
@router_admin.message(F.text == 'Клиенты')
async def get_profile(message: Message):
    all_users_data = await get_users_from_db() 
    admin_text = (f'👥 В базе данных <b>{len(all_users_data)}</b> человек. Вот короткая информация по каждому:\n\n')

    for user in all_users_data:
        admin_text += (
                f'👤 Телеграм ID: {user.id}\n'
                f'📝 Полное имя: {user.username}\n'
            )
    
    await message.answer(admin_text)        



# обработчик кнопки Рассылка
'''@router_admin.message(F.text == 'Рассылка')
async def admin_sending(message: types.Message):
   # Получаем текст сообщения для рассылки
    await message.answer("Введите текст для рассылки:")

    # Ожидаем ответа от администратора
    @router_admin.message()
    async def process_message_for_broadcast(broadcast_message: types.Message):
        # Получаем всех пользователей из базы данных
        notifications = await get_users_to_sending_message_from_db()

        # Рассылаем сообщение всем пользователям
        for notification in notifications:
            notification.message = broadcast_message.text  # Устанавливаем текст сообщения
            await notification.send_notification()  # Отправляем уведомление

        await message.answer("Рассылка завершена!")

    # Регистрация обработчика для сообщения с текстом
    router_admin.message()(process_message_for_broadcast)'''


class Del(StatesGroup):
    user_id = State()

# обработчик кнопки удалить
@router_admin.message(F.text == 'Удалить пользователя')
async def admin_bloc(message: types.Message, state: FSMContext):
    await message.answer('Введите ID пользователя, которого хотите удалить:')
    await state.set_state(Del.user_id)

@router_admin.message(Del.user_id)
async def admin_bloc_delete(message: types.Message, state: FSMContext):
    user_id_to_del = message.text.strip()
    try:
        user = await get_user_from_db(user_id_to_del)
        await delete_user(user)
        await message.answer(f'Пользователь с ID {user_id_to_del} удален.')
    except CustomUser.DoesNotExist:
        await message.answer(f'Пользователь с ID {user_id_to_del} не найден.')
    finally:
        await state.set_state(None)  # Устанавливает состояние в None

#-----------------END-ADMIN--------------------
