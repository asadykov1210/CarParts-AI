import { apiRequest } from "./client";

export async function login(email, password) {
  // Отправляем запрос на авторизацию.
  const result = await apiRequest("/auth/login", "POST", { email, password });

  // Сохраняем токен и данные пользователя.
  localStorage.setItem("token", result.access_token);
  localStorage.setItem("user", JSON.stringify(result.user));

  // Уведомляем приложение об изменении состояния авторизации.
  window.dispatchEvent(new Event("auth-change"));
  return result;
}

export function register(email, name, password, phone, city, country) {
  // Регистрация нового пользователя.
  return apiRequest("/auth/register", "POST", {
    email,
    name,
    password,
    phone,
    city,
    country
  });
}

export function updateProfile({ name, password, phone, city, country }) {
  // Обновление профиля пользователя.
  return apiRequest("/auth/update", "PUT", {
    name,
    password,
    phone,
    city,
    country
  });
}
