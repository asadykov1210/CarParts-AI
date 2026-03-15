from sqlalchemy.orm import Session
from src.database.models import User
from src.utils.security import hash_password, verify_password

# Создание пользователя.
def create_user(db: Session, email: str, name: str, password: str):
    user = User(
        email=email,
        name=name,
        password_hash=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Проверка логина/пароля.
# Возвращаем пользователя, если всё ок, иначе — None.
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
