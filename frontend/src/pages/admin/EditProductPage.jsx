import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getProduct, updateProduct } from "../../api/products";

export default function EditProductPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [product, setProduct] = useState(null);

  useEffect(() => {
    // Загружаем данные товара.
    getProduct(id).then((data) => {
      setProduct({
        name: data.part_name,
        article: data.part_number,
        brand: data.brand || "",
        model: data.model || "",
        year: data.year || "",
        engine: data.engine || "",
        category: data.category || "",
        sub_category: data.sub_category || "",
        oem: data.oem || "",
        vin: data.vin || "",
        price: data.price,
        stock: data.stock,
      });
    });
  }, [id]);

  if (!product) return <div style={{ color: "white" }}>Загрузка...</div>;

  // Сохранение изменений.
  const handleSave = async () => {
    await updateProduct(id, {
      part_name: product.name,
      part_number: product.article,
      brand: product.brand,
      model: product.model,
      year: Number(product.year),
      engine: product.engine,
      category: product.category,
      sub_category: product.sub_category,
      oem: product.oem,
      vin: product.vin,
      price: Number(product.price),
      stock: Number(product.stock),
    });

    navigate("/admin/products");
  };

  // Универсальный компонент поля ввода.
  const input = (key, label, type = "text") => (
    <label style={{ display: "flex", flexDirection: "column", color: "#D4AF37" }}>
      {label}
      <input
        type={type}
        value={product[key]}
        onChange={(e) => setProduct({ ...product, [key]: e.target.value })}
        style={{
          width: "100%",
          padding: "10px 12px",
          borderRadius: "10px",
          border: "1px solid #333",
          background: "#1A1A1A",
          color: "#F5F5F5",
          marginTop: 6,
        }}
      />
    </label>
  );

  return (
    <div style={{ padding: 24, color: "white" }}>
      <h1 style={{ fontSize: 28, marginBottom: 20, color: "#D4AF37" }}>
        Редактирование товара #{id}
      </h1>

      <div style={{ display: "flex", flexDirection: "column", gap: 16, maxWidth: 400 }}>
        {input("name", "Название")}
        {input("article", "Артикул")}
        {input("brand", "Бренд")}
        {input("model", "Модель авто")}
        {input("year", "Год", "number")}
        {input("engine", "Двигатель")}
        {input("category", "Категория")}
        {input("sub_category", "Подкатегория")}
        {input("oem", "OEM")}
        {input("vin", "VIN")}
        {input("price", "Цена", "number")}
        {input("stock", "Наличие", "number")}

        <div style={{ display: "flex", justifyContent: "space-between", marginTop: 20 }}>
          <button
            onClick={() => navigate("/admin/products")}
            style={{
              background: "transparent",
              border: "1px solid #D4AF37",
              color: "#D4AF37",
              padding: "10px 16px",
              cursor: "pointer",
              borderRadius: 8,
            }}
          >
            ← Назад
          </button>

          <button
            onClick={handleSave}
            style={{
              background: "#D4AF37",
              border: "none",
              padding: "10px 20px",
              cursor: "pointer",
              fontWeight: 600,
              borderRadius: 8,
              color: "black",
            }}
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
  );
}
