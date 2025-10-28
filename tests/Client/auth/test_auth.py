def test_login_success(client):
    client.post('/api/register', json={'username': 'robby1', 'password': '123456'})
    r = client.post('/api/login', json={'username': 'robby1', 'password': '123456'})
    assert r.get_json()['success'] is True