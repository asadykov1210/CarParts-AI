from src.database.db import SessionLocal


# Генератор сессии базы данных.
# Создаёт новую сессию для запроса и закрывает её после использования.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
