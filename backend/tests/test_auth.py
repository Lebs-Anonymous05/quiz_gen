def test_register_success(client):
    res = client.post("/api/auth/register", json={
        "full_name": "Hopkins Bah",
        "email": "test@test.com",
        "password": "test1234",
        "role": "student"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "user" in data
    assert data["user"]["email"] == "test@test.com"


def test_register_duplicate_email(client):
    payload = {
        "full_name": "Hopkins Bah",
        "email": "dup@test.com",
        "password": "secure123",
        "role": "student"
    }
    client.post("/api/auth/register", json=payload)
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 409


def test_login_success(client):
    client.post("/api/auth/register", json={
        "full_name": "Hopkins Bah",
        "email": "login@test.com",
        "password": "secure123",
        "role": "student"
    })
    res = client.post("/api/auth/login", json={
        "email": "login@test.com",
        "password": "secure123"
    })
    assert res.status_code == 200
    assert "token" in res.get_json()


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "full_name": "Hopkins Bah",
        "email": "wrong@test.com",
        "password": "correct123",
        "role": "student"
    })
    res = client.post("/api/auth/login", json={
        "email": "wrong@test.com",
        "password": "wrongpass"
    })
    assert res.status_code == 401