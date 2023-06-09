!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
сайт хостинга pythonanywhere
убери прокси если тестируешь везде кроме этого сайта

        Если вы заливаете бота на сайт, то:
замените строчку bot = Bot(token=BOT_TOKEN) в файлах user_bot и teach_bot на bot = Bot(token=BOT_TOKEN,proxy="http://proxy.server:3128")
(в user_bot Bot(token=BOT_TOKEN1,proxy="http://proxy.server:3128") а в teach_bot Bot(token=BOT_TOKEN,proxy="http://proxy.server:3128")
,
в  def __init__ в db.file
замените:
    self.conn = mysql.connector.connect(user='root',
                                        post='127.0.0.1',
                                        password='',
                                        database='otrab01')
    self.cursor = self.conn.cursor(buffered=True)
на:
    self.conn = mysql.connector.connect(host='имя_пользователя.mysql.pythonanywhere-services.com',
                                        user='имя_пользователя',
                                        password='пароль_бд',
                                        database='имя_пользователя$название_бд')
    self.cursor = self.conn.cursor()'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
config - там содержатся токены
db - там всё связанное с бд пояснения для функций там же
keyboards - там клавиатуры
teach_bot - бот тьютора
user_bot - бот для резидента
bot - файл для запуска обоих ботов


@dp.message_handler(commands=['start']) //активируется при написании команды в кавычках после /

message.get_args() // извлекает сообщение после команды

await message.delete() // удаляет сообщение

await callback.message.delete() // удаляет сообщение в коллбек_хэндлерах



await bot.send_message(chat_id=message.from_user.id,       //куда отправлять сообщение
                       text="Если вы хотите выбрать ещё один день выбирайте. "+commands, //текст сообщения
                       parse_mode='HTML',//если хочешь добавить например жирность
                       reply_markup=day_ikb)//клавиатура если стоит ReplyKeyboardRemove() то все кнопки кроме инлайновых убираются


!!!!Создание таблиц(ввести перед началом работы)!!!!
CREATE TABLE `admin` (
  `id` int NOT NULL,
  `days` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `times` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `password` varchar(40) DEFAULT NULL,
  `user_id` varchar(20) DEFAULT NULL,
  `nickname` varchar(33) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE `user` (
  `id` int NOT NULL,
  `user_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `time` varchar(20) DEFAULT NULL,
  `check_update` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE `time` (
  `id` int NOT NULL,
  `day` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `time1` varchar(20) DEFAULT NULL,
  `time2` varchar(20) DEFAULT NULL,
  `check1` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;


!!!!добавление данных в таблицы!!!!

INSERT INTO `admin` (`id`, `days`, `times`, `password`, `user_id`, `nickname`) VALUES
(1, '1', '1', 'нужный пароль', '2', '3');  //Корневой пароль

!!!Время нужно вставлять через двоеточие воттак(часы:минуты)(если времени нет, то вставляйте 'xx:xx')!!!
INSERT INTO `time` (`id`, `day`, `time1`, `time2`, `check1`) VALUES
(1, 'Понедельник', 'xx:xx', 'xx:xx',  0),
(2, 'Вторник', 'xx:xx', 'xx:xx', 0),
(3, 'Среда', 'xx:xx', 'xx:xx', 0),
(4, 'Четверг', 'xx:xx', 'xx:xx', 0),
(5, 'Пятница', 'xx:xx', 'xx:xx', 0),
(6, 'Суббота', 'xx:xx', 'xx:xx', 0),
(7, 'Воскресенье', 'xx:xx', 'xx:xx', 0);

