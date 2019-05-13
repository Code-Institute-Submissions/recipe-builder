import os 
import tempfile

import pytest

import app as app_module

app = app_mudule.app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()
    
    with app.app_context():
        init_db()
        
    yield client
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])