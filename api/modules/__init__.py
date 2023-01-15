# -*- coding: utf-8 -*-

from loguru import logger as log

import os
from modules import config
from flask import Flask, request, abort
from flask_cors import CORS

# from werkzeug.contrib.fixers import ProxyFix
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

async_mode = 'eventlet'

app = Flask(__name__)
CORS(app)
# app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

app_settings = os.getenv(
    'API_SETTINGS',
    'modules.config.Development'
)
app.config.from_object(app_settings)
app.logger.disabled = True


db_session = db = SQLAlchemy(app, engine_options={'pool_size': 50, 'max_overflow': 10},
                             session_options={"autoflush": False, "autocommit": False})

# local_base = 'postgresql://{user}:{passw}@{host}:{port}/'.format(user=config.db_params['user'],
#                                                                  passw=config.db_params['passw'],
#                                                                  host=config.db_params['host'],
#                                                                  port=config.db_params['port'])
# data_base_uri = local_base + config.database_name
# engine = create_engine(data_base_uri)
# Session = scoped_session(sessionmaker(bind=engine))
#
#
# @contextmanager
# def session_scope():
#     """Provide a transactional scope around a series of operations."""
#     session = Session()
#     try:
#         yield session
#         session.commit()
#     except Exception as ex:
#         log.error(ex)
#         raise
#     finally:
#         Session.remove()


ma = Marshmallow(app)

# region LOGGING
LOG_PATH = os.getenv('LOG_DIR') or './logs'

info_filter = lambda record: record["level"].name == "INFO" or record["level"].name == "DEBUG"
log.add(LOG_PATH + '/info.log', filter=info_filter, level="DEBUG", rotation="30 MB", retention="10 days",
        backtrace=False, diagnose=False)

error_filter = lambda record: record["level"].name == "ERROR"
log.add(LOG_PATH + '/error.log', filter=error_filter, level="DEBUG", rotation="30 MB", retention="10 days",
        backtrace=False, diagnose=False)

# endregion

api = Api(title='Food Backend API',
          version='1.0',
          description='Food Backend API')

prefix = '/v1'


from .v1.project.controllers.food_category import api as food_category_api_ns
from .v1.project.controllers.topping import api as topping_api_ns
from .v1.project.controllers.food import api as food_api_ns

api.add_namespace(food_category_api_ns, path=prefix + '/food_category')
api.add_namespace(topping_api_ns, path=prefix + '/topping')
api.add_namespace(food_api_ns, path=prefix + '/food')

