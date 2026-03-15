import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getAdminLogs } from "../../api/logs";

// Цветовая подсветка строк по типу действия.
function getRowStyle(action) {
  switch (action) {
    case "CREATE":
    case "CREATE_SYNC":
      return { background: "rgba(0, 255, 0, 0.15)" };
    case "UPDATE":
      return { background: "rgba(255, 255, 0, 0.15)" };
    case "DELETE":
      return { background: "rgba(255, 0, 0, 0.15)" };
    default:
      return {};
  }
}

export default function AdminLogsPage() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    // Загружаем историю изменений
    getAdminLogs().then(setLogs);
  }, []);

  return (
    <div style={{ padding: 20, color: "white" }}>
      <h1>История изменений</h1>

      <Link
        to="/admin/products"
        style={{
          display: "inline-block",
          marginBottom: 20,
          background: "transparent",
          border: "1px solid #D4AF37",
          color: "#D4AF37",
          padding: "8px 16px",
          borderRadius: 4,
          textDecoration: "none",
          fontWeight: 600,
        }}
      >
        ← Назад к админ-панели
      </Link>

      <table
        border="1"
        cellPadding="8"
        style={{ width: "100%", marginTop: 10, borderCollapse: "collapse" }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Действие</th>
            <th>ID товара</th>
            <th>До</th>
            <th>После</th>
            <th>Дата</th>
          </tr>
        </thead>

        <tbody>
          {logs.map((log) => (
            <tr key={log.id} style={getRowStyle(log.action)}>
              <td>{log.id}</td>
              <td>{log.action}</td>
              <td>{log.product_id}</td>
              <td>
                <pre style={{ whiteSpace: "pre-wrap" }}>{log.before}</pre>
              </td>
              <td>
                <pre style={{ whiteSpace: "pre-wrap" }}>{log.after}</pre>
              </td>
              <td>{new Date(log.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
