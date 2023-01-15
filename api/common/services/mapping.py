# -*- coding: utf-8 -*-
from marshmallow import EXCLUDE

from marshmallow_sqlalchemy import ModelConversionError, ModelSchema

# region фабрики классов для схем marsmallow вида:

# class StaffSchema(ma.ModelSchema):
#     class Meta:
#         model = models.Staff
#
# class StaffSchemaPut(StaffSchema):
#     class Meta:
#         exclude = EXCLUDED_FIELDS
#
# class StaffSchemaPost(StaffSchema):
#     class Meta:
#         exclude = EXCLUDED_FIELDS + ['id']
#
# class StaffListSchema(ma.Schema):
#     totalCount = fields.Integer()
#     data = fields.List(fields.Nested(StaffSchema()))


def flat_main_schema_fabric(class_name, db_model):
    return type(class_name,
                (ModelSchema,),
                {"Meta":
                     type('Meta', (), {
                         "model": db_model,
                         "transient": True})})


def flat_main_schema_fabric_dt(class_name, db_model, converter):
    return type(class_name,
                (ModelSchema,),
                {"Meta":
                     type('Meta', (), {
                         "model": db_model,
                         "model_converter": converter,
                         "transient": True})})


def slave_schemas_fabric(main_schema, db_model, excluded=None):
    excluded_ = excluded or []
    main_schema_name = type(main_schema()).__name__
    PutSchema = type(main_schema_name + 'Put',
                     (main_schema,),
                     {"Meta":
                          type('Meta', (),
                               {"model": db_model,
                                "exclude": excluded_,
                                "unknown": EXCLUDE,
                                "transient": True})})
    PostSchema = type(main_schema_name + 'Post',
                      (main_schema,),
                      {"Meta":
                           type('Meta', (),
                                {"model": db_model,
                                 "exclude": ['id'] + excluded_,
                                 "unknown": EXCLUDE,
                                 "transient": True})})
    # ListSchema = type(main_schema_name + 'List',
    #                   (ma.Schema,), {"totalCount": fields.Integer(),
    #                                  "data": fields.List(fields.Nested(main_schema()))})
    #
    ListSchema = main_schema(many=True)


    return PutSchema, PostSchema, ListSchema
# endregion
