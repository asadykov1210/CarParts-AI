import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { apiRequest } from "../api/client";
import { CATEGORY_LABELS, SUBCATEGORY_LABELS } from "../utils/categoryLabels";
import ProductReviews from "../components/ProductReviews"; // <-- добавили

export default function PartPage() {
  const { part_number } = useParams();
  const navigate = useNavigate();

  const [part, setPart] = useState(null);
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Загружаем данные детали и товара
  const loadPart = async () => {
    try {
      setLoading(true);

      // Деталь из каталога
      const data = await apiRequest(`/api/catalog/${part_number}`, "GET");

      setPart({
        part_number: data.part_number,
        name: data.part_name,
        brand: data.brand,
        category: data.category,
        sub_category: data.sub_category,
        oem: data.oem,
        model: data.model,
        engine: data.engine,
        year: data.year,
      });

      // Товар магазина
      const prod = await apiRequest(`/api/product/by-part/${part_number}`, "GET");
      setProduct(prod);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Добавление в корзину
  const addToCart = async () => {
    if (!product) return;

    try {
      await apiRequest(`/cart/add/${product.id}`, "POST");
      alert("Товар добавлен в корзину!");
    } catch (err) {
      alert(err.message);
    }
  };

  useEffect(() => {
    loadPart();
  }, [part_number]);

  if (loading) return <div style={{ color: "#ccc" }}>Загрузка...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;
  if (!part) return <div style={{ color: "#ccc" }}>Деталь не найдена</div>;

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", color: "#F5F5F5" }}>
      <h1 style={{ fontSize: 32, marginBottom: 20, color: "#D4AF37" }}>
        {part.name}
      </h1>

      <div
        style={{
          background: "#1A1A1A",
          padding: 20,
          borderRadius: 12,
          border: "1px solid #333",
        }}
      >
        <p><strong>Артикул:</strong> {part.part_number}</p>
        <p><strong>Бренд:</strong> {part.brand}</p>

        <p>
          <strong>Категория:</strong>{" "}
          {CATEGORY_LABELS[part.category] || part.category}
        </p>

        <p>
          <strong>Подкатегория:</strong>{" "}
          {SUBCATEGORY_LABELS[part.sub_category] || part.sub_category}
        </p>

        <p><strong>OEM:</strong> {part.oem ? "Да" : "Нет"}</p>
        <p><strong>Модель авто:</strong> {part.model}</p>
        <p><strong>Двигатель:</strong> {part.engine}</p>
        <p><strong>Год:</strong> {part.year}</p>
      </div>

      {/* ==== БЛОК ТОВАРА МАГАЗИНА ==== */}
      <div
        style={{
          marginTop: 30,
          padding: 20,
          background: "#111",
          borderRadius: 12,
          border: "1px solid #333",
        }}
      >
        <h2 style={{ color: "#D4AF37", marginBottom: 10 }}>Товар в магазине</h2>

        {!product && (
          <p style={{ color: "#aaa" }}>
            Этот артикул пока не добавлен в магазин.
          </p>
        )}

        {product && (
          <>
            <p><strong>Цена:</strong> {product.price} ₽</p>
            <p>
              <strong>Наличие:</strong>{" "}
              {product.stock > 0 ? `${product.stock} шт.` : "Нет в наличии"}
            </p>

            {product.stock > 0 && (
              <button
                onClick={addToCart}
                style={{
                  marginTop: 15,
                  padding: "10px 16px",
                  background: "#D4AF37",
                  color: "#000",
                  border: "none",
                  borderRadius: 8,
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                Добавить в корзину
              </button>
            )}

            <button
              onClick={() => navigate("/cart")}
              style={{
                marginTop: 15,
                marginLeft: 10,
                padding: "10px 16px",
                background: "#D4AF37",
                color: "#000",
                border: "none",
                borderRadius: 8,
                cursor: "pointer",
                fontWeight: 600,
              }}
            >
              Перейти в корзину
            </button>
          </>
        )}
      </div>

      {/* ==== ОТЗЫВЫ ==== */}
      {product && (
        <ProductReviews productId={product.id} />
      )}

      <a
        href="/catalog"
        style={{
          display: "inline-block",
          marginTop: 20,
          background: "#D4AF37",
          color: "#000",
          padding: "10px 16px",
          borderRadius: 8,
          textDecoration: "none",
          fontWeight: 600,
        }}
      >
        ← Назад в каталог
      </a>
    </div>
  );
}
