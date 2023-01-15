# -*- coding: utf-8 -*-

from loguru import logger as log
import os


# region LOGGING
LOG_PATH = os.getenv('LOG_DIR') or './logs'

info_filter = lambda record: record["level"].name == "INFO" or record["level"].name == "DEBUG"
log.add(LOG_PATH + '/info.log', filter=info_filter, level="DEBUG", rotation="30 MB", retention="10 days",
        backtrace=False, diagnose=False)

error_filter = lambda record: record["level"].name == "ERROR"
log.add(LOG_PATH + '/error.log', filter=error_filter, level="DEBUG", rotation="30 MB", retention="10 days",
        backtrace=False, diagnose=False)

# endregion
