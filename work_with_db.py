import shutil
import sqlite3

from config import db_name, table_name


__all__ = ("DbWorker",)


class DbWorker(object):
    def __init__(self):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def open_connection(self):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def get_all_users(self, names=False):
        if not names:
            return self.returner(f"SELECT * FROM {table_name}")
        return self.returner(f"SELECT name FROM {table_name}")

    def get_number_of_users(self):
        return len(self.returner(f"SELECT id FROM {table_name}"))

    def get_one_user(self, user_id: str):
        return self.returner(
            f"SELECT * FROM {table_name} WHERE id = {user_id}",
        )

    def add_user(self, username: str):
        return self.returner(
            f"""INSERT INTO {table_name} (id, name) values(
            {self.get_number_of_users() + 1},
             '{username}')""",
            commit=True,
        )

    def edit_user_info(
        self,
        user_id,
        user_name,
    ):
        return self.returner(
            f"UPDATE {table_name} SET "
            f"name = '{user_name}' "
            f"WHERE id = {user_id}",
            full_fetching=False,
            commit=True,
        )

    def delete_user(self, user_id: int):
        try:
            self.delete_user_photos(user_id)
        except FileNotFoundError:
            pass
        return self.returner(
            f"DELETE FROM {table_name} " f"WHERE id = {user_id}",
            full_fetching=False,
            commit=True,
        )

    @staticmethod
    def delete_user_photos(user_id: int) -> None:
        path_for_del = f"dataSet/{user_id}"
        shutil.rmtree(path_for_del)
        return

    def create_db(self, db_naming: str):
        self.returner(
            f"""CREATE TABLE {db_naming}
             (id INT  PRIMARY KEY   NOT NULL,
             name           TEXT    NOT NULL);""",
        )

    def clear_db(self, db_naming: str):
        self.returner(
            f"""DELETE FROM {db_naming};""",
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
