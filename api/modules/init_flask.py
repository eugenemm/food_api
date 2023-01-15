# -*- coding: utf-8 -*-

import os

from flask import Flask, request, abort
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    # app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

    app_settings = os.getenv(
        'API_SETTINGS',
        'modules.config.Development'
    )
    app.config.from_object(app_settings)
    app.logger.disabled = True

    return app




