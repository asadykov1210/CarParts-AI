# test_admin.py

from src.database.deps import get_db
from src.database.models.user import User


# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def admin_headers(client, email="admin@mail.com"):
    """Создаём админа и получаем токен"""
    client.post("/auth/register", json={
        "email": email,
        "name": "Admin",
        "password": "pass"
    })

    # Достаём тестовую БД из dependency_overrides
    override = client.app.dependency_overrides
    db_gen = override[list(override.keys())[0]]()
    db = next(db_gen)

# Повышаем роль до admin
    admin = db.query(User).filter(User.email == email).first()
    admin.role = "admin"
    db.commit()

    # Логинимся и получаем токен
    login = client.post("/auth/login", json={
        "email": email,
        "password": "pass"
    })

    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# part_to_dict(None)
def test_part_to_dict_none():
    from src.admin.admin_routes import part_to_dict
    assert part_to_dict(None) == {}

# CREATE PRODUCT
def test_create_product(client):
    headers = admin_headers(client)

    response = client.post("/admin/products", json={
        "part_number": "A100",
        "part_name": "Test Product",
        "price": 5000,
        "stock": 10,
        "brand": "BrandX",
        "model": "ModelY",
        "category": "Engine"
    }, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["part_number"] == "A100"

# GET ALL PRODUCTS
def test_get_all_products(client):
    headers = admin_headers(client)

    client.post("/admin/products", json={
        "part_number": "A200",
        "part_name": "Another Product",
        "price": 3000,
        "stock": 5,
        "brand": "BrandX",
        "model": "ModelY",
        "category": "Engine"
    }, headers=headers)

    response = client.get("/admin/products", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# GET PRODUCT BY ID
def test_get_product_by_id(client):
    headers = admin_headers(client)

    created = client.post("/admin/products", json={
        "part_number": "A300",
        "part_name": "Single Product",
        "price": 1000,
        "stock": 3,
        "brand": "BrandX",
        "model": "ModelY",
        "category": "Engine"
    }, headers=headers).json()

    product_id = created["id"]

    response = client.get(f"/admin/products/{product_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == product_id

# UPDATE PRODUCT
def test_update_product(client):
    headers = admin_headers(client)

    created = client.post("/admin/products", json={
        "part_number": "A400",
        "part_name": "Old Name",
        "price": 2000,
        "stock": 2,
        "brand": "BrandX",
        "model": "ModelY",
        "category": "Engine"
    }, headers=headers).json()

    product_id = created["id"]

    response = client.put(f"/admin/products/{product_id}", json={
        "part_name": "New Name",
        "price": 2500
    }, headers=headers)

    assert response.status_code == 200
    assert response.json()["part_name"] == "New Name"

# UPDATE NOT FOUND
def test_admin_update_not_found(client):
    headers = admin_headers(client)
    resp = client.put("/admin/products/99999", json={"part_name": "X"}, headers=headers)
    assert resp.status_code == 404

# DELETE PRODUCT
def test_delete_product(client):
    headers = admin_headers(client)

    created = client.post("/admin/products", json={
        "part_number": "A500",
        "part_name": "To Delete",
        "price": 1500,
        "stock": 1,
        "brand": "BrandX",
        "model": "ModelY",
        "category": "Engine"
    }, headers=headers).json()

    product_id = created["id"]

    response = client.delete(f"/admin/products/{product_id}", headers=headers)
    assert response.status_code == 200

    response = client.get(f"/admin/products/{product_id}", headers=headers)
    assert response.status_code == 404

# DELETE NOT FOUND
def test_admin_delete_not_found(client):
    headers = admin_headers(client)
    resp = client.delete("/admin/products/99999", headers=headers)
    assert resp.status_code == 404

# GET LOGS
def test_admin_get_logs(client):
    headers = admin_headers(client)
    resp = client.get("/admin/logs", headers=headers)
    assert resp.status_code == 200

# GET LOG BY ID
def test_admin_get_log_by_id(client):
    headers = admin_headers(client)

    client.post("/admin/products", json={
        "part_number": "LOG1",
        "part_name": "Log Test",
        "price": 100,
        "stock": 1
    }, headers=headers)

    logs = client.get("/admin/logs", headers=headers).json()
    log_id = logs[0]["id"]

    resp = client.get(f"/admin/logs/{log_id}", headers=headers)
    assert resp.status_code == 200

# GET LOG NOT FOUND
def test_get_log_not_found(client):
    headers = admin_headers(client)
    resp = client.get("/admin/logs/99999", headers=headers)
    assert resp.status_code == 404

# DELETE LOG
def test_admin_delete_log(client):
    headers = admin_headers(client)

    client.post("/admin/products", json={
        "part_number": "LOG2",
        "part_name": "Log Test 2",
        "price": 100,
        "stock": 1
    }, headers=headers)

    logs = client.get("/admin/logs", headers=headers).json()
    log_id = logs[0]["id"]

    resp = client.delete(f"/admin/logs/{log_id}", headers=headers)
    assert resp.status_code == 200

# DELETE LOG NOT FOUND
def test_delete_log_not_found(client):
    headers = admin_headers(client)
    resp = client.delete("/admin/logs/99999", headers=headers)
    assert resp.status_code == 404

# MANAGER REQUESTS
def test_manager_requests(client):
    headers = admin_headers(client)
    resp = client.get("/admin/manager-requests", headers=headers)
    assert resp.status_code == 200

# MANAGER REQUESTS INVALID JSON
def test_manager_requests_invalid_json(client):
    headers = admin_headers(client)

    override = client.app.dependency_overrides
    db_gen = override[list(override.keys())[0]]()
    db = next(db_gen)

    from src.database.models.admin_log import AdminLog
    from datetime import datetime

    bad_log = AdminLog(
        action="REQUEST_MANAGER",
        product_id=None,
        before=None,
        after="NOT_JSON",
        created_at=datetime.utcnow()
    )
    db.add(bad_log)
    db.commit()

    resp = client.get("/admin/manager-requests", headers=headers)
    assert resp.status_code == 200
