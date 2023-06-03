from aiogram import types, executor, Dispatcher, Bot
from config import BOT_TOKEN
from aiogram.types import ReplyKeyboardRemove
from keyboards import day_ikb, time_kb1, time_kb2, time_kb3, time_kb4, time_kb5, time_kb6, time_kb7, day_kb, \
    time_kb_for_update
from db import BotDB
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageTextIsEmpty, ChatNotFound
from mysql.connector.errors import IntegrityError
import sys

day_for_delete = '1'
day_for_update = '1'
time_for_update = '1'
admins_interval = 7
last_id = 0
"""память машины состояний"""
storage = MemoryStorage()

"""имя бд"""
BotDB = BotDB('prov.db')

"""бот, прокси"""
bot = Bot(token=BOT_TOKEN)
"""диспатчер"""
dp = Dispatcher(bot=bot,
                storage=storage)
"""список дней"""
day_mas = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
"""список клавиату"""
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

commands = "Откройте меню чтобы посмотреть какие команды тут есть."
class StatesGroup(StatesGroup):
    """класс состояний мышины состояний"""
    password = State()
    time = State()
    day = State()
    time_for_update = State()
    update_time = State()
    delete_day = State()
    delete_time = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Добро пожаловать. Введите пароль чтобы войти")
    """ожидает сообщение с паролем от пользователя"""
    await StatesGroup.password.set()


