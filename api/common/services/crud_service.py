# -*- coding: utf-8 -*-
from common.data_access import common_crud_pool as common_crud


def getListFPS(log, model, session, load_options=None):
    rows, total_count = common_crud.get_fsp(log, model, session, load_options)

    return rows, total_count


def getById(model, _id, log, session, user_id=None):

    _row = common_crud.get_by_id(model, _id, log, session, user_id)
    return _row
