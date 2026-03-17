import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, adminOnly = false }) {
  // Пытаемся получить пользователя из localStorage.
  let user = null;

  try {
    user = JSON.parse(localStorage.getItem("user"));
  } catch {
    user = null;
  }

  // Если пользователь не авторизован — отправляем на логин.
  if (!user) {
    return <Navigate to="/login" />;
  }

  // Если маршрут только для админа — проверяем роль.
  if (adminOnly && user.role !== "admin") {
    return <Navigate to="/" />;
  }

  // Доступ разрешён.
  return children;
}

export default ProtectedRoute;
