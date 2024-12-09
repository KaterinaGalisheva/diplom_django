import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
import bot_app.keyboards as kb
from sign_in.models import CustomUser, save_user


# Создание базового логирования
logging.basicConfig(filename='errors.log', level=logging.INFO)

router_sign_in = Router()


class Form(StatesGroup):
    username = State()
    email = State()
    password1 = State()
    password2 = State()
    check_state = State()
    
@router_sign_in.message(F.text == 'Регистрация')
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer('Привет. Напиши как тебя зовут: ')
    await state.set_state(Form.username)

    
@router_sign_in.message(F.text, Form.username)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Теперь напиши свой email: ')
    await state.set_state(Form.email)

@router_sign_in.message(F.text, Form.email)
async def capture_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Теперь напиши пароль более 6 символов, включая буквы: ')
    await state.set_state(Form.password1)

    
@router_sign_in.message(F.text, Form.password1)
async def capture_password1(message: Message, state: FSMContext):
    await state.update_data(password1=message.text)
    await message.answer('Повтори пароль: ')
    await state.set_state(Form.password2)


@router_sign_in.message(F.text, Form.password2)
async def capture_password2(message: Message, state: FSMContext):
    await state.update_data(password2=message.text)

# проверка данных
    data = await state.get_data()

    caption = f'Пожалуйста, проверьте все ли верно: \n\n' \
              f'<b>Полное имя</b>: {data.get("username")}\n' \
              f'<b>email</b>: {data.get("email")}\n' \
              f'<b>password1</b>: {data.get("password1")}\n' \
              f'<b>password2</b>: {data.get("password2")}'

    await message.answer(text=caption, reply_markup=kb.check_data)
    await state.set_state(Form.check_state)

# сохраняем данные
@router_sign_in.callback_query(F.data == 'correct', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    # Создание пользователя
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password1')

    user = CustomUser(username=username, email=email)
    user.set_password(password)  # Хешируем пароль
    await save_user(user)
    await call.answer('Данные сохранены')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Благодарю за регистрацию. Ваши данные успешно сохранены!')
    await state.set_state(None)  # Устанавливает состояние в None


    # запускаем анкету сначала
@router_sign_in.callback_query(F.data == 'incorrect', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Запускаем сценарий с начала')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Привет. Для начала Укажи свое имя: ')
    await state.set_state(Form.username)





        

'''------------- ОЧЕНЬ ВАЖНО!!!!!!!!!---------------

Пользователь заполняет анкету, а после передумывает. Нажимает через командное меню /start, а у него ничего не происходит. Дело в том, что сценарий, который мы запустили, не завершился.

Бывает, что происходит. В таком случае вместо имени бот записывает имя «/start», после отправляет новый вопрос «Введи возраст». Пользователь снова жмет /start, и это все идет до момента, пока пользователь не удаляет бота и не считает, что его делали некомпетентные люди.

Чтобы эту проблему избежать, стоит в своей архитектуре закладывать возможность выхода из сценария анкетирования. Лично я всегда закладываю в команде /start и в прочих командах (в их хендлерах) сброс сценария. Для этого необходимо следующее:

async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

В таком случае вы автоматически ставите закрытие сценария анкетирования, и пользователь, нажав на старт, просто получит сброс данных.

Также советую добавлять возможность выхода по клику на кнопку клавиатуры. Это может быть текстовая кнопка с надписью «Отмена» или инлайн-кнопка с call_data = cancel, а далее просто обработчик, который будет закрывать (очищать) хранилище, тем самым выбивая пользователя из сценария.

-------------------------------------------------------------------------------------------'''
























































