# -*- coding: utf-8 -*-
from flask_restplus import Namespace, Resource, reqparse

from common.controllers_template import controller_fabric
from ..models import models
from modules import db_session
from modules import log

# from ..services import user_role_service as service


main_model = models.Topping


api = Namespace('Ингредиенты', description='Ингредиенты')

main_model = models.Topping

from modules.v1.project.data_access.schemas import ToppingSchemas as schemas
(main_schema, put_schema, post_schema, list_schema) = schemas


# def before_crud(payload: any, action: str) -> str:
#     # Валидация
#     if action == 'put' or action == 'post':
#         error = service.user_role_save_validation_error(payload, log, db_session.session)
#         if error:
#             return error
#     return ''


Controller, ControllerId = controller_fabric(api, main_model, db_session, log, main_schema, list_schema)
