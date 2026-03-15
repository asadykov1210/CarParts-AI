import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CheckoutPage() {
  const navigate = useNavigate();
  const [cart, setCart] = useState([]);
  const [total, setTotal] = useState(0);

  // Данные покупателя
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");

  const [paymentMethod, setPaymentMethod] = useState("card");

  useEffect(() => {
    // Данные покупателя
    fetch("http://localhost:8000/cart/my", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    })
      .then(res => res.json())
      .then(data => {
        setCart(data);
        // Подсчёт итоговой суммы
        let sum = 0;
        data.forEach(item => {
          sum += item.product.price * item.quantity;
        });
        setTotal(sum);
      });
  }, []);

  // Отправка заказа
  const submitOrder = async () => {
    const body = {
      name,
      phone,
      email,
      address,
      payment_method: paymentMethod,
    };

    const res = await fetch("http://localhost:8000/orders/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
      body: JSON.stringify(body),
    });

    const data = await res.json();

    if (data.order_id) {
      navigate(`/orders/${data.order_id}`);
    }
  };

  return (
    <div className="text-white p-6 max-w-2xl mx-auto">

      <button
        onClick={() => navigate("/cart")}
        style={{
          background: "#D4AF37",
          color: "#000",
          padding: "10px 16px",
          borderRadius: "6px",
          fontWeight: "bold",
          marginBottom: "20px",
        }}
      >
        ← Назад
      </button>

      <h1 className="text-2xl mb-4">Оформление заказа</h1>

      {/* Товары */}
      <h2 className="text-xl mb-2">Ваши товары</h2>

      <div className="space-y-3 mb-6">
        {cart.map((item, index) => (
          <div
            key={index}
            className="bg-[#111] p-4 rounded border border-gray-700 flex justify-between"
          >
            <div>
              <div className="text-lg">{item.product.name}</div>
              <div className="text-gray-400">
                {item.quantity} × {item.product.price} ₽
              </div>
            </div>

            <div className="text-lg font-bold">
              {item.product.price * item.quantity} ₽
            </div>
          </div>
        ))}
      </div>

      <div className="text-xl font-bold mb-6">
        Итоговая сумма: {total} ₽
      </div>

      {/* Данные пользователя */}
      <h2 className="text-xl mb-2">Ваши данные</h2>

      <input
        className="w-full p-2 mb-3 bg-[#111] border border-gray-700 rounded"
        placeholder="Имя"
        value={name}
        onChange={e => setName(e.target.value)}
      />

      <input
        className="w-full p-2 mb-3 bg-[#111] border border-gray-700 rounded"
        placeholder="Телефон"
        value={phone}
        onChange={e => setPhone(e.target.value)}
      />

      <input
        className="w-full p-2 mb-3 bg-[#111] border border-gray-700 rounded"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />

      <input
        className="w-full p-2 mb-3 bg-[#111] border border-gray-700 rounded"
        placeholder="Адрес"
        value={address}
        onChange={e => setAddress(e.target.value)}
      />

      {/* Метод оплаты */}
      <h2 className="text-xl mb-2 mt-4">Метод оплаты</h2>

      <label className="flex items-center gap-2 mb-2">
        <input
          type="radio"
          name="payment"
          value="Оплата картой"
          checked={paymentMethod === "Оплата картой"}
          onChange={() => setPaymentMethod("Оплата картой")}
        />
        Оплата картой
      </label>

      <label className="flex items-center gap-2 mb-2">
        <input
          type="radio"
          name="payment"
          value="cНаличными при полученииash"
          checked={paymentMethod === "Наличными при получении"}
          onChange={() => setPaymentMethod("Наличными при получении")}
        />
        Наличными при получении
      </label>

      <label className="flex items-center gap-2 mb-4">
        <input
          type="radio"
          name="payment"
          value="Онлайн‑оплата"
          checked={paymentMethod === "Онлайн‑оплата"}
          onChange={() => setPaymentMethod("Онлайн‑оплата")}
        />
        Онлайн‑оплата
      </label>

      {/* Кнопка подтверждения */}
      <button
        onClick={submitOrder}
        style={{
          background: "#D4AF37",
          color: "#000",
          padding: "12px 20px",
          borderRadius: "6px",
          fontWeight: "bold",
          width: "100%",
          marginTop: "10px",
        }}
      >
        Подтвердить заказ →
      </button>
    </div>
  );
}
