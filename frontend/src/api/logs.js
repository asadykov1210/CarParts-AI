import { apiRequest } from "./client";

export function getAdminLogs() {
  // Получаем логи администратора.
  return apiRequest("/admin/logs", "GET");
}
