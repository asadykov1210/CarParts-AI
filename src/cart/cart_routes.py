from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.deps import get_db
from src.database.models.cart_item import CartItem
from src.database.models.part import Part
from src.auth.routes import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])


# Маршрут для получения корзины пользователя.
# Возвращает список товаров с количеством и базовой информацией о продукте.
@router.get("")
def get_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = db.query(CartItem).filter_by(user_id=user.id).all()

    result = []
    for item in items:
        part = db.query(Part).filter(Part.id == item.product_id).first()
        if not part:
            continue

        result.append({
            "id": item.id,
            "product": {
                "id": part.id,
                "name": part.part_name,
                "price": part.price,
                "part_number": part.part_number,
                "image_url": None,  # если добавишь картинки — подставим
            },
            "quantity": item.quantity,
        })

    return result


# Альтернативный маршрут получения корзины.
# Используется в интерфейсе, где требуется другой формат данных.
@router.get("/my")
def get_my_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = db.query(CartItem).filter_by(user_id=user.id).all()

    result = []
    for item in items:
        part = db.query(Part).filter(Part.id == item.product_id).first()
        if not part:
            continue

        result.append({
            "id": item.id,
            "quantity": item.quantity,
            "product": {
                "id": part.id,
                "name": part.part_name,
                "price": part.price,
                "part_number": part.part_number,
                "image_url": None,
            }
        })

    return result


# Добавление товара в корзину.
# Если товар уже есть — увеличиваем количество.
@router.post("/add/{part_id}")
def add_to_cart(part_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Проверяем, что деталь существует
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Деталь не найдена")

    item = db.query(CartItem).filter_by(user_id=user.id, product_id=part_id).first()

    if item:
        item.quantity += 1
    else:
        item = CartItem(user_id=user.id, product_id=part_id, quantity=1)
        db.add(item)

    db.commit()
    return {"status": "ok"}


# Удаление одной штуки товара или всего товара, если quantity = 1.
@router.post("/remove/{item_id}")
def remove_from_cart(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = db.query(CartItem).filter_by(id=item_id, user_id=user.id).first()

    if not item:
        raise HTTPException(404, "Товар не найден в корзине")

    if item.quantity > 1:
        item.quantity -= 1
        db.commit()
        return {"status": "ok", "quantity": item.quantity}

    db.delete(item)
    db.commit()
    return {"status": "removed"}


# Полная очистка корзины пользователя.
@router.delete("/clear")
def clear_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    db.query(CartItem).filter_by(user_id=user.id).delete()
    db.commit()
    return {"status": "cleared"}
