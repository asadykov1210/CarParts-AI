from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime

from src.database.db import Base


class AdminLog(Base):
    __tablename__ = "admin_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Тип действия: создание, обновление или удаление записи.
    action = Column(String, nullable=False)  

    # ID связанного товара (может быть пустым, если действие не привязано к продукту).
    product_id = Column(Integer, ForeignKey("parts.id"), nullable=True)

    # JSON-строки с данными до и после изменения
    before = Column(Text, nullable=True)
    after = Column(Text, nullable=True)
    
    # Время создания записи.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
