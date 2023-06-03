from aiogram import types, executor, Dispatcher, Bot
from config import BOT_TOKEN1
from aiogram.types import ReplyKeyboardRemove
from keyboards import day_ikb, time_kb1, time_kb2, time_kb3, time_kb4, time_kb5, time_kb6, time_kb7
from db import BotDB
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from mysql.connector.errors import DataError
import sys
import time
"""память машины состояний"""
storage = MemoryStorage()

"""имя бд"""
BotDB = BotDB('prov.db')

"""бот, прокси"""
bot = Bot(token=BOT_TOKEN1)

"""диспатчер"""
dp = Dispatcher(bot=bot,
                storage=storage)


commands = "выберите команду"

root_password = BotDB.select_root_password(1)[0]
"""создание кнопок времени ко всем дням исключая пустое время"""
day_mas = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
kb_mas = [time_kb1, time_kb2, time_kb3, time_kb4, time_kb5, time_kb6, time_kb7]
i = 0
checking_the_addition = False
while i <= 6:
    try:
        kb_mas[i].add(str(BotDB.select_time1(day_mas[i])), str(BotDB.select_time2(day_mas[i])))
        checking_the_addition = True
    except TypeError:
        kb_mas[i].add(str(BotDB.select_time2(day_mas[i])))
        checking_the_addition = True
    if checking_the_addition == False:
        try:
            kb_mas[i].add(str(BotDB.select_time1(day_mas[i])))
        except TypeError:
            checking_the_addition = False
    checking_the_addition = False
    i += 1


class StatesGroup(StatesGroup):
    """класс состояний мышины состояний"""
    name = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        try:
            need_id = int(BotDB.select_last_user('1')[0]) + 15
            BotDB.add_user(need_id, message.from_user.id)
        except TypeError:
            BotDB.add_user(1, message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите ваши имя, фамилию, отчество.",
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())
        await StatesGroup.name.set()

    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите одну из команд",
                           parse_mode='HTML',
                           reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['add_day'])
async def start_command(message: types.Message):
    """бот отправляет сообщение с клавиатурой дней"""
    await bot.send_message(chat_id=message.from_user.id,
                           text="В какой день вы хотите пойти на отработку?",
                           parse_mode='HTML',
                           reply_markup=day_ikb)


@dp.message_handler(commands=['update_name'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите ваши имя, фамилию, отчество.",
                           parse_mode='HTML',
                           reply_markup=ReplyKeyboardRemove())
    await StatesGroup.name.set()


@dp.message_handler(commands=['delete_all'])
async def start_command(message: types.Message):
    try:
        int(BotDB.select_last_user_id_del(message.from_user.id)[0])
        await bot.send_message(chat_id=message.from_user.id,
                               text="Все ваши дни удалены",
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())
    except TypeError:
        await bot.send_message(chat_id=message.from_user.id,
                               text="У вас нет дней.",
                               reply_markup=ReplyKeyboardRemove())
    BotDB.delete_all_user(message.from_user.id)


@dp.message_handler(commands=['delete_last_day'])
async def start_command(message: types.Message):
    try:
        last_id = int(BotDB.select_last_user_id_del(message.from_user.id)[0])
        await bot.send_message(chat_id=message.from_user.id,
                               text="Ваш последний день удалён.",
                               reply_markup=ReplyKeyboardRemove())
        BotDB.delete_need_day_user(last_id)
    except TypeError:
        await bot.send_message(chat_id=message.from_user.id,
                               text="У вас нет дней.",
                               reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['select_all'])
async def select_command(message: types.Message):
    """показывает все дни тьютора"""
    days_count = str(BotDB.select_user_count_for_all_select(message.from_user.id)[0])
    if days_count == '1':
        await bot.send_message(chat_id=message.from_user.id,
                               text='У вас нет дней',
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.from_user.id,
                               text=commands,
                               parse_mode='HTML',
                               reply_markup=day_ikb)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=BotDB.select_all_for_user(message.from_user.id, '1'),
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.from_user.id,
                               text=commands,
                               parse_mode='HTML')


@dp.callback_query_handler()
async def day_command(callback: types.CallbackQuery):
    await callback.message.delete()
    last_user_id = int(BotDB.select_last_user_id(callback.message.chat.id)[0]) + 1
    """бот проверяет коллбэк"""
    if callback.data == "day1":
        day = "Понедельник"
        kla = time_kb1
    if callback.data == "day2":
        day = "Вторник"
        kla = time_kb2
    if callback.data == "day3":
        day = "Среда"
        kla = time_kb3
    if callback.data == "day4":
        day = "Четверг"
        kla = time_kb4
    if callback.data == "day5":
        day = "Пятница"
        kla = time_kb5
    if callback.data == "day6":
        day = "Суббота"
        kla = time_kb6
    if callback.data == "day7":
        day = "Воскресенье"
        kla = time_kb7
    if callback.data == "day1" or "day2" or "day3" or "day4" or "day5" or "day6" or "day7":
        """Бот высылыает сообщение с кнопками времени"""
        count_days = int(BotDB.select_user_count(callback.message.chat.id, '1')[0])
        count_user_days = int(BotDB.select_count_user_days(day)[0])
        if count_user_days <= 2:
            if count_days <= 14:
                await bot.send_message(callback.message.chat.id,
                                       text=day,
                                       reply_markup=kla)

                BotDB.add_user_day(str(last_user_id), day, callback.message.chat.id)
                await bot.send_message(chat_id=callback.message.chat.id,
                                       text="Выберите время.")
            else:
                await bot.send_message(chat_id=callback.message.chat.id,
                                       text="Вы выбрали все возможные дни и время.")
        else:
            await bot.send_message(chat_id=callback.message.chat.id,
                                   text="Вы выбрали всё возможное время на этот день.")


@dp.message_handler(lambda message: ':' in message.text)
async def user_command(message: types.Message):
    await message.delete()
    await bot.send_message(chat_id=message.from_user.id,
                           text=message.text,
                           parse_mode='HTML',
                           reply_markup=ReplyKeyboardRemove())
    last_id = BotDB.select_last_user_id(message.from_user.id)[0]
    day = BotDB.select_need_user_day(last_id)[0]
    count_user_time = int(BotDB.select_count_user_time(day, message.text)[0])
    """бот убирает кнопки и отправляет сообщение"""
    if count_user_time >= 1:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вы уже выбирали это время",
                               reply_markup=day_ikb)
    else:
        BotDB.add_user_time(message.text, message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id,
                               text="Время успешно добавлено")


@dp.message_handler(state=StatesGroup.name)
async def user_command(message: types.Message, state: FSMContext):
    name = message.text
    """проверяет не слишком ли длинное введённое сообщение"""
    await state.finish()
    try:
        BotDB.add_username(message.from_user.id, name, '1')
        """бот отправляет сообщение"""
        await bot.send_message(chat_id=message.from_user.id,
                               text="ФИО успешно добавлено",
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())
    except DataError:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите имя, фамилию, отчество заново, ваше сообщение слишком длинное.",
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())
        await StatesGroup.name.set()


@dp.message_handler(commands=['harakiri' + str(root_password)])
async def delete_admin_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text="Уведомления отправлены")
    sys.exit()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
