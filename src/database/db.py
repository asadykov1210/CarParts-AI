import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Путь к директории, где лежит модуль базы данных.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Путь к SQLite базе
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}"

# Создаём движок SQLAlchemy.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Фабрика сессий для работы с базой.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс моделей
Base = declarative_base()


# Импорт моделей, чтобы SQLAlchemy зарегистрировал их перед созданием таблиц.
from src.database.models.user import User
from src.database.models.cart_item import CartItem
from src.database.models.order import Order
from src.database.models.order_item import OrderItem
from src.database.models.review import Review
from src.database.models.part import Part
from src.database.models.admin_log import AdminLog


# Создание таблиц, если их ещё нет.
def init_db():
    """Создание всех таблиц, если их нет."""
    Base.metadata.create_all(bind=engine)
