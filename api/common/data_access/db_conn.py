import multiprocessing
import multiprocessing.pool

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import psycopg2
from functools import wraps
from modules import config


def timer_request(max_timeout=10):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator


class CreateSessionContext:

    def __init__(self, engine=None):
        data_base_uri = config.local_base + config.database_name
        self.engine = engine if engine else data_base_uri
        self.engine_local = self.Session_local = self.session = None

    def __enter__(self):
        self.engine_local = create_engine(self.engine, echo=False, pool_size=1, max_overflow=0)
        session_factory = sessionmaker(autocommit=False,
                                       autoflush=False,
                                       expire_on_commit=False,
                                       bind=self.engine_local)
        self.Session_local = scoped_session(session_factory)
        self.session = self.Session_local()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Session_local.remove()
        self.engine_local.dispose()


class CreateConnection:
    def __init__(self, engine=None):
        data_base_uri = config.local_base + config.database_name
        self.engine = engine if engine else data_base_uri
        self.engine_local = self.connection = None

    def __enter__(self):
        self.engine_local = create_engine(self.engine, echo=True)
        self.connection = self.engine_local.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        self.engine_local.dispose()


def getEngine():
    return create_engine(config.local_base, echo=False)


# Cоединение через psycopg2
def create_simple_connect(params):
    con = None

    try:
        con = psycopg2.connect(**params)
    except Exception:
        print("I am unable to connect to the database")

    return con
