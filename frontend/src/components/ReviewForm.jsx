import { useState } from "react";
import { apiRequest } from "../api/client";

export default function ReviewForm({ productId, onClose }) {
  // Локальное состояние формы.
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");

  // Отправка отзыва.
  const submitReview = async () => {
    try {
      await apiRequest("/reviews", "POST", {
        product_id: productId,
        rating,
        comment,
      });

      alert("Спасибо за отзыв!");
      onClose();
    } catch (err) {
      alert("Ошибка при отправке отзыва");
    }
  };

  return (
    <div
      style={{
        marginTop: 12,
        padding: 16,
        background: "#222",
        borderRadius: 8,
        border: "1px solid #333",
      }}
    >
      <h3 style={{ color: "#D4AF37", marginBottom: 12 }}>Оставить отзыв</h3>

      {/* Оценка */}
      <label
        style={{
          color: "#fff",
          display: "block",
          marginBottom: 6,
          fontWeight: 500,
        }}
      >
        Оценка:
      </label>

      <select
        value={rating}
        onChange={(e) => setRating(Number(e.target.value))}
        style={{
          marginBottom: 16, // <-- нормальный отступ
          padding: 8,
          borderRadius: 6,
          background: "#fff",
          color: "#000",
          width: "100%",
          border: "1px solid #ccc",
        }}
      >
        <option value={5}>5 — Отлично</option>
        <option value={4}>4 — Хорошо</option>
        <option value={3}>3 — Нормально</option>
        <option value={2}>2 — Плохо</option>
        <option value={1}>1 — Ужасно</option>
      </select>

      {/* Комментарий */}
      <label
        style={{
          color: "#fff",
          display: "block",
          marginBottom: 6,
          fontWeight: 500,
        }}
      >
        Комментарий:
      </label>

      <textarea
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        placeholder="Напишите свой отзыв..."
        style={{
          width: "100%",
          height: 90,
          marginBottom: 16,
          padding: 10,
          borderRadius: 6,
          background: "#fff",
          color: "#000",
          border: "1px solid #ccc",
          resize: "vertical",
        }}
      />

      {/* Кнопки */}
      <div style={{ display: "flex", gap: 10 }}>
        <button
          onClick={submitReview}
          style={{
            background: "#D4AF37",
            color: "#000",
            padding: "8px 14px",
            borderRadius: 6,
            cursor: "pointer",
            fontWeight: 600,
            border: "none",
          }}
        >
          Отправить
        </button>

        <button
          onClick={onClose}
          style={{
            background: "#444",
            color: "#fff",
            padding: "8px 14px",
            borderRadius: 6,
            cursor: "pointer",
            border: "none",
          }}
        >
          Отмена
        </button>
      </div>
    </div>
  );
}
