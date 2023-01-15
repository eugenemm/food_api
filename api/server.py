# -*- coding: utf-8 -*-

from modules import app, api, config


if __name__ == '__main__':

    api.init_app(app)
    app.run(**config.api_server)

