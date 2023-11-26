from os import getenv

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

db_name = getenv("DB_NAME")
