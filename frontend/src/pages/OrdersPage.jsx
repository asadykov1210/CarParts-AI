import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";
import { Link } from "react-router-dom";

export default function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  // Загружаем заказы пользователя
  useEffect(() => {
    apiRequest("/orders/my", "GET")
      .then((data) => setOrders(data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div style={{ padding: 24, color: "white" }}>Загрузка...</div>;
  }

  return (
    <div style={{ padding: 24, color: "white" }}>
      <h1 style={{ fontSize: 28, marginBottom: 20, color: "#D4AF37" }}>
        Мои заказы
      </h1>

      {orders.length === 0 && (
        <div
          style={{
            background: "#1A1A1A",
            padding: 20,
            borderRadius: 12,
            border: "1px solid #333",
            color: "#aaa",
            maxWidth: 400,
          }}
        >
          У вас пока нет заказов
        </div>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        {orders.map((order) => (
          <div
            key={order.id}
            style={{
              background: "#111",
              border: "1px solid #D4AF37",
              borderRadius: 12,
              padding: 16,
            }}
          >
            <div style={{ fontSize: 18, marginBottom: 6 }}>
              Заказ №{order.user_order_number}
            </div>

            <div style={{ color: "#aaa", marginBottom: 16 }}>
              Сумма: {order.total_amount} ₽
            </div>

            <Link
              to={`/orders/${order.id}`}
              style={{
                background: "#D4AF37",
                padding: "8px 14px",
                borderRadius: 8,
                color: "black",
                fontWeight: 600,
                textDecoration: "none",
              }}
            >
              Подробнее →
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
