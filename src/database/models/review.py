from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    # Пользователь, оставивший отзыв.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Товар, к которому относится отзыв.
    product_id = Column(Integer, ForeignKey("parts.id"), nullable=False)

    # Оценка и текст комментария.
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)

    # Связи с пользователем и товаром.
    user = relationship("User", back_populates="reviews")
    part = relationship("Part")
