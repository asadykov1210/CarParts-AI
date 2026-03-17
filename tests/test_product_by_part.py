# test_product_by_part.py
import pytest
from src.database.deps import get_db
from src.database.models.part import Part


# 1) Есть Part с таким part_number
def test_product_by_part_found(client):
    db_gen = client.app.dependency_overrides[get_db]()
    db = next(db_gen)

    part = Part(
        vin="1HGCM82633A004352",
        brand="Honda",
        model="Accord",
        year=2003,
        engine="2.4",
        category="Engine",
        sub_category="Filter",
        part_number="OF123",
        part_name="Oil Filter",
        oem="OEM123",
        price=500,
        stock=10,
    )
    db.add(part)
    db.commit()

    response = client.get("/api/product/by-part/OF123")
    assert response.status_code == 200

    data = response.json()
    assert data["source"] == "part"
    assert data["id"] == part.id
    assert data["part_number"] == "OF123"
    assert data["brand"] == "Honda"


# 2) Нет Part
def test_product_by_part_not_found(client):
    response = client.get("/api/product/by-part/NOTFOUND123")
    assert response.status_code == 404
    assert response.json()["detail"] == "Деталь не найдена"
