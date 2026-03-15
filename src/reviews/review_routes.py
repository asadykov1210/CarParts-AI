from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.deps import get_db
from src.database.models.review import Review
from src.database.models.part import Part
from src.reviews.schemas import ReviewCreate, ReviewOut
from src.auth.routes import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewOut)
def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Проверяем, что деталь существует
    part = db.query(Part).filter(Part.id == review_in.product_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Деталь не найдена")

    # Проверяем, что пользователь покупал эту деталь
    order_item = db.execute(
        text("""
            SELECT oi.id
            FROM order_items oi
            JOIN orders o ON o.id = oi.order_id
            WHERE oi.product_id = :pid AND o.user_id = :uid
        """),
        {"pid": review_in.product_id, "uid": current_user.id}
    ).fetchone()

    if not order_item:
        raise HTTPException(
            status_code=400,
            detail="Вы не можете оставить отзыв на деталь, которую не покупали"
        )

    # Создаём отзыв
    review = Review(
        user_id=current_user.id,
        product_id=review_in.product_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "id": review.id,
        "product_id": review.product_id,
        "rating": review.rating,
        "comment": review.comment,
        "user_id": review.user_id,
        "user_name": review.user.name,
    }


@router.get("/product/{product_id}", response_model=list[ReviewOut])
def get_reviews_for_product(product_id: int, db: Session = Depends(get_db)):
    # Получаем список отзывов для указанной детали.
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(Review.id.desc())
        .all()
    )

    return [
        {
            "id": r.id,
            "product_id": r.product_id,
            "rating": r.rating,
            "comment": r.comment,
            "user_id": r.user_id,
            "user_name": r.user.name,
        }
        for r in reviews
    ]


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Проверяем, что отзыв существует.
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")

    # Удалять может автор или администратор.
    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Удаление запрещено")

    db.delete(review)
    db.commit()

    return {"message": "Отзыв удалён"}
