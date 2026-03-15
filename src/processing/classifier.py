import re

class QueryClassifier:
    """
    Классификатор типа запроса:
    - vin
    - article
    - text
    - clarification
    """

    VIN_PATTERN = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$", re.IGNORECASE)
    ARTICLE_PATTERN = re.compile(r"^[A-Z0-9\-]{4,}$", re.IGNORECASE)

    def classify(self, query: str) -> str:
        q = query.strip()

        # VIN
        if self.VIN_PATTERN.match(q):
            return "vin"

        # Артикул
        if self.ARTICLE_PATTERN.match(q) and " " not in q:
            return "article"

        # Уточнение
        clarification_keywords = ["дешевле", "подешевле", "аналог", "есть ли еще", "что-нибудь еще"]
        if any(k in q.lower() for k in clarification_keywords):
            return "clarification"

        # Текст
        return "text"
