import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

export default function ManagerRequests() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

   // Загружаем список запросов менеджеру.
  const loadRequests = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await fetch("http://localhost:8000/admin/manager-requests", {
        headers: {
          "Content-Type": "application/json",
          Authorization: token ? `Bearer ${token}` : "",
        },
      });

      const data = await response.json();
      setRequests(data);
    } catch (err) {
      toast.error("Ошибка загрузки запросов менеджеру");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRequests();
  }, []);

  // WebSocket для получения новых запросов в реальном времени.
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/admin/manager-requests");

    ws.onopen = () => console.log("WS CONNECTED");

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === "manager_request") {
          toast.success("Новый запрос менеджеру");
          loadRequests();
        }
      } catch (e) {
        console.error("WS parse error:", e);
      }
    };

    ws.onerror = (e) => console.error("WS ERROR:", e);
    ws.onclose = () => console.log("WS CLOSED");

    return () => ws.close();
  }, []);

  // Отметить запрос как обработанный.
  const markDone = async (id) => {
    try {
      const token = localStorage.getItem("token");

      await fetch(`http://localhost:8000/admin/manager-requests/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: token ? `Bearer ${token}` : "",
        },
      });

      toast.success("Запрос обработан");
      setRequests((prev) => prev.filter((r) => r.id !== id));
    } catch (err) {
      toast.error("Ошибка при удалении");
    }
  };

  return (
    <div style={{ padding: 24, color: "white" }}>
      {/* Заголовок + кнопка назад */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: 20,
          alignItems: "center",
        }}
      >
        <h1 style={{ fontSize: 28, color: "#D4AF37" }}>Запросы менеджеру</h1>

        {/* 🔥 Кнопка назад в твоём стиле */}
        <button
          onClick={() => navigate("/admin/products")}
          style={{
            background: "#D4AF37",
            color: "black",
            padding: "10px 20px",
            borderRadius: 4,
            fontWeight: 600,
            cursor: "pointer",
            border: "none",
          }}
        >
          ← Назад
        </button>
      </div>

      {loading && <p>Загрузка...</p>}

      {!loading && requests.length === 0 && (
        <p style={{ color: "#777" }}>Запросов пока нет</p>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        {requests.map((req) => (
          <div
            key={req.id}
            style={{
              background: "#111",
              border: "1px solid #333",
              padding: 16,
              borderRadius: 10,
            }}
          >
            <div style={{ marginBottom: 6 }}>
              <strong>Имя:</strong> {req.name || "—"}
            </div>

            <div style={{ marginBottom: 6 }}>
              <strong>Email:</strong> {req.email || "—"}
            </div>

            <div style={{ marginBottom: 6 }}>
              <strong>Телефон:</strong> {req.phone || "—"}
            </div>

            <div style={{ marginBottom: 10 }}>
              <strong>Дата:</strong>{" "}
              {req.created_at
                ? new Date(req.created_at).toLocaleString()
                : "—"}
            </div>

            <button
              onClick={() => markDone(req.id)}
              style={{
                background: "#D4AF37",
                color: "#000",
                padding: "8px 14px",
                borderRadius: 8,
                fontWeight: 600,
                cursor: "pointer",
              }}
            >
              Отметить как обработано
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
