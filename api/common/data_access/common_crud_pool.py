# coding: utf-8
import copy
import json

from typing import Optional, List, TypeVar, Union, Tuple


from sqlalchemy import cast, String
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.sql import sqltypes

from common.data_access.db_conn import CreateConnection
from data_access.db_conn import create_simple_connect
from modules.v1.project.models import models

T = TypeVar('T')


def save_list_fast(_model: T, _list: List[T], log) -> Optional[bool]:
    """
    Общий метод сохранения данных в базу через connection.execute
    :param _model: модель сущности бд
    :param _list: массив сущностей для сохранения (! в виде словарей !)
    :param log:
    :return: Optional[bool]
    """

    if not isinstance(_list, list):
        return None
    if len(_list) == 0:
        return True

    with CreateConnection() as new_connection:
        connection = new_connection.connection
        try:
            connection.execute(_model.__table__.insert(), _list)
        except Exception:
            log.exception("ОШИБКА сохранения данных (model: {})".format(_model))
            return None

        else:
            return True

def raw_sql_query(log, _query: str, conn_dict: dict) -> Optional[List[dict]]:
    """
    выполнение запроса по SQL строке
    :param log:
    :param _query: сформированный запрос к базе
    :param conn_dict: словарь подключения к базе
    :return:
    """

    connection = create_simple_connect(conn_dict)
    conn_cursor = connection.cursor()
    try:
        conn_cursor.execute(_query)
        result = conn_cursor.fetchall()

    except Exception:
        log.exception("ОШИБКА выполнения сформированного запроса к базе: {0}".format(_query))
        conn_cursor.close()
        connection.close()
        return None

    conn_cursor.close()
    connection.close()
    return result


def get_by_id(model: T, _id: Union[int, str], log, session, user_id: Optional[str] = None) -> Optional[T]:
    """
    общий метод получения сущности по id в базе
    :param model: модель сущности бд
    :param _id: id сущности в базе
    :param log:
    :param user_id:
    :param session: сессия пула подключений к базе
    :return: сущность или None
    """

    # if _id is None or not isinstance(_id, uuid):
    #     return None

    try:
        entity = session.query(model)\
            .filter(model.id == _id, model.deleted.isnot(True))\
            .one()
        if user_id is not None and entity.created_by_id != user_id:
            entity = None

        return entity

    except Exception:
        log.exception("ОШИБКА получения инфо о сущности из базы: model - {}, id - {}".format(model, _id))
        session.rollback()
        return None


def get(model: T, log, session, take: int = 100000000, user_id: Optional[str] = None, not_deleted: bool = True) -> Optional[List[T]]:
    """
    получение списка сущностей из базы
    :param model: модель сущности бд
    :param log:
    :param take: ограничение кол-во поднимаемых сущностей
    :param user_id:
    :param session: сессия пула подключений к базе
    :param not_deleted: только не помеченные как удаленные в базе
    :return:
    """

    try:

        entities = session.query(model)

        # if not_deleted:
        #     entities = entities.filter(model.deleted.isnot(True))

        # if user_id is not None:
        #     entities = entities.filter(model.created_by_id == user_id)

        return entities.limit(take).all()

    except Exception:
        log.exception("ОШИБКА получения списка сущностей из базы: model - {}".format(model))
        session.rollback()
        return None



def get_fsp(log, model: T, session, load_options: Optional[dict] = None) -> Tuple[Optional[List[T]], Optional[int]]:
    """
    получение списка сущностей из базы c Filtration, Sorting, Pagination (FSP)
    :param model: модель сущности бд
    :param log:
    :param load_options: параметры пагиннации, сортировки и фильтрации
    :param user_id:
    :param session: сессия пула подключений к базе
    :return:
    """

    _filter = load_options.get('filter', None)

    try:
        entities = session.query(model)

        if model is models.Food:
            entities = entities.filter(models.Food.is_publish)

        entities = filter_query(model, entities, _filter)
        total_count = entities.count()

        return entities.all(), total_count

    except Exception as ex:
        log.exception("ОШИБКА получения списка сущностей из базы: model - {0}".format(model))
        session.rollback()
        return None, None


