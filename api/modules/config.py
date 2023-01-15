# coding: utf-8

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv('.env')

api_server = dict(host='0.0.0.0',
                  port=49105,
                  debug=False)

rest_url = 'http://127.0.0.1:{}/v1'\
            .format(api_server.get('port', 49105))

DB_USER = os.getenv('DB_USER')
DB_PASSWD = os.getenv('DB_PASSWD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
database_name = os.getenv('DB_NAME')


db_params = dict(user=DB_USER,
                 password=DB_PASSWD,
                 host=DB_HOST,
                 port=DB_PORT,
                 database=database_name)

local_base = 'postgresql://{user}:{passw}@{host}:{port}/'.format(user=db_params['user'],
                                                                 passw=db_params['password'],
                                                                 host=db_params['host'],
                                                                 port=db_params['port'])


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', '077fb320-6dc1-4033-a8b0-5ba0a55dceb2')
    DEBUG = os.getenv('DEBUG') == 'True'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = local_base + database_name
    RESTPLUS_MASK_HEADER = False
    RESTPLUS_MASK_SWAGGER = False
    FILE_UPLOAD_FOLDER = "files"


class Development(BaseConfig):
    """Development configuration."""
    SQLALCHEMY_ECHO = True
    pass

class Testing(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class Production(BaseConfig):
    """Production configuration."""
    pass

