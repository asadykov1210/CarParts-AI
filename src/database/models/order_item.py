from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.database.db import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    # Заказ, к которому относится позиция.
    order_id = Column(Integer, ForeignKey("orders.id"))

    # Товар, добавленный в заказ.
    product_id = Column(Integer, ForeignKey("parts.id"))

    # Название товара на момент оформления.
    product_name = Column(String)
    # Количество единиц товара.
    quantity = Column(Integer, default=1)
    # Цена товара на момент оформления.
    price_at_moment = Column(Float)
    
    # Связи с заказом и товаром.
    order = relationship("Order", back_populates="items")
    part = relationship("Part")
