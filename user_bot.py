from aiogram import types, executor, Dispatcher, Bot
from config import BOT_TOKEN1
from aiogram.types import ReplyKeyboardRemove
from keyboards import day_ikb, time_kb1, time_kb2, time_kb3, time_kb4, time_kb5, time_kb6, time_kb7, day_kb
from db import BotDB
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageTextIsEmpty
from mysql.connector.errors import DataError, IntegrityError
import sys
import os
import time

time.sleep(1)


os.system('start python teach_bot.py')

"""память машины состояний"""
storage = MemoryStorage()

"""имя бд"""
BotDB = BotDB('prov1.db')

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
    delete_day = State()
    delete_time = State()
    add_time = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
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

    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Введите одну из команд",
                               parse_mode='HTML',
                               reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['add_day'])
async def start_command(message: types.Message):
    """бот отправляет сообщение с клавиатурой дней"""
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
    await bot.send_message(chat_id=message.from_user.id,
                           text="В какой день вы хотите пойти на отработку?",
                           parse_mode='HTML',
                           reply_markup=day_ikb)


@dp.message_handler(commands=['update_name'])
async def start_command(message: types.Message):
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Введите ваши имя, фамилию, отчество.",
                           parse_mode='HTML',
                           reply_markup=ReplyKeyboardRemove())
    await StatesGroup.name.set()


@dp.message_handler(commands=['delete_all'])
async def start_command(message: types.Message):
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
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


@dp.message_handler(commands=['select_all'])
async def select_command(message: types.Message):
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
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
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
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
        if count_user_days < 2:
            if count_days <= 14:
                await bot.send_message(callback.message.chat.id,
                                       text=day,
                                       reply_markup=kla)

                BotDB.add_user_day(str(last_user_id), day, callback.message.chat.id)
                await bot.send_message(chat_id=callback.message.chat.id,
                                       text="Выберите время. Если вы больше не хотите добавлять день пишите stop")
                await StatesGroup.add_time.set()
            else:
                await bot.send_message(chat_id=callback.message.chat.id,
                                       text="Вы выбрали все возможные дни и время.")
        else:
            await bot.send_message(chat_id=callback.message.chat.id,
                                   text="Вы выбрали всё возможное время на этот день.")
    else:
        await bot.send_message(chat_id=callback.message.chat.id,
                               text="Выберите день из клавиатуры.",
                               reply_markup=day_ikb)


@dp.message_handler(state=StatesGroup.add_time)
async def user_command(message: types.Message, state: FSMContext):
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
    await message.delete()
    if message.text != 'stop':
        try:
            """проверяет время ли введено"""
            check_int = int(message.text[0:1])
            check_int1 = int(message.text[3:4])
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
                BotDB.delete_need_day_us(BotDB.select_last_user_id(message.from_user.id)[0])
            else:
                BotDB.add_user_time(message.text, message.from_user.id)
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Время успешно добавлено")
        except ValueError:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=message.text,
                                   reply_markup=ReplyKeyboardRemove())
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Не балуйтесь со временем! Начинайте выбор дня сначала.',
                                   reply_markup=day_ikb)
            """Удаляет день без времени"""
            BotDB.delete_need_day_us(BotDB.select_last_user_id(message.from_user.id)[0])
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Процесс остановлен")
    await state.finish()


@dp.message_handler(state=StatesGroup.name)
async def user_command(message: types.Message, state: FSMContext):
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
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


@dp.message_handler(commands=['delete_day'])
async def delete_command(message: types.Message):
    """бот отправляет сообщение"""
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
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
                               text="Какой день вы хотите удалить?",
                               parse_mode='HTML',
                               reply_markup=day_kb)
        await StatesGroup.delete_day.set()


@dp.message_handler(state=StatesGroup.delete_day)
async def time_command(message: types.Message, state: FSMContext):
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
    await state.finish()
    await message.delete()
    if message.text != 'stop':
        day_for_delete = message.text
        if message.text == "Понедельник":
            kla = time_kb1
        if message.text == "Вторник":
            kla = time_kb2
        if message.text == "Среда":
            kla = time_kb3
        if message.text == "Четверг":
            kla = time_kb4
        if message.text == "Пятница":
            kla = time_kb5
        if message.text == "Суббота":
            kla = time_kb6
        if message.text == "Воскресенье":
            kla = time_kb7
        try:
            await bot.send_message(message.from_user.id,
                                   text=day_for_delete,
                                   reply_markup=kla)
            await bot.send_message(message.from_user.id,
                                   text="Время: \n")
            await bot.send_message(message.from_user.id,
                                   text=BotDB.select_need_user_time(message.text))
            await StatesGroup.delete_time.set()

            BotDB.update_check_update(1, message.from_user.id, message.text)
        except MessageTextIsEmpty:
            await bot.send_message(message.from_user.id,
                                   text='У вас нет времени на этот день',
                                   reply_markup=ReplyKeyboardRemove())
        except UnboundLocalError:
            await bot.send_message(message.from_user.id,
                                   text='Это не день',
                                   reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(message.from_user.id,
                               text='Процесс остановлен',
                               reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=StatesGroup.delete_time)
async def time_command(message: types.Message, state: FSMContext):
    if BotDB.select_time_true(1)[0] == 1:
        sys.exit()
    await message.delete()
    time_for_delete = message.text
    if message.text != 'stop':
        try:
            day_for_delete = BotDB.select_check_update(1, message.from_user.id)[0]
            last_day_id = BotDB.select_last_user_id(message.from_user.id)[0]
            need_day_id = BotDB.select_need_day_id_us(day_for_delete, time_for_delete)[0]
            BotDB.delete_need_day_1_us(day_for_delete, time_for_delete)
            if last_day_id == need_day_id:
                k = 0
            else:
                last_day_id = BotDB.select_last_user_id(message.from_user.id)[0]
                last_day_and_time = BotDB.select_user_day_and_time(last_day_id)
                try:
                    BotDB.update_day_id_us(need_day_id, last_day_and_time[0], last_day_and_time[1])
                except IntegrityError:
                    k = 0
                await bot.send_message(message.from_user.id,
                                       text=message.text)
            await bot.send_message(message.from_user.id,
                                   text='День и время удалены',
                                   reply_markup=ReplyKeyboardRemove())
        except TypeError:
            await bot.send_message(message.from_user.id,
                                   text='У вас нет таких дня и времени',
                                   reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(message.from_user.id,
                               text='Процесс остановлен',
                               reply_markup=ReplyKeyboardRemove())
    BotDB.update_check_update1(0, message.from_user.id)
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

