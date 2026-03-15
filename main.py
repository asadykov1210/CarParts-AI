from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import re
import json
import requests
import httpx
from dotenv import load_dotenv
from datetime import datetime

# Загружаем конфиг из .env — ключи для API храним отдельно от кода.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
AUTO_DEV_API_KEY = os.getenv("AUTO_DEV_API_KEY")

MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"


# Инициализация FastAPI-приложения.
app = FastAPI()

#Middleware для замера времени всех запросов
import time
from fastapi import Request

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"Request took {duration:.3f} seconds | {request.url.path}")
    return response

# Подключаем базу и модели.
from src.database.db import init_db
from src.database.models.part import Part
from src.database.models.admin_log import AdminLog
from src.database.deps import get_db

init_db()

# Разрешаем фронтенду ходить к API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Простые обработчики ошибок, чтобы не падать на кривом JSON.
@app.exception_handler(json.JSONDecodeError)
async def json_decode_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid JSON"},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


# Подключаем модули: авторизация, корзина, заказы, отзывы.
from src.auth.routes import router as auth_router
app.include_router(auth_router, prefix="/auth")

from src.cart.cart_routes import router as cart_router
app.include_router(cart_router)

from src.orders.order_routes import router as orders_router
app.include_router(orders_router, prefix="/orders")

from src.reviews.review_routes import router as reviews_router
app.include_router(reviews_router)

# WebSocket для админов — сюда приходят запросы менеджеру.
admin_ws_connections: set[WebSocket] = set()

@app.websocket("/ws/admin/manager-requests")
async def ws_manager_requests(websocket: WebSocket):
    await websocket.accept()
    admin_ws_connections.add(websocket)
    print("WS CONNECTED")

    try:
        # Просто держим соединение открытым.
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("WS DISCONNECTED")
        admin_ws_connections.discard(websocket)

# Рассылка уведомлений всем активным админам.
async def notify_admins_manager_request(user_info: dict):
    dead = []
    for ws in list(admin_ws_connections):
        try:
            await ws.send_json({
                "type": "manager_request",
                "user": user_info,
                "created_at": datetime.utcnow().isoformat(),
            })
        except Exception:
            dead.append(ws)
    # Чистим отвалившиеся соединения.
    for ws in dead:
        admin_ws_connections.discard(ws)

# Подключаем админские маршруты.
from src.admin.admin_routes import router as admin_router
app.include_router(admin_router)

