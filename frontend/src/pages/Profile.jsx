import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";
import { Navigate } from "react-router-dom";

export default function Profile() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  const token = localStorage.getItem("token");

  // Если токена нет — отправляем на страницу входа
  if (!token) return <Navigate to="/login" replace />;

  useEffect(() => {
     // Загружаем профиль
    const load = async () => {
      try {
        const data = await apiRequest("/auth/me", "GET");
        setUser(data);
      } catch (err) {
        setError(err.message);
      }
    };
    load();
  }, []);

  // Ошибка загрузки
  if (error) {
    return (
      <div style={{ maxWidth: 600, margin: "40px auto", color: "#FF4D4D" }}>
        Ошибка: {error}
      </div>
    );
  }

  // Пока данные загружаются
  if (!user) {
    return (
      <div style={{ maxWidth: 600, margin: "40px auto", color: "#B3B3B3" }}>
        Загрузка профиля...
      </div>
    );
  }

  // Основной контент
  return (
    <div style={{ maxWidth: 600, margin: "40px auto" }}>
      <h1 style={{ fontSize: 32, marginBottom: 20, color: "#D4AF37" }}>
        Профиль
      </h1>

      <div className="card">
        <p style={{ fontSize: 18 }}>
          <span style={{ color: "#B3B3B3" }}>Email:</span> {user.email}
        </p>

        <p style={{ fontSize: 18 }}>
          <span style={{ color: "#B3B3B3" }}>Имя:</span> {user.name}
        </p>

        <p style={{ fontSize: 18 }}>
          <span style={{ color: "#B3B3B3" }}>Телефон:</span> {user.phone || "—"}
        </p>

        <p style={{ fontSize: 18 }}>
          <span style={{ color: "#B3B3B3" }}>Город:</span> {user.city || "—"}
        </p>

        <p style={{ fontSize: 18 }}>
          <span style={{ color: "#B3B3B3" }}>Страна:</span> {user.country || "—"}
        </p>
      </div>

      <a
        href="/profile/edit"
        style={{
          display: "inline-block",
          marginTop: 20,
          background: "#D4AF37",
          color: "#000",
          padding: "10px 16px",
          borderRadius: 8,
          textDecoration: "none",
          fontWeight: 600,
        }}
      >
        Редактировать профиль
      </a>
    </div>
  );
}
