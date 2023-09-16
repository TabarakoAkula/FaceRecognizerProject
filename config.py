from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

host = getenv('HOST')
db_name = getenv('DB_NAME')
password = getenv('PASSWORD')
user = getenv('USER')
