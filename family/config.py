import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


class Config:
    """ App config settings """
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', "sqlite:///family_organizer.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True