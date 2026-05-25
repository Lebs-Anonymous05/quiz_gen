import pytest
from app import create_app, db
from app.models.user import User


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app("testing")
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def auth_token(client):
    """Register and login a test user, return JWT token."""
    # Register
    client.post("/api/auth/register", json={
        "full_name": "Test User",
        "email": "test@test.com",
        "password": "test1234",
        "role": "student"
    })

    # Login
    res = client.post("/api/auth/login", json={
        "email": "test@test.com",
        "password": "test1234"
    })
    return res.get_json()["token"]


@pytest.fixture
def auth_headers(auth_token):
    """Return auth headers with JWT token."""
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }