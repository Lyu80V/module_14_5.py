from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *
initiate_db()

api = '720'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()     # возраст
    growth = State()  # рост
    weight = State()  # вес
    gender = State()  # пол

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State(1000)


m_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Регистрация')
button3 = KeyboardButton(text='Купить')
m_kb.row(button, button2, button3)

kb = InlineKeyboardMarkup()
button4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button5 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.row(button4, button5)

b_kb = InlineKeyboardMarkup()
button6 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
button7 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
button8 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
button9 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
b_kb.row(button6, button7, button8, button9)



@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Привет, {message.from_user.username}! Я бот помогающий твоему здоровью.', reply_markup=m_kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await  message.answer('Выберите опцию:', reply_markup=kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('(10 * вес + 6.25 * рост - 5 * возраст + 5) - для мужчин, '
                              '\n(10 * вес + 6.25 * рост - 5 * возраст - 161) - для женщин')
    await call.answer()

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
        return

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer("Регистрация прошла успешно")
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in get_all_products():
        await message.answer(f'Название: {i[1]}| Описание: описание{i[2]}| Цена: {i[3]}')
        with open(f'{i[0]}img.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=b_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст(г):')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост(см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес(кг):')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Введите свой пол(муж/жен):')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    if data['gender']=='муж':
        norma_1 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)  # для мужчин
        await message.answer(f'Ваша норма колорий:\n {norma_1} ккал')
        await state.finish()
    elif data['gender'] == 'жен':
        norma_2 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)  # для женщин
        await message.answer(f'Ваша норма колорий: {norma_2} ккал')
        await state.finish()
    else:
        await message.answer('Что-то пошло не так, попробуйте ещё раз')
        await UserState.gender.set()
        return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)