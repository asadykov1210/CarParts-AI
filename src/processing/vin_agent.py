import httpx
from src.database.db import SessionLocal
from src.database.models.part import Part


class VinAgent:
    """
    Агент обработки VIN-кодов.
    Сначала ищет VIN в локальной БД, затем — во внешнем API.
    """

    def __init__(self, external_api_key: str | None = None):
        self.external_api_key = external_api_key

    #Поиск VIN в локальной базе
    def search_local(self, vin: str):
        db = SessionLocal()
        try:
            part = db.query(Part).filter(Part.vin == vin).first()
            return part
        finally:
            db.close()

    #Поиск VIN во внешнем API
    async def search_external(self, vin: str):
        if not self.external_api_key:
            return None

        url = f"https://api.auto.dev/vin/{vin}"
        headers = {"Authorization": f"Bearer {self.external_api_key}"}

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=headers)

        if resp.status_code != 200:
            return None

        return resp.json()

    #Основной метод обработки
    async def process(self, vin: str):
        vin = vin.upper().strip()

        if len(vin) != 17:
            return {
                "type": "vin",
                "vin": vin,
                "status": "error",
                "message": "VIN должен содержать 17 символов."
            }

        # Проверяем локальную базу.
        local = self.search_local(vin)
        if local:
            return {
                "type": "vin",
                "vin": vin,
                "status": "ok",
                "source": "local_db",
                "brand": local.brand,
                "model": local.model,
                "year": local.year,
                "engine": local.engine,
                "raw": {
                    "brand": local.brand,
                    "model": local.model,
                    "year": local.year,
                    "engine": local.engine,
                }
            }

        # Обращаемся к внешнему API.
        external = await self.search_external(vin)
        if external:
            return {
                "type": "vin",
                "vin": vin,
                "status": "ok",
                "source": "external_api",
                "brand": external.get("make"),
                "model": external.get("model"),
                "year": external.get("year"),
                "engine": external.get("engine"),
                "raw": external
            }

        # Если данных нет.
        return {
            "type": "vin",
            "vin": vin,
            "status": "not_found",
            "message": "Информация по VIN не найдена ни в базе, ни во внешнем API."
        }