# Запрос менеджера — логируем и уведомляем админов.
@app.post("/assistant/request-manager")
async def request_manager(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    print("RAW REQUEST:", data)

    user_info = {
        "id": data.get("user_id"),
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
    }

    # Пишем событие в лог.
    log = AdminLog(
        action="REQUEST_MANAGER",
        product_id=None,
        before=None,
        after=json.dumps(user_info, ensure_ascii=False),
        created_at=datetime.utcnow(),
    )
    db.add(log)
    db.commit()

    # Уведомляем админов по WebSocket.
    await notify_admins_manager_request(user_info)

    return {"reply": "Ваш менеджер свяжется с вами в ближайшее время"}

# История запросов менеджеру — для админ-панели.
@app.get("/admin/manager-requests")
def get_manager_requests(db: Session = Depends(get_db)):
    logs = db.query(AdminLog).filter(AdminLog.action == "REQUEST_MANAGER").all()

    result = []
    for log in logs:
        try:
            data = json.loads(log.after) if log.after else {}
        except:
            data = {}

        result.append({
            "id": log.id,
            "user_name": data.get("name"),
            "user_email": data.get("email"),
            "user_phone": data.get("phone"),
            "created_at": log.created_at.isoformat(),
        })


    return result



@app.delete("/admin/manager-requests/{log_id}")
def delete_manager_request(log_id: int, db: Session = Depends(get_db)):
    log = db.query(AdminLog).filter(AdminLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Запрос не найден")

    db.delete(log)
    db.commit()
    return {"status": "ok"}

# Обёртка над Mistral API — чтобы не дублировать код.
def call_mistral(messages: list):
    """
    Обёртка для вызова Mistral API.
    В тестах эта функция будет замокана.
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-small-latest",
        "messages": messages,
        "temperature": 0.7
    }

    try:
        resp = requests.post(MISTRAL_URL, headers=headers, json=payload, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


# Основной чат ассистента.
# Здесь обрабатываем текст, VIN, номера деталей и зовём Mistral.
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "").strip()

    if not user_message:
        raise HTTPException(status_code=400, detail="Поле 'message' обязательно")
    
    # Если пользователь явно просит менеджера — не зовём ИИ.
    manager_triggers = [
        "менеджер", "оператор", "живой человек",
        "позвать менеджера", "нужен менеджер",
        "хочу поговорить с менеджером",
    ]

    if any(t in user_message.lower() for t in manager_triggers):
        return {"reply": "Ваш менеджер свяжется с вами в ближайшее время"}

    # Ищем VIN в тексте.
    vin_match = re.search(r"\b([A-HJ-NPR-Z0-9]{17})\b", user_message)
    vin_data = None

    if vin_match:
        vin = vin_match.group(1)
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://127.0.0.1:8000/api/vin/{vin}")
            vin_data = resp.json()

    # Ищем номер детали.
    part_match = re.search(r"\b([A-Z0-9\-]{5,})\b", user_message)
    part_data = None

    if part_match:
        part_number = part_match.group(1)
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://127.0.0.1:8000/api/product/by-part/{part_number}")
            if resp.status_code == 200:
                part_data = resp.json()

    # Формируем системный промпт для модели.
    system_prompt = (
        "Ты — AI‑ассистент CarParts AI. "
        "Ты помогаешь пользователю с подбором деталей, VIN‑проверкой и совместимостью.\n\n"
    )

    if vin_data and vin_data.get("make"):
        system_prompt += f"Данные по VIN:\n{vin_data}\n\n"
    else:
        system_prompt += "Данные по VIN: отсутствуют.\n\n"

    if part_data:
        system_prompt += f"Данные по детали:\n{part_data}\n\n"
    else:
        system_prompt += "Данные по детали: отсутствуют.\n\n"

    system_prompt += (
        "Если данных из API нет, используй знания об автомобилях. "
        "Отвечай строго на русском языке."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    result = call_mistral(messages)

    if "choices" not in result:
        return {"reply": f"Ошибка API: {result}"}

    reply = result["choices"][0]["message"]["content"]
    return {"reply": reply}

# VIN API — сначала ищем в локальной базе, потом AutoDev.
@app.get("/api/vin/{vin}")
async def decode_vin(vin: str, db: Session = Depends(get_db)):
    vin = vin.upper().strip()

    if len(vin) != 17:
        raise HTTPException(status_code=400, detail="VIN должен быть 17 символов")

    parts = db.query(Part).filter(Part.vin == vin).all()

    if parts:
        p = parts[0]
        return {
            "vin": vin,
            "make": p.brand,
            "model": p.model,
            "year": p.year,
            "engine": p.engine,
            "parts": [
                {
                    "vin": part.vin,
                    "brand": part.brand,
                    "model": part.model,
                    "year": part.year,
                    "engine": part.engine,
                    "category": part.category,
                    "sub_category": part.sub_category,
                    "part_number": part.part_number,
                    "part_name": part.part_name,
                    "oem": part.oem,
                }
                for part in parts
            ],
            "raw": {
                "brand": p.brand,
                "model": p.model,
                "year": p.year,
                "engine": p.engine,
            }
        }

    # Если ключа AutoDev нет — возвращаем пустой ответ.
    if not AUTO_DEV_API_KEY:
        return {
            "vin": vin,
            "make": None,
            "model": None,
            "year": None,
            "engine": None,
            "parts": [],
            "raw": None
        }

    # Запрашиваем AutoDev.
    url = f"https://api.auto.dev/vin/{vin}"
    headers = {"Authorization": f"Bearer {AUTO_DEV_API_KEY}"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, headers=headers)

    if resp.status_code != 200:
        return {
            "vin": vin,
            "make": None,
            "model": None,
            "year": None,
            "engine": None,
            "parts": [],
            "raw": None
        }

    data = resp.json()

    model = data.get("model")
    brand = data.get("make")

    # Подбираем детали по модели/бренду.
    parts_by_model = db.query(Part).filter(
        Part.model == model,
        Part.brand == brand
    ).all()

    return {
        "vin": vin,
        "make": brand,
        "model": model,
        "year": data.get("year"),
        "engine": data.get("engine"),
        "parts": [
            {
                "vin": part.vin,
                "brand": part.brand,
                "model": part.model,
                "year": part.year,
                "engine": part.engine,
                "category": part.category,
                "sub_category": part.sub_category,
                "part_number": part.part_number,
                "part_name": part.part_name,
                "oem": part.oem,
            }
            for part in parts_by_model
        ],
        "raw": data
    }

# Каталог деталей.
@app.get("/api/catalog")
def api_catalog(db: Session = Depends(get_db)):
    parts = db.query(Part).all()
    return [
        {
            "vin": p.vin,
            "brand": p.brand,
            "model": p.model,
            "year": p.year,
            "engine": p.engine,
            "category": p.category,
            "sub_category": p.sub_category,
            "part_number": p.part_number,
            "part_name": p.part_name,
            "oem": p.oem,
        }
        for p in parts
    ]


@app.get("/api/catalog/{part_number}")
def api_catalog_item(part_number: str, db: Session = Depends(get_db)):
    p = db.query(Part).filter(Part.part_number == part_number).first()
    if not p:
        raise HTTPException(status_code=404, detail="Деталь не найдена")

    return {
        "vin": p.vin,
        "brand": p.brand,
        "model": p.model,
        "year": p.year,
        "engine": p.engine,
        "category": p.category,
        "sub_category": p.sub_category,
        "part_number": p.part_number,
        "part_name": p.part_name,
        "oem": p.oem,
    }


@app.get("/api/product/by-part/{part_number}")
def get_product_by_part(part_number: str, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.part_number == part_number).first()

    if not part:
        raise HTTPException(404, "Деталь не найдена")

    return {
        "source": "part",
        "id": part.id,
        "vin": part.vin,
        "brand": part.brand,
        "model": part.model,
        "year": part.year,
        "engine": part.engine,
        "category": part.category,
        "sub_category": part.sub_category,
        "part_number": part.part_number,
        "part_name": part.part_name,
        "oem": part.oem,
        "price": part.price,
        "stock": part.stock,
        
    }


# Корневой маршрут — просто проверка, что сервер жив.
@app.get("/")
def root():
    return {"message": "CarParts AI backend работает!"}
