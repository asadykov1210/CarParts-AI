from src.database.db import SessionLocal
from src.database.models.part import Part

class CatalogClient:
    """
    Клиент для работы с таблицей Part.
    Предоставляет методы поиска и вспомогательные операции.
    """

    def get_part_by_number(self, part_number: str):
        # Поиск детали по её артикулу.
        db = SessionLocal()
        try:
            return db.query(Part).filter(Part.part_number == part_number).first()
        finally:
            db.close()

    def get_compatibility_for_part(self, part_number: str):
        """
        Получение информации о совместимости.
        """
        return None

    def find_problem_category(self, text: str):
        """
        Определение категории проблемы по текстовому описанию.
        """
        return None

    def suggest_part_for_problem(self, problem: str):
        """
        Подбор детали на основе описанной проблемы.
        """
        return None

    def find_parts_by_name(self, name: str):
        """
        Поиск деталей по названию.
        """
        db = SessionLocal()
        try:
            return db.query(Part).filter(Part.part_name.ilike(f"%{name}%")).all()
        finally:
            db.close()
