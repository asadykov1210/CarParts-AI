import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function AdminDeletedProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Загружаем удалённые товары.
  async function loadProducts() {
    setLoading(true);
    const res = await fetch("http://localhost:8000/admin/products/deleted");
    const data = await res.json();
    setProducts(data);
    setLoading(false);
  }

  // Восстановление товара.
  const handleRestore = async (id) => {
    await fetch(`http://localhost:8000/admin/products/${id}/restore`, {
      method: "POST",
    });
    await loadProducts();
  };

  useEffect(() => {
    // Загружаем список при открытии страницы.
    loadProducts();
  }, []);

  return (
    <div style={{ padding: 20, color: "white" }}>
      <h1>Корзина товаров</h1>

      <button
        onClick={() => navigate("/admin/products")}
        style={{
          background: "transparent",
          border: "1px solid #D4AF37",
          color: "#D4AF37",
          padding: "10px 16px",
          cursor: "pointer",
          borderRadius: 4,
          marginBottom: 20,
        }}
      >
        ← Назад к товарам
      </button>

      {loading ? (
        <div>Загрузка...</div>
      ) : products.length === 0 ? (
        <div>Корзина пуста</div>
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
                <td>{p.name}</td>
                <td>{p.price} ₽</td>
                <td>{p.stock}</td>
                <td>
                  <button
                    onClick={() => handleRestore(p.id)}
                    style={{
                      background: "#2ecc71",
                      border: "none",
                      padding: "6px 10px",
                      cursor: "pointer",
                      color: "white",
                      borderRadius: 4,
                    }}
                  >
                    Восстановить
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
