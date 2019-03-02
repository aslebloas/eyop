import os
from credentials import PG_USR, PG_USR_PWD, PG_HOST, PG_DB, SECRET_K

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = SECRET_K
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(PG_USR,
                                                                PG_USR_PWD,
                                                                PG_HOST,
                                                                PG_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
