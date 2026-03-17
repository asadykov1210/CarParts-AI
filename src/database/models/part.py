from sqlalchemy import Column, Integer, String, Float
from src.database.db import Base

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True)

    # Основные характеристики детали.
    vin = Column(String, index=True)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)
    engine = Column(String)
    category = Column(String)
    sub_category = Column(String)

    # Идентификаторы и названия.
    part_number = Column(String, index=True)
    part_name = Column(String)
    oem = Column(String, nullable=True)

    # Стоимость и количество на складе.
    price = Column(Float, default=0)
    stock = Column(Integer, default=0)
