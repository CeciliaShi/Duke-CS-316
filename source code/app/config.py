import os
import pwd

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:dbpasswd@localhost/gtd'.format(pwd.getpwuid(os.getuid())[0])
SQLALCHEMY_ECHO = True
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False