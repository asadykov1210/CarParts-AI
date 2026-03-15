from sqlalchemy.orm import Session
from src.database.models import User

# Возвращает пользователя по email или None, если такого нет.
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
