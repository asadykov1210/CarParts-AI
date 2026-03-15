from typing import Dict, Any

class ArticleAgent:
    """
    Класс для обработки артикулов автозапчастей.
    Выполняет поиск детали и получение информации о совместимости.
    """

    def __init__(self, catalog_client, compatibility_service):
        # Клиент каталога и сервис проверки совместимости.
        self.catalog = catalog_client
        self.compat = compatibility_service

    def process(self, article: str) -> Dict[str, Any]:
        # Получаем информацию о детали по артикулу.
        part = self.catalog.get_part_by_number(article)
        if not part:
            return {
                "type": "article",
                "article": article,
                "status": "not_found",
                "message": "Деталь с таким артикулом не найдена."
            }

        # Получаем данные о совместимости.
        compat = self.catalog.get_compatibility_for_part(article)

        return {
            "type": "article",
            "article": article,
            "status": "ok",
            "part": part,
            "compatibility": compat
        }
