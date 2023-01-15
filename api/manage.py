# -*- coding: utf-8 -*-

import unittest
# import coverage

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import subprocess
from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from modules import app, db
from modules import config


migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def create_db_tables():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db_tables():
    """Drops the db tables."""
    db.drop_all()

@manager.command
def create_database():
    con = connect(dbname='postgres',
                  host=config.db_params.get('host'),
                  port=config.db_params.get('port'),
                  user=config.db_params.get('user'),
                  password=config.db_params.get('password'))

    dbname = config.database_name

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('CREATE DATABASE "' + dbname + '"')
    cur.close()
    con.close()

    # con = connect(dbname=dbname,
    #               host=config.db_params.get('host'),
    #               port=config.db_params.get('port'),
    #               user=config.db_params.get('user'),
    #               password=config.db_params.get('passw'))
    #
    # con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # cur = con.cursor()
    # cur.execute('CREATE EXTENSION postgis SCHEMA public;')
    # cur.close()
    # con.close()

@manager.command
def drop_database():
    con = connect(dbname='postgres',
                  host=config.db_params.get('host'),
                  port=config.db_params.get('port'),
                  user=config.db_params.get('user'),
                  password=config.db_params.get('password'))

    dbname = config.database_name

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('DROP DATABASE "' + dbname + '"')
    cur.close()
    con.close()


@manager.command
def update_database():
    print("Start alembic upgrade")
    stat_code = subprocess.call("python manage.py db upgrade", shell=True)
    if stat_code != 0:
        sys.exit("Alembic return non-zero code")
    print("Finished alembic upgrade")


@manager.command
def seed_all():
    import json

    with open('seed.json') as json_file:
        data = json.load(json_file)

        pass


@manager.command
def recreate_db():
    drop_database()
    create_database()
    update_database()
    seed_all()


if __name__ == '__main__':

    manager.run()
