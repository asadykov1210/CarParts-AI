import { Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Navbar() {
  const location = useLocation();

  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("user"));
    } catch {
      return null;
    }
  });

  useEffect(() => {
    const update = () => {
      setToken(localStorage.getItem("token"));

      try {
        setUser(JSON.parse(localStorage.getItem("user")));
      } catch {
        setUser(null);
      }
    };

    window.addEventListener("auth-change", update);
    return () => window.removeEventListener("auth-change", update);
  }, []);

  //Страницы, где показываем только кнопку "Войти"
  const minimalPages = ["/", "/login", "/register"];
  const isMinimal = minimalPages.includes(location.pathname) && !token;

  return (
    <nav
      style={{
        width: "100%",
        background: "#111111",
        padding: "16px 24px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderBottom: "1px solid #D4AF37",
      }}
    >
      {/* Логотип */}
      <Link
        to="/"
        style={{
          fontSize: 24,
          fontWeight: 700,
          color: "#D4AF37",
          textDecoration: "none",
        }}
      >
        CarParts AI
      </Link>

      {/* Если минимальный режим — показываем только кнопку Войти */}
      {isMinimal && (
        <div style={{ display: "flex", gap: 24, fontSize: 16 }}>
          <Link style={{ color: "#D4AF37", textDecoration: "none" }} to="/login">
            Войти
          </Link>
        </div>
      )}

      {/* Если НЕ минимальный режим — показываем всё меню */}
      {!isMinimal && (
        <div style={{ display: "flex", gap: 24, fontSize: 16 }}>
          <Link style={{ color: "#F5F5F5", textDecoration: "none" }} to="/vin">
            VIN поиск
          </Link>

          <Link style={{ color: "#F5F5F5", textDecoration: "none" }} to="/catalog">
            Каталог
          </Link>

          <Link style={{ color: "#F5F5F5", textDecoration: "none" }} to="/assistant">
            Ассистент
          </Link>

          <Link style={{ color: "#F5F5F5", textDecoration: "none" }} to="/profile">
            Профиль
          </Link>

          {token && (
            <Link style={{ color: "#F5F5F5", textDecoration: "none" }} to="/orders">
              Мои заказы
            </Link>
          )}

          {token && (
            <Link style={{ color: "#F5F5F5", textDecoration: "none" }} to="/cart">
              Корзина
            </Link>
          )}

          {user?.role === "admin" && (
            <Link
              style={{ color: "#D4AF37", textDecoration: "none" }}
              to="/admin/products"
            >
              Админ-панель
            </Link>
          )}

          {!token && (
            <Link style={{ color: "#D4AF37", textDecoration: "none" }} to="/login">
              Войти
            </Link>
          )}

          {token && (
            <button
              onClick={() => {
                localStorage.clear();
                window.dispatchEvent(new Event("auth-change"));
                window.location.href = "/login";
              }}
              style={{
                background: "transparent",
                border: "none",
                color: "#FF4D4D",
                cursor: "pointer",
                fontSize: 16,
              }}
            >
              Выйти
            </button>
          )}
        </div>
      )}
    </nav>
  );
}
