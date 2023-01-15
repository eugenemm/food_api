# -*- coding: utf-8 -*-
import json
import os

import pytest

def test_ping(app):
    client = app.test_client()
    resp = client.get('/v1/food')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'pong' in data['message']
    assert 'success' in data['status']
