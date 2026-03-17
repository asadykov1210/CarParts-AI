from typing import Dict, Any

class TextAgent:
    """
    Агент обработки текстовых описаний проблем.
    """

    def __init__(self, catalog_client):
        self.catalog = catalog_client

    def process(self, text: str) -> Dict[str, Any]:
        problem_row = self.catalog.find_problem_category(text)
        if not problem_row:
            return {
                "type": "text",
                "query": text,
                "status": "unknown",
                "message": "Не удалось сопоставить проблему с известной категорией."
            }

        suggested_part_name = self.catalog.suggest_part_for_problem(problem_row["problem"])
        parts = self.catalog.find_parts_by_name(suggested_part_name) if suggested_part_name else []

        return {
            "type": "text",
            "query": text,
            "status": "ok",
            "problem": problem_row["problem"],
            "category": problem_row["category"],
            "suggested_part_name": suggested_part_name,
            "candidate_parts": parts
        }
