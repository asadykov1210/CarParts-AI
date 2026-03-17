# test_reviews.py


# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def auth_headers(client, email="review@mail.com", password="pass"):
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


def create_test_part(client, part_number="R100", name="Review Product"):
    override = client.app.dependency_overrides
    db_gen = override[list(override.keys())[0]]()
    db = next(db_gen)

    from src.database.models.part import Part

    part = Part(
        part_number=part_number,
        part_name=name,
        price=500,
        stock=10,
        brand="BrandX",
        model="ModelY",
        category="Engine"
    )
    db.add(part)
    db.commit()
    return part.id


def order_payload():
    return {
        "name": "Иван",
        "phone": "+79000000000",
        "email": "ivan@example.com",
        "address": "Москва"
    }

# ОТЗЫВЫ — ОШИБКИ
def test_review_product_not_found(client):
    headers = auth_headers(client)
    resp = client.post("/reviews/", json={
        "product_id": 99999,
        "rating": 5,
        "comment": "Test"
    }, headers=headers)
    assert resp.status_code == 404


def test_review_without_purchase(client):
    headers = auth_headers(client)
    part_id = create_test_part(client)

    resp = client.post("/reviews/", json={
        "product_id": part_id,
        "rating": 5,
        "comment": "Test"
    }, headers=headers)

    assert resp.status_code == 400


def test_delete_review_not_found(client):
    headers = auth_headers(client)
    resp = client.delete("/reviews/99999", headers=headers)
    assert resp.status_code == 404


def test_delete_review_forbidden(client):
    headers1 = auth_headers(client, email="u1@mail.com")
    part_id = create_test_part(client)

    client.post(f"/cart/add/{part_id}", headers=headers1)
    client.post("/orders/create", json=order_payload(), headers=headers1)

    review = client.post("/reviews/", json={
        "product_id": part_id,
        "rating": 4,
        "comment": "ok"
    }, headers=headers1).json()

    headers2 = auth_headers(client, email="u2@mail.com")

    resp = client.delete(f"/reviews/{review['id']}", headers=headers2)
    assert resp.status_code == 403

# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ
def test_get_reviews_empty(client):
    part_id = create_test_part(client)
    resp = client.get(f"/reviews/product/{part_id}")
    assert resp.status_code == 200
    assert resp.json() == []


def test_delete_review_admin(client):
    # user
    headers_user = auth_headers(client, email="revadmin@mail.com")
    part_id = create_test_part(client)

    # покупка
    client.post(f"/cart/add/{part_id}", headers=headers_user)
    client.post("/orders/create", json={
        "name": "A",
        "phone": "1",
        "email": "a@a",
        "address": "x"
    }, headers=headers_user)

    # отзыв
    review = client.post("/reviews/", json={
        "product_id": part_id,
        "rating": 5,
        "comment": "ok"
    }, headers=headers_user).json()

    # admin
    headers_admin = auth_headers(client, email="adminrev@mail.com")

    # делаем админом
    override = client.app.dependency_overrides
    db = next(override[list(override.keys())[0]]())
    from src.database.models.user import User
    admin = db.query(User).filter(User.email == "adminrev@mail.com").first()
    admin.role = "admin"
    db.commit()

    resp = client.delete(f"/reviews/{review['id']}", headers=headers_admin)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Отзыв удалён"
