# -*- coding: utf-8 -*-

import requests as r


def post_request(token: str, url: str, json):
    _token = token if token else ''
    headers = {'Authorization': 'Bearer ' + _token, 'Content-Type': 'application/json'}
    return r.post(url, headers=headers, json=json)


def get_request(token: str, url: str, params=None):
    _token = token if token else ''
    headers = {'Authorization': 'Bearer ' + _token, 'Content-Type': 'application/json'}
    return r.get(url, headers=headers, params=params)
