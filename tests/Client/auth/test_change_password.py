# tests/auth/test_change_password.py
from tests.utils.factories import register_user

def test_change_password_success(client):
    register_user(client)  # регистрируем и логиним пользователя

    r = client.post('/api/change-password', json={
        'old_password': '123456',
        'new_password': 'newpass123'
    })
    assert r.get_json()['success'] is True

    client.post('/api/logout')
    r = client.post('/api/login', json={'username': 'testuser', 'password': 'newpass123'})
    assert r.get_json()['success'] is True
