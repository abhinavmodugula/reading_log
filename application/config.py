# -*- coding: utf-8 -*-
"""
Confid file

@author: abhin
"""



TESTING = False
DEBUG = False
SECRET_KEY = "environ.get('SECRET_KEY')"

SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False


