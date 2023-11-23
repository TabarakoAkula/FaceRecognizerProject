import shutil

from config import db_name, host, password, user
import psycopg2


__all__ = ()


class DbWorker(object):
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
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
            database=db_name,
        )
        self.cursor = self.connection.cursor()

    def get_all_users(self, names=False):
        if not names:
            return self.returner("SELECT * FROM users")
        return self.returner("SELECT name FROM users")

    def get_number_of_users(self):
        return len(self.returner("SELECT id FROM users"))

    def get_one_user(self, user_id: str):
        return self.returner(f"SELECT * FROM users WHERE id = {user_id}")

    def add_user(self, username: str, profile_photo_address: str):
        return self.returner(
            f"""INSERT INTO
             users (id, name, profile_photo_address)
             values({self.get_number_of_users() + 1},
             '{username}', '{profile_photo_address}')""",
            full_fetching=False,
            commit=True,
        )

    def edit_user_info(
        self,
        user_id,
        user_name,
        user_photo_address,
        change_name,
        change_path,
    ):
        if change_name and change_path:
            return self.returner(
                f"UPDATE users SET "
                f"name = '{user_name}', "
                f"profile_photo_address = '{user_photo_address}' "
                f"WHERE id = {user_id}",
                full_fetching=False,
                commit=True,
            )
        if change_name:
            return self.returner(
                f"UPDATE users SET "
                f"name = '{user_name}' "
                f"WHERE id = {user_id}",
                full_fetching=False,
                commit=True,
            )
        return self.returner(
            f"UPDATE users SET "
            f"profile_photo_address = '{user_photo_address}' "
            f"WHERE id = {user_id}",
            full_fetching=False,
            commit=True,
        )

    def delete_user(self, user_id: int):
        self.delete_user_photos(user_id)
        return self.returner(
            f"UPDATE users SET name = ' ', "
            f"profile_photo_address = ' ' "
            f"WHERE id = {user_id}",
            full_fetching=False,
            commit=True,
        )

    @staticmethod
    def delete_user_photos(user_id: int) -> None:
        path_for_del = f"dataSet/{user_id}"
        shutil.rmtree(path_for_del)
        return

    def clear_db(self, name_db: str):
        self.returner(
            f"""TRUNCATE {name_db}""",
            full_fetching=False,
            commit=True,
        )
        return

    def returner(self, execution_line, full_fetching=True, commit=False):
        self.open_connection()
        self.cursor.execute(execution_line)
        if not full_fetching:
            self.cursor.execute(execution_line)
            if commit:
                self.connection.commit()
            self.close_connection()
            return "Success"
        if commit:
            self.connection.commit()
        return self.cursor.fetchall()
