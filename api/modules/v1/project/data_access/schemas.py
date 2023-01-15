# -*- coding: utf-8 -*-
from marshmallow import fields

from common.services.mapping import flat_main_schema_fabric, slave_schemas_fabric
from ..models import models

ToppingSchema = flat_main_schema_fabric('Topping', models.Topping)
ToppingSchemas = (ToppingSchema, *slave_schemas_fabric(ToppingSchema, models.Topping))


class FoodSchema(flat_main_schema_fabric('FoodSchema', models.Food)):
    toppings = fields.Pluck(ToppingSchema, 'name', many=True)


FoodSchemas = (FoodSchema, *slave_schemas_fabric(FoodSchema, models.Food))


FoodCategorySchema = flat_main_schema_fabric('FoodCategory', models.FoodCategory)
FoodCategorySchemas = (FoodCategorySchema, *slave_schemas_fabric(FoodCategorySchema, models.FoodCategory))


class GroupedFoodSchema(flat_main_schema_fabric('GroupedFoodListSchema', models.FoodCategory)):
    foods = fields.List(fields.Nested(FoodSchema))


GroupedFoodSchemas = (GroupedFoodSchema, *slave_schemas_fabric(GroupedFoodSchema, models.FoodCategory))
