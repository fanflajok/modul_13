from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard = True)
kb2 = ReplyKeyboardMarkup(resize_keyboard = True)

bu1 = KeyboardButton(text = 'Рассчитать')
bu2 = KeyboardButton(text = 'Информация')
bu3 = KeyboardButton(text = 'М')
bu4 = KeyboardButton(text = 'Ж')

kb.add(bu1)
kb.add(bu2)
kb2.add(bu3)
kb2.add(bu4)


kbinl = InlineKeyboardMarkup()
bu_inl_1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
bu_inl_2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')
kbinl.add(bu_inl_1)
kbinl.add(bu_inl_2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()




@dp.message_handler(commands=['start'])
async def start(message):
     await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text = 'Информация')
async def info(message):
    await message.answer('Пока я умею только считать норму твоих калорий')

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = kbinl)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Формулы Миффлина-Сан Жеора для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                            'Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_sex(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Введите свой пол:', reply_markup = kb2)
    await UserState.sex.set()

@dp.message_handler(state = UserState.sex, text='М')
async def calc_for_men(message, state):
    data = await state.get_data()
    calories_for_men = (10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']))+5
    await message.answer(f'Ваша норма калорий: {calories_for_men}ккал/сут')
    await state.finish()


@dp.message_handler(state = UserState.sex, text = 'Ж')
async def calc_for_women(message, state):
    data = await state.get_data()
    calories_for_women = (10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']))-161
    await message.answer(f'Ваша норма калорий: {calories_for_women}ккал/сут')
    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)