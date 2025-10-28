# tests/conftest.py
import os
import tempfile
import pytest
import importlib

@pytest.fixture
def client():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    os.environ['DB_PATH'] = path

    import app as app_module
    importlib.reload(app_module)
    app_module.init_db()
    app = app_module.app
    app.testing = True

    with app.test_client() as client:
        yield client

    os.remove(path)
