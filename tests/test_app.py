import pytest
import os
import tempfile
from app import app, init_db, DB_PATH

@pytest.fixture
def client():
    db_fd, test_db = tempfile.mkstemp()
    app.config['TESTING'] = True
    global DB_PATH
    DB_PATH = test_db
    init_db()

    with app.test_client() as client:
        with client.session_transaction() as sess:
            pass
        yield client

    os.close(db_fd)
    os.unlink(test_db)

def register(client, username, password):
    return client.post('/api/register', json={'username': username, 'password': password})

def login(client, username, password):
    return client.post('/api/login', json={'username': username, 'password': password})

def change_password(client, old_password, new_password):
    return client.post('/api/change-password', json={'old_password': old_password, 'new_password': new_password})

def create_todo(client, title, description=''):
    return client.post('/api/todos', json={'title': title, 'description': description})

def delete_todo(client, todo_id):
    return client.delete(f'/api/todos/{todo_id}')

# Тест регистрации
def test_register_login(client):
    rv = register(client, 'user1', 'password123')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['success'] is True

    # Повторная регистрация с тем же именем
    rv = register(client, 'user1', 'password123')
    data = rv.get_json()
    assert data['success'] is False

    # Логин с правильными данными
    rv = login(client, 'user1', 'password123')
    data = rv.get_json()
    assert data['success'] is True

    # Логин с неверным паролем
    rv = login(client, 'user1', 'wrongpass')
    data = rv.get_json()
    assert data['success'] is False

# Тест смены пароля
def test_change_password_flow(client):
    register(client, 'user2', 'oldpass123')
    login(client, 'user2', 'oldpass123')

    rv = change_password(client, 'oldpass123', 'newpass456')
    data = rv.get_json()
    assert data['success'] is True

    # Попытка войти со старым паролем
    client.post('/api/logout')
    rv = login(client, 'user2', 'oldpass123')
    data = rv.get_json()
    assert data['success'] is False

    # Вход с новым паролем
    rv = login(client, 'user2', 'newpass456')
    data = rv.get_json()
    assert data['success'] is True

# Тест добавления и удаления Todo
def test_todo_create_delete(client):
    register(client, 'user3', 'testpass')
    login(client, 'user3', 'testpass')

    # Создание Todo
    rv = create_todo(client, 'My Task', 'Task description')
    data = rv.get_json()
    assert data['success'] is True

    # Получаем список Todo, чтобы узнать ID
    rv = client.get('/api/todos')
    data = rv.get_json()
    assert len(data['todos']) == 1
    todo_id = data['todos'][0]['id']

    # Удаление Todo
    rv = delete_todo(client, todo_id)
    data = rv.get_json()
    assert data['success'] is True

    # Проверка, что список пуст
    rv = client.get('/api/todos')
    data = rv.get_json()
    assert len(data['todos']) == 0
