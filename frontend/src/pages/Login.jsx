import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth";

export default function Login() {
  const navigate = useNavigate();

  // Поля формы
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  // Ошибка авторизации
  const [error, setError] = useState("");

  // Отправка формы
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const data = await login(email, password);
      localStorage.setItem("token", data.access_token);
      navigate("/profile");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="card" style={{ maxWidth: 420, width: "100%" }}>
        <h2 className="text-center text-3xl font-bold mb-6 text-[#D4AF37]">
          Вход в аккаунт
        </h2>

        {error && (
          <div
            className="p-3 rounded-xl mb-4 text-sm"
            style={{ background: "#7F1D1D", color: "#FCA5A5" }}
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-5">
          <div>
            <label className="text-[#D4AF37] mb-1 block">Email</label>
            <input
              type="email"
              className="w-full px-4 py-3 rounded-xl 
                         bg-[#1A1A1A] border border-[#333]
                         text-[#F5F5F5] placeholder-[#777]
                         focus:border-[#D4AF37] focus:ring-2 focus:ring-[#D4AF37] outline-none"
              placeholder="example@mail.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="text-[#D4AF37] mb-1 block">Пароль</label>
            <input
              type="password"
              className="w-full px-4 py-3 rounded-xl 
                         bg-[#1A1A1A] border border-[#333]
                         text-[#F5F5F5] placeholder-[#777]
                         focus:border-[#D4AF37] focus:ring-2 focus:ring-[#D4AF37] outline-none"
              placeholder="Введите пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="w-full py-3 rounded-xl font-semibold 
                       bg-[#D4AF37] text-black 
                       hover:bg-[#b8922f] transition"
          >
            Войти
          </button>
        </form>

        <p className="text-center mt-4 text-[#B3B3B3]">
          Нет аккаунта?{" "}
          <a href="/register" className="text-[#D4AF37] hover:underline">
            Зарегистрироваться
          </a>
        </p>
      </div>
    </div>
  );
}
