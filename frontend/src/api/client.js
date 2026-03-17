const API_URL = "http://localhost:8000";

export async function apiRequest(path, method = "GET", body = null) {
  // Базовые заголовки запроса.
  const headers = {
    "Content-Type": "application/json",
  };

  // Добавляем токен, если пользователь авторизован.
  const token = localStorage.getItem("token");
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Формируем параметры запроса.
  const options = { method, headers };

  // Добавляем тело запроса, если оно есть.
  if (body) {
    options.body = JSON.stringify(body);
  }

  // Выполняем запрос к API.
  const response = await fetch(API_URL + path, options);

  // Обрабатываем ошибку, если статус не успешный.
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Ошибка запроса");
  }

  // Возвращаем JSON‑ответ.
  return response.json();
}
