# -*- coding: utf-8 -*-
import json
from typing import List, Type, Union
from os import path
from common.data_access import common_crud_pool as common_crud
from modules import log, db_session
from modules.v1.project.models import models


def init_food_categories():
    """ первичное заполнение Категорий блюд"""
    try:
        seed_path = 'modules/v1/seeds/json_dumps/'

        already_exist = db_session.session.query(models.FoodCategory).first() is not None

        if not already_exist:
            with open(path.relpath(seed_path + 'food_categories.json'), 'r') as input_:
                food_categories_list = json.load(input_)
                print(food_categories_list)
                common_crud.save_list_fast(models.FoodCategory, food_categories_list, log)


    except Exception as ex:
        print(ex)

