# Create class Config to initiate all configurations for the app
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Config:
    CS_MYSQL_USER = getenv('CS_MYSQL_USER')
    CS_MYSQL_HOST = getenv('CS_MYSQL_HOST')
    CS_MYSQL_DB = getenv('CS_MYSQL_DB')
    CS_MYSQL_PASS = getenv('CS_MYSQL_PASS')
    CS_ENV = getenv('CS_ENV')
    CS_MYSQL_PORT = getenv('CS_MYSQL_PORT')
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{CS_MYSQL_USER}:{CS_MYSQL_PASS}@{CS_MYSQL_HOST}:{CS_MYSQL_PORT}/{CS_MYSQL_DB}'
