# test_cart.py

# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def auth_headers(client, email="cart@mail.com", password="pass"):
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


def create_test_part(client, part_number="P100", name="Test Product"):
    override = client.app.dependency_overrides
    db_gen = override[list(override.keys())[0]]()
    db = next(db_gen)

    from src.database.models.part import Part

    part = Part(
        part_number=part_number,
        part_name=name,
        price=1000,
        stock=5,
        brand="BrandX",
        model="ModelY",
        category="Engine"
    )
    db.add(part)
    db.commit()
    return part.id


# БАЗОВЫЕ ТЕСТЫ
def test_cart_empty(client):
    headers = auth_headers(client)
    response = client.get("/cart/my", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_cart_add_item(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    response = client.post(f"/cart/add/{part_id}", headers=headers)
    assert response.status_code == 200

    cart = client.get("/cart/my", headers=headers).json()
    assert len(cart) == 1
    assert cart[0]["product"]["id"] == part_id
    assert cart[0]["quantity"] == 1


def test_cart_add_nonexistent_product(client):
    headers = auth_headers(client)
    resp = client.post("/cart/add/99999", headers=headers)
    assert resp.status_code == 404


def test_cart_remove_item(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)
    item_id = client.get("/cart/my", headers=headers).json()[0]["id"]

    resp = client.post(f"/cart/remove/{item_id}", headers=headers)
    assert resp.status_code == 200

    assert client.get("/cart/my", headers=headers).json() == []


def test_cart_remove_nonexistent_item(client):
    headers = auth_headers(client)
    resp = client.post("/cart/remove/99999", headers=headers)
    assert resp.status_code == 404


def test_cart_remove_other_user_item(client):
    headers1 = auth_headers(client, email="u1@mail.com")
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers1)
    item_id = client.get("/cart/my", headers=headers1).json()[0]["id"]

    headers2 = auth_headers(client, email="u2@mail.com")

    resp = client.post(f"/cart/remove/{item_id}", headers=headers2)
    assert resp.status_code == 404


def test_cart_clear(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)
    client.post(f"/cart/add/{part_id}", headers=headers)

    resp = client.delete("/cart/clear", headers=headers)
    assert resp.status_code == 200

    assert client.get("/cart/my", headers=headers).json() == []


def test_cart_clear_empty(client):
    headers = auth_headers(client)
    resp = client.delete("/cart/clear", headers=headers)
    assert resp.status_code == 200


# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ
def test_old_cart_route(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)

    resp = client.get("/cart", headers=headers)
    assert resp.status_code == 200
    data = resp.json()

    assert len(data) == 1
    assert data[0]["product"]["id"] == part_id


def test_old_cart_skip_missing_product(client):
    headers = auth_headers(client)

    override = client.app.dependency_overrides
    db = next(override[list(override.keys())[0]]())

    from src.database.models.cart_item import CartItem

    bad_item = CartItem(user_id=1, product_id=99999, quantity=1)
    db.add(bad_item)
    db.commit()

    resp = client.get("/cart", headers=headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_cart_remove_decrease_quantity_exact(client):
    headers = auth_headers(client, email="branch@mail.com")
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers)
    client.post(f"/cart/add/{part_id}", headers=headers)
    client.post(f"/cart/add/{part_id}", headers=headers)

    cart = client.get("/cart/my", headers=headers).json()
    item_id = cart[0]["id"]
    assert cart[0]["quantity"] == 3

    resp = client.post(f"/cart/remove/{item_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["quantity"] == 2

def test_cart_remove_quantity_branch(client):
    # создаём уникального пользователя
    headers = auth_headers(client, email="branch_unique@mail.com")

    # создаём деталь
    part_id = create_test_part(client, part_number="BRANCH1")

    # добавляем 2 раза — quantity станет 2
    client.post(f"/cart/add/{part_id}", headers=headers)
    client.post(f"/cart/add/{part_id}", headers=headers)

    # получаем item_id
    cart = client.get("/cart/my", headers=headers).json()
    assert len(cart) == 1
    item_id = cart[0]["id"]
    assert cart[0]["quantity"] == 2  # гарантируем >1

    # удаляем 1 штуку → ДОЛЖНА выполниться строка 51
    resp = client.post(f"/cart/remove/{item_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["quantity"] == 1
