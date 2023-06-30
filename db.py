"""import MySQLdb"""
import mysql.connector


class BotDB:
    """соединение с бд(базой данных)"""
    def __init__(self, db_file):
        """соединение с бд(базой данных)"""
        self.conn = mysql.connector.connect(user='root',
                                            host='127.0.0.1',
                                            password='',
                                            database='otrab01')
        self.cursor = self.conn.cursor(buffered=True)

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        self.cursor.execute("SELECT id FROM user WHERE user_id = %s", (user_id,))
        return bool(len(self.cursor.fetchall()))

    def add_user(self, id, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO user (id, user_id, day, time, name) VALUES (%s, %s, 1, 1, 2)", (id, user_id,))
        return self.conn.commit()

    def add_username(self, user_id, name, day):
        """Добавляем имя юзера в базу"""
        self.cursor.execute("UPDATE user SET name = %s WHERE user_id = %s AND day = %s", (name, user_id, day))
        return self.conn.commit()

    def add_admin_day(self, id, days, user_id):
        """Добавляем день тьютора в базу"""
        self.cursor.execute(
            "INSERT INTO admin (id, times, days, user_id, nickname) VALUES (%s, 2, %s, %s, 1)",
            (id, days, user_id))
        return self.conn.commit()

    def add_user_day(self, id, day, user_id):
        """Добавляем день юзреа в базу"""
        self.cursor.execute(
            "INSERT INTO user (id, time, day, user_id, name) VALUES (%s, 2, %s, %s, 1)",
            (id, day, user_id))
        return self.conn.commit()

    def add_admin_time2(self, times, user_id):
        """Добавляем время тьютора в базу"""
        self.cursor.execute("UPDATE admin SET times = %s WHERE user_id = %s AND times = '2'", (times, user_id))
        return self.conn.commit()

    def add_user_time(self, time, user_id):
        """Добавляем время когда юзер придёт на отработку в базу"""
        self.cursor.execute("UPDATE user SET time = %s WHERE user_id = %s AND time = '2'", (time, user_id))
        return self.conn.commit()

    def add_admin_id(self, user_id, password):
        """Добавляем админа в базу"""
        self.cursor.execute("UPDATE admin SET user_id = %s WHERE password = %s", (user_id, password))
        return self.conn.commit()

    def select_time1(self, day):
        """достаём из бд время 1"""
        self.cursor.execute("SELECT time1 FROM time WHERE day = %s", (day,))
        output_text = ' '.join([' '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_time_for_update1(self, day):
        """достаём из бд время 1"""
        self.cursor.execute("SELECT time1 FROM time WHERE day = %s", (day,))
        return self.cursor.fetchone()

    def select_time_for_update2(self, day):
        """достаём из бд время 2"""
        self.cursor.execute("SELECT time2 FROM time WHERE day = %s", (day,))
        return self.cursor.fetchone()

    def select_password(self, user_id):
        """достаём пароль тьютора из бд"""
        self.cursor.execute("SELECT password FROM admin WHERE user_id = %s LIMIT 1", (user_id,))
        return self.cursor.fetchone()

    def select_name(self, user_id):
        """достаём имя юзера из бд"""
        self.cursor.execute("SELECT name FROM user WHERE user_id = %s LIMIT 1", (user_id,))
        return self.cursor.fetchone()

    def select_time2(self, day):
        """достаём из бд время 2"""
        self.cursor.execute("SELECT time2 FROM time WHERE day = %s", (day,))
        output_text = ' '.join([' '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_user_count(self, user_id, name):
        """достаём из бд количество дней юзера"""
        self.cursor.execute("SELECT count(id) FROM user WHERE user_id = %s AND name = %s", (user_id, name))
        return self.cursor.fetchone()

    def select_admin_count(self, user_id, nickname):
        """достаём из бд количество дней админа"""
        self.cursor.execute("SELECT count(id) FROM admin WHERE user_id = %s AND nickname = %s", (user_id, nickname))
        return self.cursor.fetchone()

    def select_count_user_days(self, day):
        """достаём из бд количество дней юзера у которых одинаковый день"""
        self.cursor.execute("SELECT count(id) FROM user WHERE day = %s", (day,))
        return self.cursor.fetchone()

    def select_count_admin_days(self, days):
        """достаём из бд количество дней aадмина у которых одинаковый день"""
        self.cursor.execute("SELECT count(id) FROM admin WHERE days = %s", (days,))
        return self.cursor.fetchone()

    def select_count_user_time(self, day, time):
        """достаём количество записей с опрёделённым днеём и временем"""
        self.cursor.execute("SELECT count(id) FROM user WHERE day = %s AND time = %s", (day, time))
        return self.cursor.fetchone()

    def select_admin_count_for_all_select(self, user_id):
        """достаём из бд количество айди тьютора где есть его юзер_айди тьютора"""
        self.cursor.execute("SELECT count(id) FROM admin WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    def select_user_count_for_all_select(self, user_id):
        """достаём из бд количество айди юзера где есть его юзер_айди тьютора"""
        self.cursor.execute("SELECT count(id) FROM user WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    def select_last_admin_id(self, user_id):
        """достаём из бд последний день тьютора"""
        self.cursor.execute("SELECT max(id) FROM admin WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    def select_last_user_id_del(self, user_id):
        """достаём из бд последний день юзеря для удаления"""
        self.cursor.execute("SELECT max(id) FROM user WHERE user_id = %s AND name = '1'", (user_id,))
        return self.cursor.fetchone()

    def select_last_user_id(self, user_id):
        """достаём из бд последний день юзера"""
        self.cursor.execute("SELECT max(id) FROM user WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    def select_need_user_day(self, id):
        """достаём из бд нужный день юзера"""
        self.cursor.execute("SELECT day FROM user WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def select_need_user_time(self, day):
        """достаём из бд время юзера по дню"""
        self.cursor.execute("SELECT time FROM user WHERE day = %s", (day,))
        output_text = '\n'.join([' '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_admin_day_and_time(self, id):
        """достаём из бд день и время выбранного айди"""
        self.cursor.execute("SELECT days, times FROM admin WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def select_user_day_and_time(self, id):
        """достаём из бд день и время выбранного айди"""
        self.cursor.execute("SELECT day, time FROM user WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def select_last_user(self, day):
        """достаём из бд последнего юзера"""
        self.cursor.execute("SELECT max(id) FROM user WHERE day = %s", (day,))
        return self.cursor.fetchone()

    def select_all_users(self, name):
        """достаём из бд айди всех админов"""
        self.cursor.execute("SELECT user_id FROM user WHERE name != %s", (name,))
        return self.cursor.fetchall()

    def select_need_day_id(self, days, times):
        """достаём из бд нужное айди по дню и времени (тьютор)"""
        self.cursor.execute("SELECT id FROM admin WHERE days = %s AND times = %s", (days, times))
        return self.cursor.fetchone()

    def select_need_day_id_us(self, day, time):
        """достаём из бд нужное айди по дню и времени (юзер)"""
        self.cursor.execute("SELECT id FROM user WHERE day = %s AND time = %s", (day, time))
        return self.cursor.fetchone()

    def select_all(self, user_id, nickname):
        """достаём из бд дни и время тьютора"""
        self.cursor.execute("SELECT days, times FROM admin WHERE user_id = %s and nickname = %s", (user_id, nickname))
        output_text = '\n'.join([' '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_all_for_user(self, user_id, name):
        """достаём из бд дни и время юзера"""
        self.cursor.execute("SELECT day, time FROM user WHERE user_id = %s and name = %s", (user_id, name))
        output_text = '\n'.join([' '.join(row) for row in self.cursor.fetchall()])
        return output_text

    def select_users_to_update_time(self, day, time):
        """достаём из бд корневым админом время для резидентов"""
        self.cursor.execute("SELECT id, user_id FROM user WHERE day = %s AND time = %s", (day, time))
        return self.cursor.fetchall()

    def select_admins_to_update_time(self, days, times):
        """достаём из бд обновлённое корневым админом время тьюторов"""
        self.cursor.execute("SELECT id, user_id FROM admin WHERE days = %s AND times = %s", (days, times))
        return self.cursor.fetchall()

    def select_time_true(self, id):
        """достаём из бд проверку нужно ли выключаться"""
        self.cursor.execute("SELECT check1 FROM time WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def select_check_update(self, check_update, user_id):
        """достаём день для удаления"""
        self.cursor.execute("SELECT day FROM user WHERE check_update = %s AND user_id = %s", (check_update, user_id))
        return self.cursor.fetchone()

    def delete_all(self, user_id):
        """удаляем все дни и время тьютора"""
        self.cursor.execute("DELETE FROM admin WHERE user_id = %s AND nickname = '1'", (user_id,))
        return self.conn.commit()

    def delete_all_user(self, user_id):
        """удаляем все дни и время юзера"""
        self.cursor.execute("DELETE FROM user WHERE user_id = %s AND name = '1'", (user_id,))
        return self.conn.commit()

    def delete_need_day(self, id):
        """удаляем выбранный день тьютора по айди"""
        self.cursor.execute("DELETE FROM admin WHERE id = %s", (id,))
        return self.conn.commit()

    def delete_need_day_us(self, id):
        """удаляем выбранный день юзера по айди"""
        self.cursor.execute("DELETE FROM user WHERE id = %s", (id,))
        return self.conn.commit()

    def delete_need_day_1(self, days, times):
        """удаляем выбранный день тьютора по дню и времени"""
        self.cursor.execute("DELETE FROM admin WHERE days = %s AND times = %s", (days, times))
        return self.conn.commit()

    def delete_need_day_1_us(self, day, time):
        """удаляем выбранный день юзера по дню и времени"""
        self.cursor.execute("DELETE FROM user WHERE day = %s AND time = %s", (day, time))
        return self.conn.commit()

    def delete_unfinished_day_user(self, time):
        """удаляем незаконченные дни у юзера"""
        self.cursor.execute("DELETE FROM user WHERE time = %s", (time,))
        return self.conn.commit()

    def update_time1(self, time1, day):
        """обновляем выбранное тайм1"""
        self.cursor.execute("UPDATE time SET time1 = %s WHERE day = %s", (time1, day))
        return self.conn.commit()

    def update_time2(self, time2, day):
        """обновляем выбранное тайм2"""
        self.cursor.execute("UPDATE time SET time2 = %s WHERE day = %s", (time2, day))
        return self.conn.commit()

    def update_day_id_us(self, id, days, times):
        """обновляем выбранное айди"""
        self.cursor.execute("UPDATE user SET id = %s WHERE day = %s AND time = %s", (id, days, times))
        return self.conn.commit()

    def update_day_id(self, id, days, times):
        """обновляем выбранное айди"""
        self.cursor.execute("UPDATE admin SET id = %s WHERE days = %s AND times = %s", (id, days, times))
        return self.conn.commit()

    def update_check_update(self, check_update, user_id, day):
        """обновляем проверку на удаление дня (у нужных дней)"""
        self.cursor.execute("UPDATE user SET check_update = %s WHERE user_id = %s AND day = %s", (check_update, user_id, day))
        return self.conn.commit()

    def update_check_update1(self, check_update, user_id):
        """обновляем проверку на удаление дня (у юзера)"""
        self.cursor.execute("UPDATE user SET check_update = %s WHERE user_id = %s", (check_update, user_id))
        return self.conn.commit()

    def update_time_true(self, check1, id):
        """обновляем проверку на выключение"""
        self.cursor.execute("UPDATE time SET check1 = %s WHERE id = %s", (check1, id))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
