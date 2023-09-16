import psycopg2
from config import host, password, db_name, user


class DbWorker(object):
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def open_connection(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.cursor = self.connection.cursor()

    def get_all_users(self):
        return self.returner("""SELECT * FROM users""")

    def get_number_of_users(self):
        return len(self.returner('SELECT id FROM users'))

    def get_one_user(self, user_id: str):
        return self.returner(f"""SELECT * FROM users WHERE id = {user_id}""")

    def add_user(self, username: str, profile_photo_address: str):
        return self.returner(
            f"""INSERT INTO users (id, name, profile_photo_address) values({self.get_number_of_users() + 1},
             '{username}', '{profile_photo_address}')""",
            full_fetching=False, commit=True)

    def edit_user_info(self, user_id, user_name, user_photo_address, change_name, change_path):
        if change_name and change_path:
            return self.returner(
                f'''UPDATE users SET name = '{user_name}', profile_photo_address = '{user_photo_address}' WHERE id = {user_id}''',
                full_fetching=False, commit=True)
        elif change_name:
            return self.returner(f'''UPDATE users SET name = '{user_name}' WHERE id = {user_id}''',
                                 full_fetching=False, commit=True)
        else:
            return self.returner(
                f'''UPDATE users SET profile_photo_address = '{user_photo_address}' WHERE id = {user_id}''',
                full_fetching=False, commit=True)

    # Мы не удаляем запись, а делаем пустой, т.к. индексация фото идёт по id,
    # и если смещать все id при удалении, то надо будет переименовывать все файлы фото.
    def delete_user(self, user_id: int):
        return self.returner(f'''UPDATE users SET name = ' ', profile_photo_address = ' ' WHERE id = {user_id}''',
                             full_fetching=False, commit=True)

    def create_db(self, name_db):
        return self.returner(f'''CREATE TABLE {name_db}
                                  (ID INT PRIMARY KEY     NOT NULL,
                                  NAME           TEXT    NOT NULL,
                                  profile_photo_address         TEXT NOT NULL); ''', commit=True, full_fetching=False)

    def clear_db(self, name_db: str):
        number = self.get_number_of_users()
        for i in range(number):
            self.returner(f"DELETE FROM {name_db} WHERE id = '{i + 1}'", full_fetching=False, commit=True)
        return

    def returner(self, execution_line, full_fetching=True, commit=False):
        if not full_fetching:
            self.open_connection()
            self.cursor.execute(execution_line)
            result = 'Success'
        else:
            self.open_connection()
            self.cursor.execute(execution_line)
            result = self.cursor.fetchall()
        if commit:
            self.connection.commit()
        self.close_connection()
        return result
