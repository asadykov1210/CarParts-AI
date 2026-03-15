import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function AdminProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Загружаем список товаров.
  async function loadProducts() {
    setLoading(true);
    const res = await fetch("http://localhost:8000/admin/products");
    const data = await res.json();
    setProducts(data);
    setLoading(false);
  }

  // Синхронизация с внешним каталогом.
  async function syncProducts() {
    await fetch("http://localhost:8000/admin/sync-products", {
      method: "POST",
    });
    await loadProducts();
    alert("Синхронизация завершена!");
  }

  // Полное удаление товара.
  const handleDelete = async (id) => {
    if (!window.confirm("Удалить товар полностью?")) return;

    await fetch(`http://localhost:8000/admin/products/${id}`, {
      method: "DELETE",
    });

    await loadProducts();
  };

  useEffect(() => {
    // Загружаем товары при открытии страницы.
    loadProducts();
  }, []);

  return (
    <div style={{ padding: "20px", color: "white" }}>
      <h1>Админ‑панель — Товары</h1>

      {/* Верхняя панель кнопок */}
      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <button
          onClick={() => navigate("/admin/products/new")}
          style={{
            background: "#D4AF37",
            color: "black",
            padding: "10px 20px",
            border: "none",
            cursor: "pointer",
            fontWeight: 600,
            borderRadius: 4,
          }}
        >
          + Добавить товар
        </button>

        <button
          onClick={syncProducts}
          style={{
            background: "#D4AF37",
            color: "black",
            padding: "10px 20px",
            border: "none",
            cursor: "pointer",
            fontWeight: 600,
            borderRadius: 4,
          }}
        >
          Синхронизировать с каталогом
        </button>

        <Link
          to="/admin/logs"
          style={{
            background: "#D4AF37",
            color: "black",
            padding: "10px 20px",
            borderRadius: 4,
            textDecoration: "none",
            display: "flex",
            alignItems: "center",
            fontWeight: 600,
          }}
        >
          История изменений
        </Link>

        <Link
          to="/admin/manager-requests"
          style={{
            background: "#D4AF37",
            color: "black",
            padding: "10px 20px",
            borderRadius: 4,
            textDecoration: "none",
            display: "flex",
            alignItems: "center",
            fontWeight: 600,
          }}
        >
          Запросы менеджеру
        </Link>
      </div>

      {loading ? (
        <div>Загрузка...</div>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid #555" }}>
              <th>ID</th>
              <th>Артикул</th>
              <th>Название</th>
              <th>Цена</th>
              <th>Наличие</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            {products.map((p) => (
              <tr key={p.id} style={{ borderBottom: "1px solid #333" }}>
                <td>{p.id}</td>
                <td>{p.part_number}</td>
                <td>{p.part_name}</td> {/* ← исправлено */}
                <td>{p.price} ₽</td>
                <td>{p.stock}</td>
                <td>
                  <Link
                    to={`/admin/products/${p.id}`}
                    style={{ color: "#D4AF37", marginRight: 10 }}
                  >
                    Редактировать
                  </Link>
                  <button
                    onClick={() => handleDelete(p.id)}
                    style={{
                      background: "red",
                      border: "none",
                      padding: "6px 10px",
                      cursor: "pointer",
                      color: "white",
                      borderRadius: 4,
                    }}
                  >
                    X
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default AdminProducts;
