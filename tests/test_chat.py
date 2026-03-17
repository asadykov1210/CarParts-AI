# test_chat.py
import pytest

# 1) ПУСТОЕ СООБЩЕНИЕ
def test_chat_empty_message(client):
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 400


# 2) ТРИГГЕР НА МЕНЕДЖЕРА
@pytest.mark.parametrize("text", [
    "Позвать менеджера",
    "Мне нужен менеджер",
    "Хочу поговорить с менеджером",
    "оператор",
    "живой человек"
])
def test_chat_manager_trigger(client, text):
    response = client.post("/chat", json={"message": text})
    assert response.status_code == 200
    assert response.json()["reply"] == "Ваш менеджер свяжется с вами в ближайшее время"


# 3) VIN В СООБЩЕНИИ
def test_chat_with_vin(monkeypatch, client):
    # Если сообщение содержит VIN — должен вызываться VIN‑поиск.
    async def fake_get(self, url):
        class FakeResp:
            status_code = 200
            def json(self):
                return {"make": "Toyota", "model": "Camry"}
        return FakeResp()

    monkeypatch.setattr("httpx.AsyncClient.get", fake_get)

    # Мокаем вызов Mistral
    def fake_mistral(messages):
        return {"choices": [{"message": {"content": "Ответ VIN"}}]}

    monkeypatch.setattr("main.call_mistral", fake_mistral)

    response = client.post("/chat", json={"message": "Пробей VIN JTDBE32K123456789"})
    assert response.status_code == 200
    assert response.json()["reply"] == "Ответ VIN"


# 4) PART NUMBER В СООБЩЕНИИ
def test_chat_with_part(monkeypatch, client):
    async def fake_get(self, url):
        class FakeResp:
            status_code = 200
            def json(self):
                return {"id": 1, "name": "Test Part"}
        return FakeResp()

    monkeypatch.setattr("httpx.AsyncClient.get", fake_get)

    def fake_mistral(messages):
        return {"choices": [{"message": {"content": "Ответ PART"}}]}

    monkeypatch.setattr("main.call_mistral", fake_mistral)

    response = client.post("/chat", json={"message": "Найди A12345"})
    assert response.status_code == 200
    assert response.json()["reply"] == "Ответ PART"


# 5) ОБЫЧНОЕ СООБЩЕНИЕ в MISTRAL
def test_chat_normal_message(monkeypatch, client):
    def fake_mistral(messages):
        return {"choices": [{"message": {"content": "Привет!"}}]}

    monkeypatch.setattr("main.call_mistral", fake_mistral)

    response = client.post("/chat", json={"message": "Привет"} )
    assert response.status_code == 200
    assert response.json()["reply"] == "Привет!"
