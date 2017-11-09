import os

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:dbpasswd@localhost/gtd'.format(os.getusername())
SQLALCHEMY_ECHO = True
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False