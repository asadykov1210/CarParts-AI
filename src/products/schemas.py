from pydantic import BaseModel

class ProductSchema(BaseModel):
    # Основные данные о товаре.
    name: str
    price: float
    stock: int
    article: str

    # Дополнительные характеристики.
    brand: str | None = None
    model: str | None = None
    category: str | None = None
