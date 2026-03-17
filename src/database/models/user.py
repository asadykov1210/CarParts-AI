from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Основные данные пользователя.
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password_hash = Column(String)
    role = Column(String)

    # Контактная информация.
    phone = Column(String)
    city = Column(String)
    country = Column(String)

    # Связи с отзывами и заказами.
    reviews = relationship("Review", back_populates="user")
    orders = relationship("Order", back_populates="user")  # <-- ДОБАВИЛИ
