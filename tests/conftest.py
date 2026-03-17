import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Делаем src/ доступным для импорта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.db import Base
from src.database.deps import get_db
from main import app

#   ТЕСТОВАЯ БАЗА ДАННЫХ
# Используем SQLite in‑memory + StaticPool,
# чтобы база жила на протяжении всех тестов
TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
# Фабрика сессий для тестов
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=TEST_ENGINE
)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Создаём таблицы один раз для всей сессии тестов."""
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture()
def db_session():
    """Создаём новую сессию БД для каждого теста."""
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(autouse=True)
def clean_database(db_session):
    """Очищаем ВСЕ таблицы перед каждым тестом."""
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()


@pytest.fixture()
def client(db_session):
    """Переопределяем get_db и создаём TestClient."""
    def override_get_db():
        # Подменяем зависимость, чтобы тесты использовали тестовую БД
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)
