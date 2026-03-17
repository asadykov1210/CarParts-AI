import { useState, useEffect } from "react";
import { apiRequest } from "../api/client";
import { useNavigate } from "react-router-dom";

export default function EditProfile() {
  const navigate = useNavigate();

  // Поля профиля
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  const [phone, setPhone] = useState("");
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");

  const [error, setError] = useState("");

  useEffect(() => {
    // Загружаем данные пользователя
    const load = async () => {
      try {
        const data = await apiRequest("/auth/me", "GET");

        setEmail(data.email);
        setName(data.name);
        setPhone(data.phone || "");
        setCity(data.city || "");
        setCountry(data.country || "");
      } catch (err) {
        setError(err.message);
      }
    };
    load();
  }, []);

  // Сохранение изменений
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await apiRequest("/auth/update", "PUT", {
        name,
        password,
        phone,
        city,
        country,
      });

      navigate("/profile");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto" }}>
      <h1 style={{ fontSize: 32, marginBottom: 20, color: "#D4AF37" }}>
        Редактировать профиль
      </h1>

      {error && (
        <div
          style={{
            background: "#7F1D1D",
            color: "#FCA5A5",
            padding: 12,
            borderRadius: 8,
            marginBottom: 16,
            fontSize: 14,
          }}
        >
          {error}
        </div>
      )}

      <div className="card">
        <form
          onSubmit={handleSubmit}
          style={{ display: "flex", flexDirection: "column", gap: 16 }}
        >
          <div>
            <label style={{ color: "#D4AF37", fontSize: 14 }}>
              Email (нельзя изменить)
            </label>
            <input
              type="email"
              value={email}
              disabled
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333] text-[#777]"
              style={{ marginTop: 6, cursor: "not-allowed" }}
            />
          </div>

          <div>
            <label style={{ color: "#D4AF37", fontSize: 14 }}>Имя</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333] text-[#F5F5F5]"
              style={{ marginTop: 6 }}
            />
          </div>

          <div>
            <label style={{ color: "#D4AF37", fontSize: 14 }}>Телефон</label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333] text-[#F5F5F5]"
              style={{ marginTop: 6 }}
            />
          </div>

          <div>
            <label style={{ color: "#D4AF37", fontSize: 14 }}>Город</label>
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333] text-[#F5F5F5]"
              style={{ marginTop: 6 }}
            />
          </div>

          <div>
            <label style={{ color: "#D4AF37", fontSize: 14 }}>Страна</label>
            <input
              type="text"
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333] text-[#F5F5F5]"
              style={{ marginTop: 6 }}
            />
          </div>

          <div>
            <label style={{ color: "#D4AF37", fontSize: 14 }}>
              Новый пароль
            </label>
            <input
              type="password"
              placeholder="Введите новый пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333] text-[#F5F5F5]"
              style={{ marginTop: 6 }}
            />
          </div>

          <button
            type="submit"
            className="w-full py-3 rounded-xl font-semibold bg-[#D4AF37] text-black hover:bg-[#b8922f] transition"
            style={{ marginTop: 8 }}
          >
            Сохранить
          </button>
        </form>
      </div>
    </div>
  );
}
