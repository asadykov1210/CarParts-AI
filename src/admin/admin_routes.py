import json
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.database.deps import get_db
from src.database.models.part import Part
from src.database.models.admin_log import AdminLog

router = APIRouter(prefix="/admin", tags=["admin"])


# Утилита для приведения модели Part к обычному dict.
# Используем в ответах API
def part_to_dict(part: Part) -> dict:
    if not part:
        return {}

    return {
        "id": part.id,
        "part_number": part.part_number,
        "part_name": part.part_name,
        "brand": part.brand,
        "model": part.model,
        "year": part.year,
        "engine": part.engine,
        "category": part.category,
        "sub_category": part.sub_category,
        "oem": part.oem,
        "vin": part.vin,
        "price": part.price,
        "stock": part.stock,
    }


# CRUD по товарам (Part)
@router.get("/products")
def get_all_parts(db: Session = Depends(get_db)):
    # Возвращаем весь каталог для админ-панели.
    parts = db.query(Part).all()
    return [part_to_dict(p) for p in parts]


@router.get("/products/{part_id}")
def get_part(part_id: int, db: Session = Depends(get_db)):
    # Получение одной детали по ID.
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Деталь не найдена")
    return part_to_dict(part)


@router.post("/products")
def create_part(data: dict, db: Session = Depends(get_db)):
    # Создание новой детали.
    part = Part(
        part_number=data.get("part_number"),
        part_name=data.get("part_name"),
        brand=data.get("brand"),
        model=data.get("model"),
        year=data.get("year"),
        engine=data.get("engine"),
        category=data.get("category"),
        sub_category=data.get("sub_category"),
        oem=data.get("oem"),
        vin=data.get("vin"),
        price=data.get("price"),
        stock=data.get("stock"),
    )

    db.add(part)
    db.commit()
    db.refresh(part)

    # Логируем создание.
    log = AdminLog(
        action="CREATE",
        product_id=part.id,
        before=None,
        after=json.dumps(part_to_dict(part), ensure_ascii=False),
        created_at=datetime.utcnow(),
    )
    db.add(log)
    db.commit()

    return part_to_dict(part)


@router.put("/products/{part_id}")
def update_part(part_id: int, data: dict, db: Session = Depends(get_db)):
    # Обновление существующей детали.
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Деталь не найдена")

    before_data = part_to_dict(part)

    # Поля, которые разрешено обновлять.
    fields = {
        "part_name": "part_name",
        "part_number": "part_number",
        "brand": "brand",
        "model": "model",
        "year": "year",
        "engine": "engine",
        "category": "category",
        "sub_category": "sub_category",
        "oem": "oem",
        "vin": "vin",
        "price": "price",
        "stock": "stock",
    }

    # Обновляем только те поля, что пришли в запросе.
    for key, attr in fields.items():
        if key in data:
            setattr(part, attr, data[key])

    db.commit()
    db.refresh(part)

    after_data = part_to_dict(part)

    # Логируем изменение.
    log = AdminLog(
        action="UPDATE",
        product_id=part.id,
        before=json.dumps(before_data, ensure_ascii=False),
        after=json.dumps(after_data, ensure_ascii=False),
        created_at=datetime.utcnow(),
    )
    db.add(log)
    db.commit()

    return after_data


@router.delete("/products/{part_id}")
def delete_part(part_id: int, db: Session = Depends(get_db)):
    # Удаление детали.
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Деталь не найдена")

    before_data = part_to_dict(part)

    db.delete(part)
    db.commit()

    # Логируем удаление.
    log = AdminLog(
        action="DELETE",
        product_id=part_id,
        before=json.dumps(before_data, ensure_ascii=False),
        after=None,
        created_at=datetime.utcnow(),
    )
    db.add(log)
    db.commit()

    return {"deleted": part_id}


# Логи админ-панели — полный CRUD по AdminLog

@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    # Возвращаем все логи, последние — сверху.
    logs = db.query(AdminLog).order_by(AdminLog.created_at.desc()).all()

    return [
        {
            "id": log.id,
            "action": log.action,
            "product_id": log.product_id,
            "before": log.before,
            "after": log.after,
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]


@router.get("/logs/{log_id}")
def get_log(log_id: int, db: Session = Depends(get_db)):
    # Получение одного лога.
    log = db.query(AdminLog).filter(AdminLog.id == log_id).first()
    if not log:
        raise HTTPException(404, "Лог не найден")

    return {
        "id": log.id,
        "action": log.action,
        "product_id": log.product_id,
        "before": log.before,
        "after": log.after,
        "created_at": log.created_at.isoformat(),
    }


@router.delete("/logs/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    # Удаление лога.
    log = db.query(AdminLog).filter(AdminLog.id == log_id).first()
    if not log:
        raise HTTPException(404, "Лог не найден")

    db.delete(log)
    db.commit()

    return {"deleted": log_id}


# Запросы менеджеру — те же логи, но в удобном виде.
@router.get("/manager-requests")
def get_manager_requests(db: Session = Depends(get_db)):
    logs = (
        db.query(AdminLog)
        .filter(AdminLog.action == "REQUEST_MANAGER")
        .order_by(AdminLog.created_at.desc())
        .all()
    )

    result = []
    for log in logs:
        try:
            data = json.loads(log.after) if log.after else {}
        except:
            data = {}

        print("MANAGER REQUEST DATA:", data)

        result.append({
            "id": log.id,
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "created_at": log.created_at.isoformat()
        })

    return result




