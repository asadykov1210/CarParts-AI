import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";
import { CATEGORY_LABELS } from "../utils/categoryLabels";

export default function Catalog() {
  const [parts, setParts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  // Фильтры
  const [brandFilter, setBrandFilter] = useState("");
  const [modelFilter, setModelFilter] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");

  // VIN
  const [vin, setVin] = useState("");
  const [vinError, setVinError] = useState("");

  // Загружаем весь каталог при старте
  const loadCatalog = async () => {
    try {
      setLoading(true);
      const data = await apiRequest("/api/catalog", "GET");

      // Безопасная нормализация данных
      const safe = data.map((p) => ({
        part_number: p.part_number || "",
        name: p.part_name || "",
        brand: p.brand || "",
        model: p.model || "",
        category: p.category || "",
        price: p.price || "",
      }));

      setParts(safe);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCatalog();
  }, []);

   // Уникальные значения для фильтров
  const brands = [...new Set(parts.map((p) => p.brand).filter(Boolean))];
  const models = [...new Set(parts.map((p) => p.model).filter(Boolean))];
  const categories = [...new Set(parts.map((p) => p.category).filter(Boolean))];

  // Поиск по VIN
  const handleVinSearch = async () => {
    setVinError("");

    if (!vin || vin.length !== 17) {
      setVinError("Введите корректный VIN (17 символов)");
      return;
    }

    try {
      const data = await apiRequest(`/api/vin/${vin}`, "GET");

      if (!data || !data.make) {
        setVinError("VIN не найден");
        return;
      }

      // Устанавливаем фильтры по VIN
      setBrandFilter(data.make || "");
      setModelFilter(data.model || "");

      // Заменяем каталог деталями по VIN
      setParts(
        data.parts.map((p) => ({
          part_number: p.part_number || "",
          name: p.part_name || "",
          brand: p.brand || "",
          model: p.model || "",
          category: p.category || "",
          price: p.price || "",
        }))
      );

    } catch (err) {
      setVinError("Ошибка при проверке VIN");
    }
  };

  // Фильтрация каталога
  const filtered = parts.filter((p) => {
    const s = search.toLowerCase();

    const matchesSearch =
      p.name.toLowerCase().includes(s) ||
      p.part_number.toLowerCase().includes(s);

    const matchesBrand = brandFilter ? p.brand === brandFilter : true;
    const matchesModel = modelFilter ? p.model === modelFilter : true;
    const matchesCategory = categoryFilter ? p.category === categoryFilter : true;

    return matchesSearch && matchesBrand && matchesModel && matchesCategory;
  });

  return (
    <div style={{ maxWidth: 900, margin: "40px auto" }}>
      <h1 style={{ fontSize: 32, marginBottom: 20, color: "#D4AF37" }}>
        Каталог
      </h1>

      {/* VIN поиск */}
      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <input
          type="text"
          placeholder="Введите VIN..."
          className="px-3 py-2 bg-[#1A1A1A] border border-[#333] text-[#F5F5F5] rounded-lg w-full"
          value={vin}
          onChange={(e) => setVin(e.target.value.toUpperCase())}
        />

        <button
          onClick={handleVinSearch}
          className="px-4 py-2 bg-[#D4AF37] text-black rounded-lg font-semibold"
        >
          Найти по VIN
        </button>
      </div>

      {vinError && (
        <div style={{ color: "#FCA5A5", marginBottom: 10 }}>
          {vinError}
        </div>
      )}

      {/* Фильтры */}
      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <select
          value={brandFilter}
          onChange={(e) => setBrandFilter(e.target.value)}
          className="px-3 py-2 bg-[#1A1A1A] border border-[#333] text-[#F5F5F5] rounded-lg"
        >
          <option value="">Все бренды</option>
          {brands.map((b) => (
            <option key={b} value={b}>{b}</option>
          ))}
        </select>

        <select
          value={modelFilter}
          onChange={(e) => setModelFilter(e.target.value)}
          className="px-3 py-2 bg-[#1A1A1A] border border-[#333] text-[#F5F5F5] rounded-lg"
        >
          <option value="">Все модели</option>
          {models.map((m) => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>

        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="px-3 py-2 bg-[#1A1A1A] border border-[#333] text-[#F5F5F5] rounded-lg"
        >
          <option value="">Все категории</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {CATEGORY_LABELS[c] || c}
            </option>
          ))}
        </select>
      </div>

      {/* Поиск */}
      <input
        type="text"
        placeholder="Поиск по названию или номеру детали..."
        className="w-full px-4 py-3 rounded-xl 
                   bg-[#1A1A1A] border border-[#333]
                   text-[#F5F5F5] placeholder-[#777]
                   focus:border-[#D4AF37] focus:ring-2 focus:ring-[#D4AF37] outline-none mb-6"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {loading && <div style={{ color: "#B3B3B3" }}>Загрузка...</div>}

      {error && (
        <div
          style={{
            background: "#7F1D1D",
            color: "#FCA5A5",
            padding: 12,
            borderRadius: 8,
            marginBottom: 12,
          }}
        >
          {error}
        </div>
      )}

      {/* Карточки */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: 20,
        }}
      >
        {filtered.map((part) => (
          <div key={part.part_number} className="card">
            <h2 style={{ fontSize: 20, marginBottom: 10, color: "#D4AF37" }}>
              {part.name}
            </h2>

            <p style={{ color: "#D1D5DB" }}>
              <strong>Артикул:</strong> {part.part_number}
            </p>

            <p style={{ color: "#D1D5DB" }}>
              <strong>Бренд:</strong> {part.brand}
            </p>

            <p style={{ color: "#D1D5DB" }}>
              <strong>Модель:</strong> {part.model}
            </p>

            <p style={{ color: "#D1D5DB" }}>
              <strong>Категория:</strong> {CATEGORY_LABELS[part.category] || part.category}
            </p>

            <a
              href={`/catalog/${part.part_number}`}
              style={{
                display: "inline-block",
                marginTop: 12,
                background: "#D4AF37",
                color: "#000",
                padding: "8px 14px",
                borderRadius: 8,
                textDecoration: "none",
                fontWeight: 600,
              }}
            >
              Подробнее
            </a>
          </div>
        ))}
      </div>

      {filtered.length === 0 && !loading && (
        <div style={{ color: "#B3B3B3", marginTop: 20 }}>
          Ничего не найдено
        </div>
      )}
    </div>
  );
}
