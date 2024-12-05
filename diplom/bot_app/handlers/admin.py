from datetime import datetime, timedelta
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

import bot_app.keyboards as kb
from bot_app.config import ADMIN
from sign_in.models import CustomUser   

router_admin = Router()

host = 'http://127.0.0.1:8000/bot/'

#-----------------ADMIN-----------------------

@router_admin.message(Command('admin'))
async def admin(message: Message):
    if message.from_user.id in ADMIN:
        await message.answer("Панель Администратора", reply_markup=kb.admin_panel)
    else:
        await message.answer("Вы не являетесь Админом!", reply_markup=None)

# обработчик кнопки Клиенты
@router_admin.message(F.text == 'Клиенты')
async def get_profile(message: Message):
    all_users_data = CustomUser .objects.all()
    admin_text = (f'👥 В базе данных <b>{len(all_users_data)}</b> человек. Вот короткая информация по каждому:\n\n')

    for user in all_users_data:
        admin_text += (
                f'👤 Телеграм ID: {user.user_id}\n'
                f'📝 Полное имя: {user.full_name}\n'
            )
        if user.user_login is not None:
                admin_text += f'🔑 Логин: {user.user_login}\n'

        await message.answer(admin_text)        

# обработчик кнопки Статистика
@router_admin.message(F.text == 'Статистика')
async def admin_stat(message: types.Message):
    # Получаем общее количество пользователей
    total_users = CustomUser.objects.count()
    # Определяем дату 7 дней назад
    week_ago = datetime.now() - timedelta(days=7)
    # Получаем количество активных пользователей за последние 7 дней
    active_users = CustomUser.objects.filter(last_activity__gte=week_ago).count()

    # Формируем текст ответа
    stats_text = (
        f"📊 <b>Статистика бота:</b>\n"
        f"👥 Общее количество пользователей: <b>{total_users}</b>\n"
        f"🟢 Количество активных пользователей за последние 7 дней: <b>{active_users}</b>\n")

    await message.answer(stats_text)
 

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
        user = CustomUser.objects.get(id=int(user_id_to_del))
        user.delete()
        await message.answer(f'Пользователь с ID {user_id_to_del} удален.')
    except CustomUser.DoesNotExist:
        await message.answer(f'Пользователь с ID {user_id_to_del} не найден.')
    finally:
        await state.finish()  # Завершаем состояние

#-----------------END-ADMIN--------------------
