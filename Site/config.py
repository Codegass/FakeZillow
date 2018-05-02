#encoding: utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wch1993118@localhost/flask?charset=utf8'

SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True


