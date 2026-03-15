from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    # Пользователь, оформивший заказ.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Порядковый номер заказа для конкретного пользователя.
    user_order_number = Column(Integer, nullable=False)

    # Контактные данные, указанные при оформлении.
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # Способ оплаты.
    payment_method = Column(String, default="card")
    # Текущий статус заказа.
    status = Column(String, default="new")
    # Итоговая сумма заказа.
    total_amount = Column(Float, nullable=False)
    # Дата создания заказа.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с пользователем и позициями заказа.
    user = relationship("User", back_populates="orders")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
