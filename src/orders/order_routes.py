from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from src.database.deps import get_db
from src.database.models.cart_item import CartItem
from src.database.models.order import Order
from src.database.models.order_item import OrderItem
from src.database.models.part import Part
from src.auth.routes import get_current_user
from src.database.models.user import User

router = APIRouter(tags=["orders"])


# Создание нового заказа на основе содержимого корзины.
@router.post("/create")
def create_order(
    data: dict,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    required_fields = ["name", "phone", "email", "address"]
    for field in required_fields:
        if field not in data or not data[field]:
            raise HTTPException(400, f"Поле '{field}' обязательно")

    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()

    if not cart_items:
        raise HTTPException(400, "Корзина пуста")

    total = 0

    # Проверяем наличие товаров и рассчитываем итоговую сумму.
    for item in cart_items:
        part = db.query(Part).filter(Part.id == item.product_id).first()
        if not part or part.stock < item.quantity:
            raise HTTPException(400, f"Недостаточно товара: {part.part_name}")
        total += part.price * item.quantity

    # Определяем порядковый номер заказа для пользователя.
    last_order = (
        db.query(Order)
        .filter(Order.user_id == user.id)
        .order_by(Order.user_order_number.desc())
        .first()
    )

    next_number = 1 if not last_order else last_order.user_order_number + 1

    # Создаём запись заказа.
    order = Order(
        user_id=user.id,
        user_order_number=next_number,
        total_amount=total,
        name=data["name"],
        phone=data["phone"],
        email=data["email"],
        address=data["address"],
        payment_method=data.get("payment_method", "card"),
        status="new",
        created_at=datetime.utcnow()
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    # Формируем позиции заказа и обновляем склад.
    for item in cart_items:
        part = db.query(Part).filter(Part.id == item.product_id).first()
        part.stock -= item.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=part.id,
            product_name=part.part_name,
            quantity=item.quantity,
            price_at_moment=part.price
        )
        db.add(order_item)

        db.delete(item)

    db.commit()

    return {
        "message": "Заказ оформлен",
        "order_id": order.id,
        "user_order_number": order.user_order_number
    }


# Получение списка заказов текущего пользователя.
@router.get("/my")
def my_orders(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == user.id)
        .order_by(Order.id.desc())
        .all()
    )

    return [
        {
            "id": o.id,
            "user_order_number": o.user_order_number,
            "total_amount": o.total_amount,
            "status": o.status,
        }
        for o in orders
    ]


# Получение подробной информации о конкретном заказе.
@router.get("/{order_id}")
def get_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == user.id)
        .first()
    )

    if not order:
        raise HTTPException(404, "Заказ не найден")

    items = (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order_id)
        .all()
    )

    return {
        "id": order.id,
        "user_order_number": order.user_order_number,
        "total_amount": order.total_amount,
        "name": order.name,
        "phone": order.phone,
        "email": order.email,
        "address": order.address,
        "payment_method": order.payment_method,
        "items": [
            {
                "product_id": oi.product_id,
                "product_name": oi.product_name,
                "quantity": oi.quantity,
                "price": oi.price_at_moment,
            }
            for oi in items
        ],
    }


# Удаление заказа и возврат товаров на склад.
@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == user.id)
        .first()
    )

    if not order:
        raise HTTPException(404, "Заказ не найден")

    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    # Возвращаем количество товаров на склад.
    for item in items:
        part = db.query(Part).filter(Part.id == item.product_id).first()
        if part:
            part.stock += item.quantity

    db.delete(order)
    db.commit()

    return {"message": "Заказ удалён и товары возвращены на склад"}
