# -*- coding: utf-8 -*-

import eventlet
eventlet.monkey_patch()


from modules import app, api, config


api.init_app(app)
config.api_server['debug'] = False

