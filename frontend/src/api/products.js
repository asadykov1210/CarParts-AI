import { apiRequest } from "./client";

export function getProduct(id) {
  // Получаем данные товара по ID.
  return apiRequest(`/admin/products/${id}`, "GET");
}

export function updateProduct(id, data) {
  // Обновляем данные товара.
  return apiRequest(`/admin/products/${id}`, "PUT", data);
}

export function createProduct(data) {
  // Создаём новый товар.
  return apiRequest("/admin/products", "POST", data);
}

export function deleteProduct(id) {
  // Удаляем товар по ID.
  return apiRequest(`/admin/products/${id}`, "DELETE");
}
