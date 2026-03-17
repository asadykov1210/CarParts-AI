import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CartPage() {
  const [cart, setCart] = useState([]);
  const navigate = useNavigate();

  // Стиль кнопок управления количеством.
  const buttonStyle = {
    background: "#D4AF37",
    color: "#000",
    padding: "10px 18px",
    borderRadius: "6px",
    fontWeight: "bold",
    cursor: "pointer",
    boxShadow: "0 0 10px rgba(212, 175, 55, 0.4)",
    transition: "0.2s",
  };

  
  const backButtonStyle = {
    background: "#D4AF37",
    color: "#000",
    padding: "8px 14px",
    borderRadius: "6px",
    fontWeight: "bold",
    cursor: "pointer",
    fontSize: "14px",
  };

  // Загружаем корзину.
  const loadCart = () => {
    fetch("http://localhost:8000/cart", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    })
      .then(res => res.json())
      .then(data => setCart(data));
  };

  useEffect(() => {
    loadCart();
  }, []);

  // Увеличить количество.
  const increase = (productId) => {
    fetch(`http://localhost:8000/cart/add/${productId}`, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    }).then(loadCart);
  };

  // Уменьшить количество.
  const decrease = (itemId) => {
    fetch(`http://localhost:8000/cart/remove/${itemId}`, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    }).then(loadCart);
  };

  // Переход к оформлению.
  const goToCheckout = () => {
    navigate("/checkout");
  };

  if (!cart || cart.length === 0) {
    return (
      <div className="text-white text-center mt-10 text-xl">
        Корзина пуста
        <div className="mt-4">
          <button
            onClick={() => navigate(-1)}
            style={backButtonStyle}
          >
            ← Назад
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="text-white p-6 max-w-2xl mx-auto">

      <button
        onClick={() => navigate(-1)}
        style={{ ...backButtonStyle, marginBottom: "20px" }}
      >
        ← Назад
      </button>

      <h1 className="text-2xl mb-4">Корзина</h1>

      <div className="space-y-4">
        {cart.map(item => (
          <div
            key={item.id}
            className="bg-[#111] p-4 rounded flex justify-between items-center"
            style={{ border: "1px solid #333" }}
          >
            <div>
              <div className="text-lg">{item.product.name}</div>
              <div className="text-sm text-gray-400">
                {item.product.price} ₽ × {item.quantity}
              </div>
            </div>

            <div className="flex items-center gap-3">

              <button
                onClick={() => decrease(item.id)}
                style={buttonStyle}
              >
                –
              </button>

              <span className="text-lg">{item.quantity}</span>

              <button
                onClick={() => increase(item.product.id)}
                style={buttonStyle}
              >
                +
              </button>

              <div className="text-lg font-bold w-20 text-right">
                {item.product.price * item.quantity} ₽
              </div>
            </div>
          </div>
        ))}
      </div>

      <button
        onClick={goToCheckout}
        style={{
          ...buttonStyle,
          width: "100%",
          marginTop: "24px",
          fontSize: "18px",
        }}
      >
        Перейти к оформлению заказа →
      </button>
    </div>
  );
}
