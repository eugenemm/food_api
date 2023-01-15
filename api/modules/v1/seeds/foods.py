# -*- coding: utf-8 -*-
import json
from typing import List, Type, Union
from os import path
from common.data_access import common_crud_pool as common_crud
from modules import log, db_session
from modules.v1.project.models import models


def init_foods():
    """ первичное заполнение Блюд"""
    try:
        seed_path = 'modules/v1/seeds/json_dumps/'

        already_exist = db_session.session.query(models.Food).first() is not None

        if not already_exist:
            with open(path.relpath(seed_path + 'foods.json'), 'r') as input_:
                foods_list = json.load(input_)
                common_crud.save_list_fast(models.Food, foods_list, log)


    except Exception as ex:
        print(ex)

