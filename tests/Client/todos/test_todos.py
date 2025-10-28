from tests.utils.factories import register_user, create_todo

def test_create_todo(client):
    register_user(client)
    todo_id = create_todo(client, title='Buy milk')
    todos = client.get('/api/todos').get_json()['todos']
    assert any(todo['id'] == todo_id for todo in todos)

def test_delete_todo(client):
    register_user(client)
    todo_id = create_todo(client, title='Temp task')
    
    r = client.delete(f'/api/todos/{todo_id}')
    assert r.get_json()['success'] is True
    
    todos = client.get('/api/todos').get_json()['todos']
    assert all(todo['id'] != todo_id for todo in todos)