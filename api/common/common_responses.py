# -*- coding: utf-8 -*-
from flask_restplus import abort


def response500(message='', log=None):
    if message and log:
        log.error('ERROR 500 сервера: ' + message)

    return abort(500, message)
