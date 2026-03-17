# test_vin.py
import pytest
from src.database.deps import get_db
from src.database.models.part import Part


def clean_parts(client):
    """Очищает таблицу Part перед тестом"""
    db_gen = client.app.dependency_overrides[get_db]()
    db = next(db_gen)
    db.query(Part).delete()
    db.commit()
    return db

# 1) НЕКОРРЕКТНАЯ ДЛИНА VIN
def test_vin_invalid_length(client):
    response = client.get("/api/vin/123")
    assert response.status_code == 400

# 2) VIN ЕСТЬ В БАЗЕ
def test_vin_in_database(client):
    db = clean_parts(client)

    vin = "1HGCM82633A004352"  # корректный VIN

    part = Part(
        vin=vin,
        brand="Toyota",
        model="Camry",
        year=2010,
        engine="2.4",
        category="Engine",
        sub_category="Block",
        part_number="P123",
        part_name="Engine Block",
        oem="OEM123"
    )
    db.add(part)
    db.commit()

    response = client.get(f"/api/vin/{vin}")
    assert response.status_code == 200

    data = response.json()
    assert data["make"] == "Toyota"
    assert data["model"] == "Camry"
    assert len(data["parts"]) == 1

# 3) НЕТ API KEY → ТОЛЬКО ЛОКАЛЬНЫЕ ДАННЫЕ
def test_vin_no_api_key(client, monkeypatch):
    db = clean_parts(client)

    monkeypatch.setenv("AUTO_DEV_API_KEY", "")

    vin = "NOAPIKEYVIN12345X"  # 17 символов

    response = client.get(f"/api/vin/{vin}")
    assert response.status_code == 200

    data = response.json()
    assert data["make"] is None
    assert data["parts"] == []

# 4) ВНЕШНИЙ API ВОЗВРАЩАЕТ ДАННЫЕ
def test_vin_external_api(monkeypatch, client):
    db = clean_parts(client)

    monkeypatch.setenv("AUTO_DEV_API_KEY", "TESTKEY")

    async def fake_get(self, url, headers=None):
        class FakeResp:
            status_code = 200
            def json(self):
                return {
                    "make": "Honda",
                    "model": "Civic",
                    "year": 2015,
                    "engine": "1.8"
                }
        return FakeResp()

    monkeypatch.setattr("httpx.AsyncClient.get", fake_get)

    vin = "EXTAPIKEYVIN1234Z"  # 17 символов

    response = client.get(f"/api/vin/{vin}")
    assert response.status_code == 200

    data = response.json()
    assert data["make"] == "Honda"
    assert data["model"] == "Civic"
