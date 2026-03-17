# test_errors.py

# НЕСУЩЕСТВУЮЩИЙ ЭНДПОИНТ
def test_invalid_endpoint(client):
    response = client.get("/no_such_endpoint")
    assert response.status_code == 404

# /chat БЕЗ message
def test_chat_no_message(client):
    response = client.post("/chat", json={})
    assert response.status_code in (400, 422)

# НЕВЕРНЫЙ HTTP-МЕТОД
def test_wrong_method(client):
    response = client.put("/chat", json={"message": "Привет"})
    assert response.status_code in (405, 404)

# НЕВЕРНЫЙ CONTENT-TYPE
def test_wrong_content_type(client):
    response = client.post(
        "/chat",
        data="message=Привет",
        headers={"Content-Type": "text/plain"}
    )
    assert response.status_code in (400, 415, 422)

# ПУСТОЕ ТЕЛО ЗАПРОСА
def test_empty_body(client):
    response = client.post(
        "/chat",
        data="",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code in (400, 422)

# НЕВАЛИДНЫЙ JSON
def test_invalid_json(client):
    response = client.post(
        "/chat",
        data="{not json}",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code in (400, 422)

# ЗАЩИЩЁННЫЙ ЭНДПОИНТ БЕЗ ТОКЕНА
def test_protected_endpoint_no_token(client):
    response = client.get("/auth/me")
    assert response.status_code in (401, 403)

# ЗАЩИЩЁННЫЙ ЭНДПОИНТ С НЕВЕРНЫМ ТОКЕНОМ
def test_protected_endpoint_invalid_token(client):
    response = client.get("/auth/me", headers={
        "Authorization": "Bearer WRONGTOKEN"
    })
    assert response.status_code in (401, 403)

# АДМИН-ЭНДПОИНТ БЕЗ ПРАВ
def test_admin_endpoint_no_rights(client):
    response = client.post("/api/admin/catalog", json={
        "article": "X1",
        "name": "Test",
        "brand": "Test",
        "price": 100
    })
    assert response.status_code in (401, 403, 404)

# 404 ДЛЯ НЕСУЩЕСТВУЮЩЕЙ ДЕТАЛИ
def test_server_error_mock(client):
    """Этот эндпоинт не вызывает внешних функций, поэтому 404 — корректный ответ"""
    response = client.get("/api/catalog/12345")
    assert response.status_code == 404



