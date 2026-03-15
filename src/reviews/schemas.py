from pydantic import BaseModel

class ReviewCreate(BaseModel):
    # Данные, необходимые для создания отзыва.
    product_id: int
    rating: int
    comment: str | None = None


class ReviewOut(BaseModel):
    # Поля, возвращаемые при выдаче отзыва.
    id: int
    product_id: int
    rating: int
    comment: str | None
    user_id: int
    user_name: str

    class Config:
        from_attributes = True
