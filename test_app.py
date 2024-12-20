import pytest
from app import app
from models import db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'password',
        'subscription_level': 'basic',
        'account_status': 'active'
    })
    assert response.status_code == 201

def test_login(client):
    client.post('/register', json={
        'username': 'testuser',
        'password': 'password',
        'subscription_level': 'basic',
        'account_status': 'active'
    })
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'password'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
