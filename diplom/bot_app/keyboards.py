from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from spacestore.models import get_items_from_db







# одноразовая клавиатура
'''kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)'''
# удаление клавиатуры
'''@dp.message_handler()
async def starter(message: types.Message):
    await message.answer('Рады вас видеть', reply_markup = ReplyKeyboardRemove)'''
# создать клавиатуру с множеством кнопок из списка
'''cars = ['bmv', 'mersedes', 'tesla']
async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InLineKeyboardButton(text=car, callback_data = f'car_{car}'))
    return keyboard.adjust(2).as_markup()
    вызвать в answer reply_markup = await kb.inline_cars()'''
# сделать так,чтобы после срабатывания инлайн клавиатуры, в ней появлялась другая инлайн клавиатура
'''await call.message.edit_text('Hi!', reply_markap = await kb.inline_cars())'''


#-----------------CLIENT--------------------

# создаем приветственную клавиатуру
main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Информация о магазине')],
    [KeyboardButton(text = 'Связь с оператором')],
    [KeyboardButton(text = 'Каталог товаров')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню')



# создаем инлайн клавиатуру для информация о магазине
ik_button_info_store = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text= 'График работы', callback_data= 'grafik'), 
     InlineKeyboardButton(text= 'Адрес', callback_data= 'adress')],
     [InlineKeyboardButton(text= 'Доставка', callback_data= 'delivery')]
     ]
     )

# создаем инлайн клавиатуру для каталог товаров
def create_catalog_keyboard(product_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подробное описание', callback_data=f'description_{product_id}')],
        [InlineKeyboardButton(text='Купить', callback_data=f'buy_{product_id}')]
    ])

#-----------------END-CLIENT--------------------


#-----------------ADMIN-----------------------

# клавиатура для администратора
admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Клиенты", callback_data="users")],
    [InlineKeyboardButton(text="Статистика", callback_data="stat")],
    [InlineKeyboardButton(text="Удалить пользователя", callback_data="block")]])



#-----------------END-ADMIN--------------------

