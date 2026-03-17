import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";
import { useParams, useNavigate } from "react-router-dom";
import ReviewForm from "../components/ReviewForm";

export default function OrderDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [order, setOrder] = useState(null);
  const [reviews, setReviews] = useState({});
  const [reviewProduct, setReviewProduct] = useState(null);

  // Загружаем данные заказа
  useEffect(() => {
    apiRequest(`/orders/${id}`, "GET").then(setOrder);
  }, [id]);

  // Загружаем отзывы по каждому товару
  useEffect(() => {
    if (!order) return;

    const loadReviews = async () => {
      const result = {};

      for (const item of order.items) {
        const r = await apiRequest(`/reviews/product/${item.product_id}`, "GET");
        result[item.product_id] = r;
      }

      setReviews(result);
    };

    loadReviews();
  }, [order]);

  if (!order) {
    return (
      <div style={{ padding: 24, color: "white" }}>
        Загрузка...
      </div>
    );
  }

  // Цвета статусов
  const statusColors = {
    new: "#D4AF37",
    paid: "#4CAF50",
    canceled: "#FF4D4D",
  };

  return (
    <div style={{ padding: 24, color: "white" }}>
      <h1 style={{ fontSize: 28, marginBottom: 20, color: "#D4AF37" }}>
        Заказ №{order.user_order_number}
      </h1>

      <div
        style={{
          background: "#111",
          border: "1px solid #D4AF37",
          borderRadius: 12,
          padding: 20,
          maxWidth: 600,
        }}
      >
        <div
          style={{
            marginBottom: 20,
            fontSize: 18,
            fontWeight: 600,
            color: statusColors[order.status] || "#D4AF37",
          }}
        >
          Статус:{" "}
          {order.status === "new"
            ? "Новый"
            : order.status === "paid"
            ? "Оплачен"
            : order.status === "canceled"
            ? "Отменён"
            : order.status}
        </div>

        <div style={{ marginBottom: 12 }}>
          <strong>Имя:</strong> {order.name}
        </div>
        <div style={{ marginBottom: 12 }}>
          <strong>Телефон:</strong> {order.phone}
        </div>
        <div style={{ marginBottom: 12 }}>
          <strong>Email:</strong> {order.email}
        </div>
        <div style={{ marginBottom: 12 }}>
          <strong>Адрес:</strong> {order.address}
        </div>

        <h2 style={{ marginTop: 20, marginBottom: 10, color: "#D4AF37" }}>
          Товары
        </h2>

        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {order.items.map((item) => (
            <div
              key={item.product_id}
              style={{
                background: "#1A1A1A",
                padding: 12,
                borderRadius: 10,
                border: "1px solid #333",
              }}
            >
              <div style={{ fontSize: 16 }}>{item.product_name}</div>
              <div style={{ color: "#aaa" }}>
                Количество: {item.quantity}
              </div>
              <div style={{ color: "#aaa" }}>
                Цена: {item.price} ₽
              </div>

              {reviews[item.product_id] &&
                reviews[item.product_id].length > 0 && (
                  <div
                    style={{
                      marginTop: 12,
                      padding: 10,
                      background: "#111",
                      borderRadius: 8,
                      border: "1px solid #333",
                    }}
                  >
                    <h4 style={{ color: "#D4AF37", marginBottom: 8 }}>
                      Отзывы
                    </h4>

                    {reviews[item.product_id].map((r) => (
                      <div key={r.id} style={{ marginBottom: 10 }}>
                        <div
                          style={{
                            color: "#D4AF37",
                            fontWeight: 600,
                            marginBottom: 4,
                          }}
                        >
                          {r.user_name}: {r.rating} / 5
                        </div>
                        <div>{r.comment}</div>
                      </div>
                    ))}
                  </div>
                )}

              <button
                onClick={() => setReviewProduct(item.product_id)}
                style={{
                  marginTop: 10,
                  background: "#111",
                  border: "1px solid #D4AF37",
                  color: "#D4AF37",
                  padding: "6px 12px",
                  borderRadius: 6,
                  cursor: "pointer",
                  fontSize: 14,
                }}
              >
                Оставить отзыв
              </button>

              {reviewProduct === item.product_id && (
                <ReviewForm
                  productId={item.product_id}
                  onClose={() => setReviewProduct(null)}
                />
              )}
            </div>
          ))}
        </div>

        <div
          style={{
            marginTop: 20,
            fontSize: 18,
            fontWeight: 600,
            color: "#D4AF37",
          }}
        >
          Итоговая сумма: {order.total_amount} ₽
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 12,
            marginTop: 20,
          }}
        >
          <button
            onClick={() => navigate("/orders")}
            style={{
              background: "#111",
              border: "1px solid #D4AF37",
              color: "#D4AF37",
              padding: "10px 16px",
              borderRadius: 8,
              cursor: "pointer",
              fontSize: 15,
              fontWeight: 600,
            }}
          >
            ← Назад
          </button>

          <button
            onClick={async () => {
              if (window.confirm("Удалить заказ?")) {
                await apiRequest(`/orders/${order.id}`, "DELETE");
                navigate("/orders");
              }
            }}
            style={{
              background: "#111",
              border: "1px solid #FF4D4D",
              color: "#FF4D4D",
              padding: "10px 16px",
              borderRadius: 8,
              cursor: "pointer",
              fontSize: 15,
              fontWeight: 600,
            }}
          >
            Удалить заказ
          </button>
        </div>
      </div>
    </div>
  );
}
