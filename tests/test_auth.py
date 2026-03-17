# test_auth.py

from src.database.models.user import User


# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def register_and_login(client, email="test@mail.com", password="pass"):
    client.post("/auth/register", json={
        "email": email,
        "name": "User",
        "password": password
    })

    login = client.post("/auth/login", json={
        "email": email,
        "password": password
    })

    token = login.json()["access_token"]
    return token


# REGISTER
def test_register_success(client):
    resp = client.post("/auth/register", json={
        "email": "reg@mail.com",
        "name": "Артём",
        "password": "123456"
    })
    assert resp.status_code == 200
    assert resp.json()["email"] == "reg@mail.com"


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "email": "dup@mail.com",
        "name": "User",
        "password": "pass"
    })

    resp = client.post("/auth/register", json={
        "email": "dup@mail.com",
        "name": "User2",
        "password": "pass2"
    })

    assert resp.status_code == 400
    assert resp.json()["detail"] == "Пользователь с таким email уже существует"


def test_register_empty_fields(client):
    resp = client.post("/auth/register", json={
        "email": "",
        "name": "",
        "password": ""
    })
    assert resp.status_code == 200


# LOGIN
def test_login_success(client):
    token = register_and_login(client, "login@mail.com", "pass")
    assert token is not None


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "wrong@mail.com",
        "name": "User",
        "password": "correct"
    })

    resp = client.post("/auth/login", json={
        "email": "wrong@mail.com",
        "password": "incorrect"
    })

    assert resp.status_code == 401


def test_login_nonexistent_user(client):
    resp = client.post("/auth/login", json={
        "email": "nouser@mail.com",
        "password": "1234"
    })
    assert resp.status_code == 401


def test_login_empty_fields(client):
    resp = client.post("/auth/login", json={
        "email": "",
        "password": ""
    })
    assert resp.status_code == 200
    assert resp.json()["access_token"] is None


# GET /auth/me
def test_get_me_success(client):
    token = register_and_login(client, "me@mail.com", "pass")

    resp = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })

    assert resp.status_code == 200
    assert resp.json()["email"] == "me@mail.com"


def test_get_me_no_header(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Отсутствует заголовок Authorization"


def test_get_me_invalid_header_format(client):
    token = register_and_login(client)

    resp = client.get("/auth/me", headers={
        "Authorization": f"Token {token}"
    })

    assert resp.status_code == 401
    assert resp.json()["detail"] == "Неверный формат токена"


def test_get_me_invalid_token(client):
    resp = client.get("/auth/me", headers={
        "Authorization": "Bearer WRONGTOKEN"
    })
    assert resp.status_code == 401


def test_get_me_user_not_found(client):
    token = register_and_login(client, "ghost@mail.com")

    # удаляем пользователя вручную
    override = client.app.dependency_overrides
    db_gen = override[list(override.keys())[0]]()
    db = next(db_gen)

    user = db.query(User).filter(User.email == "ghost@mail.com").first()
    db.delete(user)
    db.commit()

    resp = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })

    assert resp.status_code == 404
    assert resp.json()["detail"] == "Пользователь не найден"


# UPDATE PROFILE
def test_update_profile_success(client):
    token = register_and_login(client, "upd@mail.com", "pass")

    resp = client.put("/auth/update", json={
        "name": "New Name",
        "phone": "+79000000000",
        "city": "Москва",
        "country": "Россия",
        "password": "newpass"
    }, headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "New Name"
    assert data["phone"] == "+79000000000"
    assert data["city"] == "Москва"
    assert data["country"] == "Россия"


def test_update_profile_empty_fields(client):
    token = register_and_login(client, "upd2@mail.com", "pass")

    resp = client.put("/auth/update", json={
        "name": "",
        "phone": None,
        "city": None,
        "country": None,
        "password": None
    }, headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    assert resp.json()["name"] == ""


def test_update_profile_only_password(client):
    token = register_and_login(client, "upd3@mail.com", "pass")

    resp = client.put("/auth/update", json={
        "name": "User",
        "password": "newpass"
    }, headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200


def test_update_profile_no_changes(client):
    token = register_and_login(client, "upd4@mail.com", "pass")

    resp = client.put("/auth/update", json={
        "name": "User"
    }, headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
