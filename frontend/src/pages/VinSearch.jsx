import { useState } from "react";

export default function VinSearch() {
  // Поле ввода VIN
  const [vin, setVin] = useState("");
  // Результат поиска
  const [data, setData] = useState(null);
  // Ошибка запроса
  const [error, setError] = useState("");

  // Поиск по VIN
  const handleSearch = async () => {
    setError("");
    setData(null);

    try {
      const response = await fetch(`http://localhost:8000/api/vin/${vin}`);
      if (!response.ok) throw new Error("Ошибка при запросе");

      const result = await response.json();

      // Нормализуем, чтобы не было undefined
      setData({
        vin: result.vin || vin,
        make: result.make || "Нет данных",
        model: result.model || "Нет данных",
        year: result.year || "Нет данных",
        trim: result.trim || "Нет данных",
        engine: result.engine || "Нет данных",
        fuel: result.fuel || "Нет данных",
        drive: result.drive || "Нет данных",
        body: result.body || "Нет данных",
      });
    } catch {
      setError("Не удалось получить данные");
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto" }}>
      <h1 style={{ fontSize: 32, marginBottom: 20, color: "#D4AF37" }}>
        VIN поиск
      </h1>

      <div className="flex flex-col gap-3">
        <input
          type="text"
          value={vin}
          onChange={(e) => setVin(e.target.value)}
          placeholder="Введите VIN"
          className="w-full px-4 py-3 rounded-xl 
                     bg-[#1A1A1A] border border-[#333]
                     text-[#F5F5F5] placeholder-[#777]
                     focus:border-[#D4AF37] focus:ring-2 focus:ring-[#D4AF37] outline-none"
        />

        <button
          onClick={handleSearch}
          className="w-full py-3 rounded-xl font-semibold 
                     bg-[#D4AF37] text-black hover:bg-[#b8922f] transition"
        >
          Искать
        </button>
      </div>

      {error && (
        <p style={{ color: "#FF4D4D", marginTop: 12, fontSize: 14 }}>{error}</p>
      )}

      {data && (
        <div className="card" style={{ marginTop: 24 }}>
          <h2 style={{ marginBottom: 16, fontSize: 24, color: "#D4AF37" }}>
            Информация об автомобиле
          </h2>

          <div style={{ fontSize: 16, marginBottom: 8 }}>
            <span style={{ color: "#B3B3B3" }}>VIN:</span> {data.vin}
          </div>

          <div style={{ fontSize: 16, marginBottom: 8 }}>
            <span style={{ color: "#B3B3B3" }}>Марка:</span> {data.make}
          </div>

          <div style={{ fontSize: 16, marginBottom: 8 }}>
            <span style={{ color: "#B3B3B3" }}>Модель:</span> {data.model}
          </div>

          <div style={{ fontSize: 16, marginBottom: 8 }}>
            <span style={{ color: "#B3B3B3" }}>Год выпуска:</span> {data.year}
          </div>

          <div style={{ fontSize: 16, marginBottom: 8 }}>
            <span style={{ color: "#B3B3B3" }}>Комплектация:</span> {data.trim}
          </div>

          <div style={{ fontSize: 16, marginBottom: 8 }}>
            <span style={{ color: "#B3B3B3" }}>Двигатель:</span> {data.engine}
          </div>

          <div style={{ fontSize: 16, marginBottom: 8 }}>
            <span style={{ color: "#B3B3B3" }}>Тип топлива:</span> {data.fuel}
          </div>

          <div style={{ fontSize: 16, marginBottom: 8 }}>
            <span style={{ color: "#B3B3B3" }}>Привод:</span> {data.drive}
          </div>

          <div style={{ fontSize: 16, marginBottom: 8 }}>
            <span style={{ color: "#B3B3B3" }}>Кузов:</span> {data.body}
          </div>
        </div>
      )}
    </div>
  );
}
