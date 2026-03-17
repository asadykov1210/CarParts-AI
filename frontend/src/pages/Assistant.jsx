import { useState } from "react";
import toast from "react-hot-toast";

export default function Assistant() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Вызов менеджера вручную или по триггеру.
  const callManager = async () => {
    try {
      const user = JSON.parse(localStorage.getItem("user"));

      if (!user) {
        toast.error("Пользователь не авторизован");
        return;
      }

      const res = await fetch("http://localhost:8000/assistant/request-manager", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user.id,
          name: user.name,
          email: user.email,
          phone: user.phone,
        }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.reply || "Ваш менеджер свяжется с вами в ближайшее время",
        },
      ]);

      toast.success("Менеджер уведомлён");
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Ошибка вызова менеджера" },
      ]);
      toast.error("Ошибка вызова менеджера");
    }
  };

  // Отправка сообщения ассистенту.
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    const triggers = [
      "менеджер",
      "оператор",
      "живой человек",
      "позвать менеджера",
      "нужен менеджер",
      "хочу поговорить с менеджером",
    ];

    // Автоматический вызов менеджера.
    if (triggers.some((t) => input.toLowerCase().includes(t))) {
      await callManager();
      setInput("");
      return;
    }

    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      const botMessage = {
        role: "assistant",
        text: data.reply || "Ошибка: пустой ответ",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Ошибка соединения с сервером" },
      ]);
      toast.error("Ошибка соединения с сервером");
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 20 }}>
      <h1 style={{ fontSize: 32, marginBottom: 20, color: "#D4AF37" }}>
        AI‑ассистент
      </h1>

      <div
        className="card"
        style={{
          height: "60vh",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 16,
        }}
      >
        {messages.length === 0 && (
          <p style={{ color: "#777", textAlign: "center", marginTop: 20 }}>
            Начните диалог — ассистент готов помочь
          </p>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
              background: msg.role === "user" ? "#D4AF37" : "#1A1A1A",
              color: msg.role === "user" ? "#000" : "#F5F5F5",
              padding: "10px 14px",
              borderRadius: 10,
              maxWidth: "75%",
              border:
                msg.role === "assistant"
                  ? "1px solid #333"
                  : "1px solid #b8922f",
            }}
          >
            {msg.text}
          </div>
        ))}

        {loading && (
          <div
            style={{
              alignSelf: "flex-start",
              background: "#1A1A1A",
              color: "#777",
              padding: "10px 14px",
              borderRadius: 10,
              border: "1px solid #333",
            }}
          >
            Ассистент печатает…
          </div>
        )}
      </div>

      <div className="flex gap-3 mt-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Введите сообщение..."
          className="w-full px-4 py-3 rounded-xl 
                     bg-[#1A1A1A] border border-[#333]
                     text-[#F5F5F5] placeholder-[#777]
                     focus:border-[#D4AF37] focus:ring-2 focus:ring-[#D4AF37] outline-none"
        />

        <button
          onClick={sendMessage}
          className="px-6 py-3 rounded-xl font-semibold 
                     bg-[#D4AF37] text-black 
                     hover:bg-[#b8922f] transition"
        >
          ➤
        </button>

        <button
          onClick={callManager}
          className="px-6 py-3 rounded-xl font-semibold 
                     bg-[#1A1A1A] text-[#D4AF37] border border-[#D4AF37]
                     hover:bg-[#333] transition"
        >
          Менеджер
        </button>
      </div>
    </div>
  );
}
