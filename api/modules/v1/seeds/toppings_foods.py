# -*- coding: utf-8 -*-
import json
from os import path
from modules import log, db_session
from modules.v1.project.models import models


def init_toppings_foods():
    """ первичное заполнение М-М связей"""
    try:
        seed_path = 'modules/v1/seeds/json_dumps/'

        already_exist = db_session.session.query(models.topping_food).first() is not None

        if not already_exist:
            with open(path.relpath(seed_path + 'toppings_foods.json'), 'r') as input_:
                toppings_foods_list = json.load(input_)
                for link in toppings_foods_list:
                    db_session.session.execute(models.topping_food.insert(),
                                               link)
                    db_session.session.commit()

    except Exception as ex:
        print(ex)

