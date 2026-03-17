# test_catalog.py
import pytest
from src.database.models.part import Part

#   ТЕСТЫ КАТАЛОГА
def test_catalog_empty(client):
    """Каталог пуст — должен вернуть пустой список."""
    response = client.get("/api/catalog")
    assert response.status_code == 200
    assert response.json() == []


def test_catalog_with_parts(client, db_session):
    """Каталог с данными — должен вернуть список деталей."""
    part = Part(
        vin="VIN1234567890123",
        brand="BMW",
        model="X5",
        year=2020,
        engine="3.0",
        category="Engine",
        sub_category="Filter",
        part_number="ABC123",
        part_name="Oil Filter",
        oem="OEM123"
    )
    db_session.add(part)
    db_session.commit()

    response = client.get("/api/catalog")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["part_number"] == "ABC123"


def test_catalog_item_found(client, db_session):
    """Поиск детали по номеру — должна быть найдена."""
    part = Part(
        vin="VIN1234567890123",
        brand="BMW",
        model="X5",
        year=2020,
        engine="3.0",
        category="Engine",
        sub_category="Filter",
        part_number="XYZ789",
        part_name="Air Filter",
        oem="OEM999"
    )
    db_session.add(part)
    db_session.commit()

    response = client.get("/api/catalog/XYZ789")
    data = response.json()

    assert response.status_code == 200
    assert data["part_number"] == "XYZ789"
    assert data["brand"] == "BMW"
