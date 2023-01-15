# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, MetaData, Table, desc, or_, func
from sqlalchemy.orm import sessionmaker, scoped_session
import psycopg2
from flask import current_app
from modules import app


with app.app_context():
    ENGINE = current_app.config.get('SQLALCHEMY_DATABASE_URI')

Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      expire_on_commit=False,
                                      bind=ENGINE))


# Cоединение через psycopg2
def create_simple_connect(params):
    con = None

    try:
        con = psycopg2.connect(**params)
    except Exception:
        print("Unable to connect to the database")

    return con
