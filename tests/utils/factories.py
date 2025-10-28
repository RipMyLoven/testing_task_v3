import uuid

def register_user(client, username=None, password='123456'):
    if username is None:
        username = f"testuser_{uuid.uuid4().hex[:6]}"  # уникальное имя
    r = client.post('/api/register', json={'username': username, 'password': password})
    assert r.get_json()['success'], f"Register failed: {r.get_json()}"

    r = client.post('/api/login', json={'username': username, 'password': password})
    assert r.get_json()['success'], f"Login failed: {r.get_json()}"
    
    return client, username


def create_todo(client, title='Test Task', description=''):
    r = client.post('/api/todos', json={'title': title, 'description': description})
    data = r.get_json()
    assert data['success'], f"Failed to create todo: {data}"
    todos = client.get('/api/todos').get_json()['todos']
    return todos[-1]['id']
