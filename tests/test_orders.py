# test_orders.py

# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def auth_headers(client, email="order@mail.com", password="pass"):
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
    return {"Authorization": f"Bearer {token}"}


def create_test_part(client, part_number="P200", name="Order Product"):
    override = client.app.dependency_overrides
    db_gen = override[list(override.keys())[0]]()
    db = next(db_gen)

    from src.database.models.part import Part

    part = Part(
        part_number=part_number,
        part_name=name,
        price=1500,
        stock=10,
        brand="BrandX",
        model="ModelY",
        category="Engine"
    )
    db.add(part)
    db.commit()
    return part.id


def order_payload(address="Москва, ул. Пушкина, д. 1"):
    return {
        "name": "Иван Иванов",
        "phone": "+79000000000",
        "email": "ivan@example.com",
        "address": address
    }


# БАЗОВЫЕ ТЕСТЫ
def test_create_order(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)

    response = client.post("/orders/create", json=order_payload(), headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "order_id" in data
    assert "user_order_number" in data


def test_get_my_orders(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)
    client.post("/orders/create", json=order_payload(), headers=headers)

    response = client.get("/orders/my", headers=headers)
    assert response.status_code == 200

    orders = response.json()
    assert isinstance(orders, list)
    assert len(orders) >= 1


def test_get_order_by_id(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)
    order = client.post("/orders/create", json=order_payload(), headers=headers).json()
    order_id = order["order_id"]

    response = client.get(f"/orders/{order_id}", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == order_id
    assert "items" in data
    assert isinstance(data["items"], list)


def test_delete_order(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)
    order = client.post("/orders/create", json=order_payload(), headers=headers).json()
    order_id = order["order_id"]

    response = client.delete(f"/orders/{order_id}", headers=headers)
    assert response.status_code == 200

    response = client.get(f"/orders/{order_id}", headers=headers)
    assert response.status_code == 404



# ОШИБКИ
def test_order_empty_cart(client):
    headers = auth_headers(client)

    resp = client.post("/orders/create", json=order_payload(), headers=headers)
    assert resp.status_code == 400


def test_order_no_address(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)

    resp = client.post("/orders/create", json=order_payload(address=""), headers=headers)
    assert resp.status_code == 400


def test_order_missing_name(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)

    resp = client.post("/orders/create", json={
        "phone": "+79000000000",
        "email": "ivan@example.com",
        "address": "Москва"
    }, headers=headers)

    assert resp.status_code == 400



# ПОЛНОЕ ПОКРЫТИЕ УСПЕШНОГО ЗАКАЗА
def test_order_success_full_path(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)
    client.post(f"/cart/add/{part_id}", headers=headers)

    resp = client.post("/orders/create", json=order_payload(), headers=headers)
    assert resp.status_code == 200

    data = resp.json()
    assert "order_id" in data
    assert "user_order_number" in data


def test_order_success_multiple_items(client):
    headers = auth_headers(client)
    part1 = create_test_part(client, part_number="P201")
    part2 = create_test_part(client, part_number="P202")

    client.post(f"/cart/add/{part1}", headers=headers)
    client.post(f"/cart/add/{part2}", headers=headers)

    resp = client.post("/orders/create", json=order_payload(), headers=headers)
    assert resp.status_code == 200

    data = resp.json()
    assert "order_id" in data
    assert "user_order_number" in data
