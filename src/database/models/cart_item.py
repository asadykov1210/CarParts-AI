from sqlalchemy import Column, Integer, ForeignKey
from src.database.db import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    # Пользователь, которому принадлежит запись.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Товар, добавленный в корзину.
    product_id = Column(Integer, ForeignKey("parts.id"), nullable=False)

    # Количество единиц товара.
    quantity = Column(Integer, default=1)
