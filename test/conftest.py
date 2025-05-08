import pytest
from fastapi.testclient import TestClient
import model
from database import get_db
from main import app
from .database import SessionLocal, engine
from oauth2 import create_access_token


@pytest.fixture(scope="function")
def session():
    model.Base.metadata.drop_all(bind=engine)
    model.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture(scope="function")
def test_user(client):
    create_data = {
    "nickname": "Kacper",
    "email": "Kacper@gmail.com",
    "password": "haslo123"
}

    response = client.post("/user/register", json=create_data
)
    user = response.json()
    assert response.status_code == 201
    user['email'] = create_data['email']
    user['password'] = create_data['password']
    return user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def simple_user(client):
    response = client.post("/users/", json={
        "username": "Basia",
        "email": "Basia@gmail.com",
        "password": "haslo123"
    })
    assert response.status_code == 201
    yield response.json()

@pytest.fixture
def create_posts(session, test_user, simple_user):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        }, {
            "title": "4rd title",
            "content": "4rd content",
            "owner_id": simple_user['id']
        }]

    def convert_data_to_post(post):
        return Post(**post)

    posts = map(convert_data_to_post, posts_data)
    posts = list(posts)
    session.add_all(posts)
    session.commit()

    return posts






