from flask_restplus import Resource
from flask_restplus import reqparse
from flask_accepts import responds

from common.common_responses import *
from common.services import crud_service


def controller_fabric(api, main_model, db_session, log, main_schema, list_schema):

    @api.route('', strict_slashes=False)
    @api.response(200, 'Success')
    @api.response(400, 'Validation error')
    @api.response(500, 'Error')
    class MainTemplate(Resource):
        @responds(schema=list_schema,
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

                # entities = db_session.session.query(main_model)
                # result = entities.all()


            except Exception as ex:
                strer += str(ex)

            if result is None:
                return response500(strer, log)
            else:
                return result


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

    return MainTemplate, ControllerId

