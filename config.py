from os import getenv

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

host = getenv("HOST")
db_name = getenv("DB_NAME")
password = getenv("PASSWORD")
user = getenv("USER")