@dp.message_handler(state=StatesGroup.password)
async def tutor_command(message: types.Message, state: FSMContext):
    try:
        """извелекает пароль"""
        password = message.text
        BotDB.add_admin_id(message.from_user.id, password)
        pasw = str(BotDB.select_password(message.from_user.id)[0])
        """проверяет пароль с введёнными"""
        if pasw == password:
            root_password = BotDB.select_root_password(1)[0]
            """обнуляет состояние"""
            await state.finish()

            await message.delete()
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Выберите день",
                                   parse_mode='HTML',
                                   reply_markup=day_ikb)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=commands)

            @dp.message_handler(commands=['update_time'])
            async def select_day_command(message: types.Message):
                await message.delete()
                await bot.send_message(message.from_user.id,
                                       text="Введите день, у которого хотите обновить время. Если вы хотите "
                                            "остановить перестановку  времени пишите stop",
                                       reply_markup=day_kb)
                await StatesGroup.day.set()

            @dp.message_handler(state=StatesGroup.day)
            async def update_time_command(message: types.Message):
                global day_for_update
                await message.delete()
                await state.finish()
                if message.text != 'stop':
                    day_for_update = message.text
                    await bot.send_message(message.from_user.id,
                                           text=message.text,
                                           reply_markup=ReplyKeyboardRemove())
                    await bot.send_message(message.from_user.id,
                                           text='Введите, что вы хотите обновить. Если вы хотите остановить перестановку '
                                                'времени пишите stop',
                                           reply_markup=time_kb_for_update)
                    time1 = BotDB.select_time_for_update1(day_for_update)[0]
                    await bot.send_message(message.from_user.id,
                                           text='Текущее время для time1 - ' + time1)
                    time2 = BotDB.select_time_for_update2(day_for_update)[0]
                    await bot.send_message(message.from_user.id,
                                           text='Текущее время для time2 - ' + time2)
                    await StatesGroup.time_for_update.set()
                else:
                    await bot.send_message(message.from_user.id,
                                           text='Процесс был остановлен.')

            @dp.message_handler(state=StatesGroup.time_for_update)
            async def update_time_command(message: types.Message):
                global time_for_update
                await message.delete()
                await state.finish()
                if message.text != 'stop':
                    time_for_update = message.text
                    await bot.send_message(message.from_user.id,
                                           text=message.text,
                                           reply_markup=ReplyKeyboardRemove())
                    await bot.send_message(message.from_user.id,
                                           text='Введите, на какое время вы хотите поменять текущее. Вводите так'
                                                ' часы:время (xx:xx). Если вы хотите остановить перестановку '
                                                'времени пишите stop')
                    await StatesGroup.update_time.set()
                else:
                    await bot.send_message(message.from_user.id,
                                           text='Процесс был остановлен.')

            @dp.message_handler(state=StatesGroup.update_time)
            async def update_time_command(message: types.Message):
                global time_for_update
                global day_for_update
                global admins_interval
                await state.finish()
                await message.delete()
                if message.text != 'stop':
                    if time_for_update == 'time1':
                        last_time = BotDB.select_time_for_update1(day_for_update)[0]
                        BotDB.update_time1(message.text, day_for_update)

                    if time_for_update == 'time2':
                        last_time = BotDB.select_time_for_update2(day_for_update)[0]
                        BotDB.update_time2(message.text, day_for_update)
                    users_to_update_time = BotDB.select_users_to_update_time(day_for_update, last_time)

                    j = 0
                    try:
                        print(users_to_update_time)
                        while len(users_to_update_time) > j:
                            this_user = users_to_update_time[j][1]
                            this_user_id = users_to_update_time[j][0]
                            BotDB.delete_need_day_us(this_user_id)
                            last_day_id = BotDB.select_last_user_id(this_user)[0]
                            last_day_and_time = BotDB.select_user_day_and_time(last_day_id)
                            try:
                                if this_user_id != last_day_id:
                                    BotDB.update_day_id_us(this_user_id, last_day_and_time[0], last_day_and_time[1])
                            except IntegrityError:
                                k = 0
                            try:
                                await bot.send_message(this_user,
                                                       text='Ваше время записи ' + day_for_update + ' ' + last_time + ' теперь недоступно, так что его пришлось удалить, извиняемся за неудобство')
                            except ChatNotFound:
                                k = 0
                            j += 1
                    except IndexError:
                        k = 0

                    admins_to_update_time = BotDB.select_admins_to_update_time(day_for_update, last_time)
                    try:
                        print(admins_to_update_time[0])
                        this_admin = admins_to_update_time[0][1]
                        this_admin_id = admins_to_update_time[0][0]
                        BotDB.delete_need_day(this_admin_id)
                        last_day_id = BotDB.select_last_user_id(this_admin)[0]
                        last_day_and_time = BotDB.select_admin_day_and_time(last_day_id)
                        try:
                            if this_admin_id != last_day_id:
                                BotDB.update_day_id(this_admin_id, last_day_and_time[0], last_day_and_time[1])
                        except IntegrityError:
                            k = 0
                        await bot.send_message(this_admin,
                                               text='Ваше время записи ' + day_for_update + ' ' + last_time + ' теперь недоступно, так что его пришлось удалить, извиняемся за неудобство')
                    except IndexError:
                        k = 0

                    await bot.send_message(message.from_user.id,
                                           text=message.text,
                                           reply_markup=ReplyKeyboardRemove())
                    await bot.send_message(message.from_user.id,
                                           text='Время успешно обновлено')
                else:
                    await bot.send_message(message.from_user.id,
                                           text='Процесс был остановлен.')

            @dp.message_handler(commands=['alert'])
            async def delete_admin_command(message: types.Message):
                await message.delete()
                all_admins = BotDB.select_all_admins_user_id('1')
                j = 0
                while len(all_admins) > j:
                    try:
                        await bot.send_message(all_admins[j][0],
                                               text="Извиняемся за неудобства.")
                    except ChatNotFound:
                        k = 0
                    j += 1
                j = 0
                all_users = BotDB.select_all_users('1')
                """эта функция удаляет админа и все его дни"""
                while len(all_users) > j:
                    try:
                        await bot.send_message(all_users[j][0],
                                               text="Извиняемся за неудобства.")
                    except ChatNotFound:
                        k = 0
                    j += 1
                BotDB.delete_unfinished_day('2')
                await bot.send_message(message.from_user.id,
                                       text="Уведомления отправлены")
                sys.exit()

            @dp.message_handler(commands=['help'])
            async def help_command(message: types.Message):
                await message.delete()
                """эта функция показывает все команды корневого админа"""
                await bot.send_message(message.from_user.id,
                                       text="Чтобы ввести новый интервал между админами(со старта он = 7) введитие - /new_admins_interval_корневойпароль \\например /new_admins_interval_222"
                                            "\n\nЧтобы добавить нового админа введите - /add_new_admin_корневойпароль \\например  /add_new_admin_222"
                                            "\n\nчтобы разлогиниться из обычного админа корневому введите - /unlog_корневойпароль \\например  /unlog_222 (учтите все дни этого админа удалятся)"
                                            "\n\nчтобы увидеть всех админов введите - /all_admins_корневойпароль \\например  /all_admins_222 (3 в никнейме означает что пароль никем не занят)"
                                            "\n\nчтобы удалить админа введие - /delete_admin_корневойпароль пароль (пароль админа которого хотите удалить) \\например /delete_admin_222 152"
                                            "\n\nчтобы увидеть все команды в телеграмме введите - /help_корневойпароль \\например /help_222"
                                            "\n\nчтобы поменять время в таблице со временем введите - /update_time_корневойпароль \\например /update_time_222"
                                            "\n\nчтобы прекратить работу бота после смены времени в таблице со временем введите - /alert_корневойпароль \\например /alert_22 "
                                            "(обязательно делайте это и запускайте бота заново если вы закончили изменять время в таблице со временем)")

            @dp.callback_query_handler()
            async def day_command(callback: types.CallbackQuery):
                await callback.message.delete_reply_markup()
                await callback.message.delete()
                last_admin_id = int(BotDB.select_last_admin_id(callback.message.chat.id)[0]) + 1
                """бот проверяет коллбэк и выбирает нужнею клавиатуру с днём"""
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
                    await bot.send_message(callback.message.chat.id,
                                           text=day,
                                           reply_markup=kla)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Выберите время")

                    BotDB.add_admin_day(str(last_admin_id), day, callback.message.chat.id, 1)
                    await StatesGroup.time.set()

            @dp.message_handler(state=StatesGroup.time)
            async def time_command(message: types.Message):
                await state.finish()
                try:
                    """проверяет время ли введено"""
                    check_int = int(message.text[0:1])
                    check_int1 = int(message.text[3:4])
                    await message.delete()
                    """добавляет введённое время"""
                    BotDB.add_admin_time2(message.text, message.from_user.id)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=message.text,
                                           parse_mode='HTML',
                                           reply_markup=ReplyKeyboardRemove())
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Если вы хотите выбрать ещё один день выбирайте. " + commands,
                                           reply_markup=day_ikb)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=commands)
                except ValueError:
                    print(1)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=message.text,
                                           reply_markup=ReplyKeyboardRemove())
                    await bot.send_message(chat_id=message.from_user.id,
                                           text='Не балуйтесь со временем! Начинайте выбор дня сначала.',
                                           reply_markup=day_ikb)
                    """Удаляет день без времени"""
                    BotDB.delete_need_day(BotDB.select_last_admin_id(message.from_user.id)[0])

            @dp.message_handler(commands=['add_day'])
            async def add_command(message: types.Message):
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Выберите день",
                                       parse_mode='HTML',
                                       reply_markup=day_ikb)

            @dp.message_handler(commands=['select_all'])
            async def select_command(message: types.Message):
                """показывает все дни тьютора"""
                days_count = str(BotDB.select_admin_count_for_all_select(message.from_user.id)[0])
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
                                           text=BotDB.select_all(message.from_user.id, '1'),
                                           parse_mode='HTML',
                                           reply_markup=ReplyKeyboardRemove())
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=commands,
                                           parse_mode='HTML')

            @dp.message_handler(commands=['delete_all'])
            async def delete_command(message: types.Message):
                """удаляет все дни тьютора"""
                BotDB.delete_all(message.from_user.id)
                """бот отправляет сообщение"""
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Все ваши дни удалены.",
                                       parse_mode='HTML',
                                       reply_markup=ReplyKeyboardRemove())
                await bot.send_message(chat_id=message.from_user.id,
                                       text=commands,
                                       parse_mode='HTML',
                                       reply_markup=day_ikb)

            @dp.message_handler(commands=['delete_day'])
            async def delete_command(message: types.Message):

                """бот отправляет сообщение"""
                days_count = str(BotDB.select_admin_count_for_all_select(message.from_user.id)[0])
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
                                           text=BotDB.select_all(message.from_user.id, '1'),
                                           parse_mode='HTML',
                                           reply_markup=ReplyKeyboardRemove())
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Какой день вы хотите удалить?",
                                           parse_mode='HTML',
                                           reply_markup=day_kb)
                    await StatesGroup.delete_day.set()

            @dp.message_handler(state=StatesGroup.delete_day)
            async def time_command(message: types.Message):
                global day_for_delete
                await state.finish()
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
                    await bot.send_message(message.from_user.id,
                                           text=day_for_delete,
                                           reply_markup=kla)
                    await StatesGroup.delete_time.set()
                else:
                    await bot.send_message(message.from_user.id,
                                           text='Процесс остановлен')

            @dp.message_handler(state=StatesGroup.delete_time)
            async def time_command(message: types.Message):
                await message.delete()
                time_for_delete = message.text
                if message.text != 'stop':
                    last_day_id = BotDB.select_last_admin_id(message.from_user.id)[0]
                    need_day_id = BotDB.select_need_day_id(day_for_delete, time_for_delete)
                    BotDB.delete_need_day_1(day_for_delete, time_for_delete)
                    if last_day_id == need_day_id:
                        k = 0
                    else:
                        last_day_id = BotDB.select_last_admin_id(message.from_user.id)[0]
                        last_day_and_time = BotDB.select_admin_day_and_time(last_day_id)
                        try:
                            BotDB.update_day_id(message.from_user.id, last_day_and_time[0], last_day_and_time[1])
                        except IntegrityError:
                            k = 0
                        await bot.send_message(message.from_user.id,
                                               text=message.text)
                        await bot.send_message(message.from_user.id,
                                               text='день и время удалены')
                else:
                    await bot.send_message(message.from_user.id,
                                           text='Процесс остановлен')
                await state.finish()

            @dp.message_handler(commands=['look_all'])
            async def look_command(message: types.Message):
                """показывает всех пользователей у которых день и время совпадает с тьютором"""


                await bot.send_message(chat_id=message.from_user.id,
                                       text="все пользователи у которых день и время совпадает с вашим: ",
                                       parse_mode='HTML',
                                       reply_markup=ReplyKeyboardRemove())
                j = 0
                all_users = BotDB.select_all_users('1')
                while len(all_users) > j:
                    num = j+1
                    await bot.send_message(chat_id=message.from_user.id,
                                           text='Имя '+str(num)+' пользователя - '+BotDB.select_name(all_users[j][0])[0],
                                           parse_mode='HTML',
                                           reply_markup=ReplyKeyboardRemove())
                    await bot.send_message(chat_id=message.from_user.id,
                                           text='Все дни этого пользователя: '+BotDB.select_all_for_user(all_users[j][0], '1'),
                                           parse_mode='HTML',
                                           reply_markup=ReplyKeyboardRemove())

                    j += 1

        else:
            await bot.send_message(message.from_user.id,
                                   text="Введите пароль заново.")

    except TypeError:
        await bot.send_message(message.from_user.id,
                               text="Введите пароль заново.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
