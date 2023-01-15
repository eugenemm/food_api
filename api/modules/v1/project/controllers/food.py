# -*- coding: utf-8 -*-
from flask_restplus import Namespace, Resource, reqparse
from flask_accepts import responds

from common.common_responses import response500
from common.controllers_template import controller_fabric
from common.services import crud_service
from ..models import models
from modules import db_session
from modules import log

# from ..services import user_role_service as service

main_model = models.Food

from modules.v1.project.data_access.schemas import FoodSchemas as schemas, GroupedFoodSchemas

(main_schema, put_schema, post_schema, list_schema) = schemas
(gr_main_schema, gr_put_schema, gr_post_schema, gr_list_schema) = GroupedFoodSchemas

api = Namespace('Блюда', description='Блюда')


# Controller, ControllerId = controller_fabric(api, main_model, db_session, log, main_schema, list_schema)

@api.route('', strict_slashes=False)
@api.response(200, 'Success')
@api.response(400, 'Validation error')
@api.response(500, 'Error')
class MainTemplate(Resource):
    @responds(schema=gr_list_schema,
              api=api, status_code=200)
    def get(self):
        """Получение списка записей"""

        parser = reqparse.RequestParser()
        parser.add_argument('filter', type=str)
        load_options = parser.parse_args()

        strer = 'Ошибка чтения списка из базы. '
        result = None
        total_count = None

        try:
            result, total_count = crud_service.getListFPS(log, main_model, db_session.session, load_options)

            from itertools import groupby
            groups = groupby(result, lambda x: (x.category))
            _result = []
            for key, group in groups:
                obj = {"id": key.id, "name": key.name}
                obj["foods"] = list(group)
                _result.append(obj)
                # _result[key] = {
                #     "foods": list(group)
                # }

        except Exception as ex:
            strer += str(ex)

        if result is None:
            return response500(strer, log)
        else:
            __res = gr_list_schema.dumps(_result)

            return _result


@api.route('/<int:id_>')
@api.param('id_', 'Идентификатор записи')
@api.response(200, 'Success')
@api.response(400, 'Validation error')
@api.response(500, 'Error')
class ControllerId(Resource):

    @responds(schema=main_schema,
              api=api, status_code=200)
    def get(self, id_):
        """Получение записи"""

        strer = 'Ошибка получения сущности по идентификатору. '
        result = None

        try:
            entity = db_session.session.query(main_model) \
                .filter(main_model.id == id_) \
                .one()

            result = entity

        except Exception as ex:
            strer += str(ex)

        if result is None:
            return response500(strer, log)
        else:
            return result
