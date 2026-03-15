from pydantic import BaseModel, ConfigDict

# Данные для регистрации.
class UserRegister(BaseModel):
    email: str
    name: str
    password: str
    phone: str | None = None
    city: str | None = None
    country: str | None = None

# Данные для входа.
class UserLogin(BaseModel):
    email: str
    password: str

# Обновление профиля
class UserUpdate(BaseModel):
    name: str
    password: str | None = None
    phone: str | None = None
    city: str | None = None
    country: str | None = None

# Профиль пользователя, который возвращаем наружу.
class UserProfile(BaseModel):
    id: int
    email: str
    name: str
    role: str
    phone: str | None = None
    city: str | None = None
    country: str | None = None

    model_config = ConfigDict(from_attributes=True)
