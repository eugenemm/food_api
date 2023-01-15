# -*- coding: utf-8 -*-

from sqlalchemy.orm import relationship

from data_access.base_model import BaseTable
from modules import db



class Topping(BaseTable):
    """ Ингредиенты"""
    __tablename__ = "toppings"

    name = db.Column(db.Unicode(255), unique=True, index=True, nullable=False, comment='Название')


""" Таблица М-М связи топологий и УС """
topping_food = db.Table(
    'toppings_foods',
    db.Column('id', db.Integer, primary_key=True, unique=True, index=True, nullable=False, autoincrement=True),
    db.Column('topping_id', db.ForeignKey('toppings.id', ondelete='CASCADE'),
              nullable=False, index=True,
              comment='идентификатор Ингредиенты'),
    db.Column('food_id', db.ForeignKey('foods.id', ondelete='CASCADE'),
              nullable=False, index=True,
              comment='идентификатор Блюдо')
)


class Food(BaseTable):
    """ Блюдо"""
    __tablename__ = "foods"

    name = db.Column(db.Unicode(255), unique=True, index=True, nullable=False, comment='Название')
    description = db.Column(db.Unicode(255), index=True, nullable=True, comment='Описание')
    price = db.Column(db.Integer, nullable=False, comment='Цена')
    is_special = db.Column(db.Boolean, nullable=False, comment='Признак "особенный"')
    is_vegan = db.Column(db.Boolean, nullable=False, comment='Признак "для веганов"')
    is_publish = db.Column(db.Boolean, nullable=False, comment='Опубликован')

    category_id = db.Column(db.ForeignKey('food_categories.id', ondelete='CASCADE'), index=True, nullable=True,
                            comment='идентификатор категории')
    category = db.relationship("FoodCategory", primaryjoin="Food.category_id==FoodCategory.id", uselist=False,
                               lazy='joined')

    toppings = relationship('Topping', secondary=topping_food, lazy='joined')


class FoodCategory(BaseTable):
    """ Категория Блюд"""
    __tablename__ = "food_categories"

    name = db.Column(db.Unicode(255), unique=True, index=True, nullable=False, comment='Название')
    is_publish = db.Column(db.Boolean, nullable=False, comment='Опубликован')
