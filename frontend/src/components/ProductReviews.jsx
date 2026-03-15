import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";

export default function ProductReviews({ productId }) {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  // Берём пользователя из localStorage
  const user = JSON.parse(localStorage.getItem("user"));

  // Загружаем отзывы товара.
  const loadReviews = async () => {
    const data = await apiRequest(`/reviews/product/${productId}`, "GET");
    setReviews(data);
    setLoading(false);
  };

  // Удаление отзыва.
  const deleteReview = async (id) => {
    if (!confirm("Удалить отзыв?")) return;

    await apiRequest(`/reviews/${id}`, "DELETE");
    setReviews(reviews.filter((r) => r.id !== id));
  };

  useEffect(() => {
    // Загружаем отзывы при смене товара.
    loadReviews();
  }, [productId]);

  if (loading) return <div style={{ color: "#aaa" }}>Загрузка отзывов...</div>;

  return (
    <div style={{ marginTop: 30 }}>
      <h2 style={{ color: "#D4AF37" }}>Отзывы</h2>

      {reviews.length === 0 && (
        <p style={{ color: "#aaa" }}>Отзывов пока нет.</p>
      )}

      {reviews.map((r) => (
        <div
          key={r.id}
          style={{
            background: "#1A1A1A",
            padding: 12,
            borderRadius: 8,
            marginBottom: 12,
            border: "1px solid #333",
          }}
        >
          <div style={{ color: "#D4AF37", fontWeight: 600 }}>
            {r.user_name} — {r.rating} / 5
          </div>
          <div style={{ marginTop: 6 }}>{r.comment}</div>

          {(user?.id === r.user_id || user?.role === "admin") && (
            <button
              onClick={() => deleteReview(r.id)}
              style={{
                marginTop: 10,
                background: "#FF4D4D",
                color: "#fff",
                border: "none",
                padding: "6px 10px",
                borderRadius: 6,
                cursor: "pointer",
                fontSize: 12,
              }}
            >
              Удалить
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
