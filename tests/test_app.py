import os
import tempfile
import json
import pytest

# Lihtne pytest seadistus Flask test kliendiga

os.environ['DB_PATH'] = ''  # tagab, et allpool seatakse enne importi

import importlib


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Loob eraldi ajutise andmebaasi ja Flask test kliendi"""
    db_file = tmp_path / 'test.db'
    monkeypatch.setenv('DB_PATH', str(db_file))
    # Impordime appi iga testiga puhtalt
    app_module = importlib.import_module('app')
    importlib.reload(app_module)
    app = app_module.app
    app_module.init_db()
    app.testing = True
    with app.test_client() as c:
        yield c


def register(client, username, password):
    return client.post('/api/register', json={'username': username, 'password': password})


def login(client, username, password):
    return client.post('/api/login', json={'username': username, 'password': password})


def test_login_flow(client):
    """Testib sisselogimise voogu"""
    # registreerime
    r = register(client, 'maria', 'salasona')
    assert r.is_json and r.json['success'] is True

    # vale parool
    r = login(client, 'maria', 'vale')
    assert r.is_json and r.json['success'] is False

    # õige parool
    r = login(client, 'maria', 'salasona')
    assert r.is_json and r.json['success'] is True


def test_create_todo(client):
    """Testib ülesande lisamist"""
    # kasutaja
    assert register(client, 'jaan', 'parool1').json['success'] is True
    assert login(client, 'jaan', 'parool1').json['success'] is True

    # lisame ülesande
    payload = {
        'title': 'Osta piim',
        'description': '2L täispiima',
        'priority': 'high',
        'due_date': '2025-12-31',
        'tags': 'Kodu,Pood'
    }
    r = client.post('/api/todos', json=payload)
    assert r.is_json and r.json['success'] is True

    # kontrollime, et ülesanne on nimekirjas
    r = client.get('/api/todos')
    assert r.is_json and r.json['success'] is True
    items = r.json['todos']
    assert len(items) == 1
    item = items[0]
    assert item['title'] == 'Osta piim'
    assert item['priority'] == 'high'
    assert item['due_date'] == '2025-12-31'
    assert 'Kodu' in (item.get('tags') or '')

