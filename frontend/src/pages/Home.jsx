export default function Home() {
  return (
    <div
      style={{
        minHeight: "80vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        padding: "0 24px",
      }}
    >
      <h1 style={{ fontSize: 48, fontWeight: 800, marginBottom: 20, color: "#D4AF37" }}>
        CarParts AI
      </h1>

      <p
        style={{
          fontSize: 20,
          color: "#B3B3B3",
          maxWidth: 700,
          marginBottom: 40,
        }}
      >
        Умный ассистент для подбора автозапчастей.  
        Введите VIN, ищите детали в каталоге или общайтесь с AI‑помощником.
      </p>

      <div style={{ display: "flex", gap: 20, flexWrap: "wrap", justifyContent: "center" }}>
        <a
          href="/vin"
          style={{
            padding: "14px 28px",
            background: "#D4AF37",
            color: "#000",
            borderRadius: 10,
            fontSize: 18,
            fontWeight: 600,
            textDecoration: "none",
          }}
        >
          VIN‑поиск
        </a>

        <a
          href="/catalog"
          style={{
            padding: "14px 28px",
            background: "#D4AF37",
            color: "#000",
            borderRadius: 10,
            fontSize: 18,
            fontWeight: 600,
            textDecoration: "none",
          }}
        >
          Каталог
        </a>

        <a
          href="/assistant"
          style={{
            padding: "14px 28px",
            background: "#D4AF37",
            color: "#000",
            borderRadius: 10,
            fontSize: 18,
            fontWeight: 600,
            textDecoration: "none",
          }}
        >
          Ассистент
        </a>
      </div>
    </div>
  );
}
