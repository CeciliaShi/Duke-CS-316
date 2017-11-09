import os

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:dbpasswd@localhost/gtd'.fomrat(os.getusername())
SQLALCHEMY_ECHO = True
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False