def filter_query(_model, _query, _filter):
    """
    разбор filter expression DevExpress Grid и фильтрация выборки
    :param _model: модель БД
    :param _query: модифицируемый запрос (объект Query)
    :param _filter: filter expression DevExpress Grid
    :return: модифицированный запрос (объект Query)
    """

    if _filter is None:
        return _query

    filter_ = json.loads(_filter) if isinstance(_filter, str) else _filter
    query_mod = append_filter_to_query(_model, _query, filter_)

    return query_mod


def append_filter_to_query(_model, _query, _filter):
    """
    рекурсивный разбор строки фильтра DevExtreme,
    отдельно анализируются левая и правая часть выражения
    :param _model: модель БД
    :param _query: модифицируемый запрос (объект Query)
    :param _filter: filter expression DevExpress Grid
    :return: модифицированный запрос (объект Query)
    """
    if not isinstance(_filter, list):
        return _query

    if not isinstance(_filter[0], list) and len(_filter) == 3:
        query_mod = append_one_filter_condition(_model, _query, _filter)
    else:
        query_mod = copy.copy(_query)
        for i in range(len(_filter)):
            if isinstance(_filter[i], list):
                query_mod = append_filter_to_query(_model, query_mod, _filter[i])
            # все элементы фильтра, не являющиеся массивами, считаем оператором "and"

    return query_mod


def append_one_filter_condition(_model, _query, _filter):
    """
     анализ подстроки фильтра DevExtreme, в которой не содержится составных выражений
     :param _model: модель БД
     :param _query: модифицируемый запрос (объект Query)
     :param _filter: строка фильтра, содежащая одно выражение вида [имя поля, правило, значение]
     :return: модифицированный запрос (объект Query)
     """
    if not isinstance(_filter, list):
        return _query

    query_mod = copy.copy(_query)

    _field = _filter[0]
    _rule = _filter[1]
    _value = _filter[2]

     # парсить поле для фильтрации которое пришло, выделять точку

    if "." in str(_field):
        field_parts = str(_field).split(".")

        # по первой части до точки определять relation-сущность
        _rel_attrs = getattr(_model, field_parts[0])
        if _rel_attrs is not None:
            from sqlalchemy.orm import contains_eager
            query_mod = query_mod.join(_rel_attrs)
            query_mod = query_mod.options(contains_eager(_rel_attrs))
            # _rel_attrs.property.innerjoin = True

            # по второй части после точки определять поле у связанной сущности
            _model = _rel_attrs.property.entity.class_
            _field = field_parts[1]


    try:
        _attr = getattr(_model, _field)
    except AttributeError:
        pass
    else:
        attr_ = _attr
        if (_rule == "contains" or _rule == "notcontains" or \
            _rule == "startswith" or _rule == "endswith") and \
           (type(_attr.property) is not ColumnProperty or \
           not isinstance(_attr.property.columns[0].type, sqltypes.String)):
            attr_ = cast(_attr, String)

        if _rule == "contains":
            query_mod = query_mod.filter(attr_.ilike("%" + _value + "%"))
        elif _rule == "notcontains":
            query_mod = query_mod.filter(attr_.notilike("%" + _value + "%"))
        elif _rule == "startswith":
            query_mod = query_mod.filter(attr_.ilike(_value + "%"))
        elif _rule == "endswith":
            query_mod = query_mod.filter(attr_.ilike("%" + _value))
        elif _rule == "=":
            query_mod = query_mod.filter(_attr == _value)
        elif _rule == "<>":
            query_mod = query_mod.filter(_attr != _value)
        elif _rule == "in":
            query_mod = query_mod.filter(_attr.in_(_value))
        elif _rule == ">=":
            query_mod = query_mod.filter(_attr >= _value)
        elif _rule == "<":
            query_mod = query_mod.filter(_attr < _value)

    return query_mod




