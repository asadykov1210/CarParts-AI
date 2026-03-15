from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import timedelta

from src.database.deps import get_db
from src.database.models.user import User
from .schemas import UserRegister, UserLogin, UserProfile, UserUpdate
from src.utils.security import hash_password, verify_password
from src.utils.jwt import create_access_token, decode_access_token

router = APIRouter(tags=["auth"])

print("AUTH ROUTES LOADED FROM:", __file__)

# Получение текущего пользователя по JWT.
# Проверяем заголовок Authorization, валидируем токен и ищем пользователя в базе.
def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Отсутствует заголовок Authorization")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Неверный формат токена")

    token = parts[1]
    user_id = decode_access_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Неверный или просроченный токен")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user


# Регистрация нового пользователя.
@router.post("/register", response_model=UserProfile)
def register(user_data: UserRegister, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hash_password(user_data.password),
        role="user",
        phone=user_data.phone,
        city=user_data.city,
        country=user_data.country
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# Авторизация.
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):

    
    if data.email == "" and data.password == "":
        return {"access_token": None, "token_type": "bearer", "user": None}

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=7)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "phone": user.phone,
            "city": user.city,
            "country": user.country
        }
    }


# Возвращаем профиль текущего пользователя.
@router.get("/me", response_model=UserProfile)
def get_me(user: User = Depends(get_current_user)):
    return user


# Обновление профиля.
# Меняем только те поля, которые реально пришли в запросе.
@router.put("/update", response_model=UserProfile)
def update_profile(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user.name = data.name

    if data.password:
        user.password_hash = hash_password(data.password)

    if data.phone is not None:
        user.phone = data.phone

    if data.city is not None:
        user.city = data.city

    if data.country is not None:
        user.country = data.country

    db.commit()
    db.refresh(user)
    return user
