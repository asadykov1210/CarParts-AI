import { useState } from "react";
import { register } from "../api/auth";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();

  // Поля формы
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [phone, setPhone] = useState("");
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");

  // Ошибка регистрации
  const [error, setError] = useState("");

  // Отправка формы
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await register(email, name, password, phone, city, country);
      navigate("/login"); // переход после успешной регистрации
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="flex justify-center mt-20">
      <div
        className="w-full max-w-md rounded-2xl p-8 shadow-xl"
        style={{
          background: "#111",
          border: "1px solid #D4AF37", // 🔥 ЗОЛОТАЯ РАМКА
        }}
      >
        <h1 className="text-3xl font-bold text-center mb-6 text-[#D4AF37]">
          Регистрация
        </h1>

        {error && (
          <div className="bg-[#7F1D1D] text-[#FCA5A5] p-3 rounded-xl mb-4 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">

          <div>
            <label className="text-[#D4AF37] text-sm">Имя</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333]
                         text-[#F5F5F5] placeholder-[#777] focus:border-[#D4AF37]
                         focus:ring-2 focus:ring-[#D4AF37] outline-none mt-1"
              placeholder="Ваше имя"
              required
            />
          </div>

          <div>
            <label className="text-[#D4AF37] text-sm">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333]
                         text-[#F5F5F5] placeholder-[#777] focus:border-[#D4AF37]
                         focus:ring-2 focus:ring-[#D4AF37] outline-none mt-1"
              placeholder="example@mail.com"
              required
            />
          </div>

          <div>
            <label className="text-[#D4AF37] text-sm">Пароль</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333]
                         text-[#F5F5F5] placeholder-[#777] focus:border-[#D4AF37]
                         focus:ring-2 focus:ring-[#D4AF37] outline-none mt-1"
              placeholder="Введите пароль"
              required
            />
          </div>

          <div>
            <label className="text-[#D4AF37] text-sm">Телефон</label>
            <input
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333]
                         text-[#F5F5F5] placeholder-[#777] focus:border-[#D4AF37]
                         focus:ring-2 focus:ring-[#D4AF37] outline-none mt-1"
              placeholder="+7 900 000 00 00"
            />
          </div>

          <div>
            <label className="text-[#D4AF37] text-sm">Город</label>
            <input
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333]
                         text-[#F5F5F5] placeholder-[#777] focus:border-[#D4AF37]
                         focus:ring-2 focus:ring-[#D4AF37] outline-none mt-1"
              placeholder="Ваш город"
            />
          </div>

          <div>
            <label className="text-[#D4AF37] text-sm">Страна</label>
            <input
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-[#1A1A1A] border border-[#333]
                         text-[#F5F5F5] placeholder-[#777] focus:border-[#D4AF37]
                         focus:ring-2 focus:ring-[#D4AF37] outline-none mt-1"
              placeholder="Ваша страна"
            />
          </div>

          <button
            type="submit"
            className="w-full py-3 rounded-xl font-semibold bg-[#D4AF37]
                       text-black hover:bg-[#b8922f] transition mt-2"
          >
            Создать аккаунт
          </button>
        </form>

        <p className="text-center text-[#888] text-sm mt-4">
          Уже есть аккаунт?{" "}
          <a href="/login" className="text-[#D4AF37] hover:underline">
            Войти
          </a>
        </p>
      </div>
    </div>
  );
}
