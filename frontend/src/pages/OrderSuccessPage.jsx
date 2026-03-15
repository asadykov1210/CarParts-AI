import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";

export default function OrderSuccessPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [order, setOrder] = useState(null);

  // Загружаем данные заказа
  useEffect(() => {
    apiRequest(`/orders/${id}`, "GET").then(setOrder);
  }, [id]);

  const buttonStyle = {
    background: "#D4AF37",
    color: "#000",
    padding: "12px 20px",
    borderRadius: "6px",
    fontWeight: "bold",
    cursor: "pointer",
    width: "100%",
    marginTop: "20px",
    fontSize: "18px",
    boxShadow: "0 0 10px rgba(212, 175, 55, 0.4)",
  };

  return (
    <div className="text-white p-6 max-w-xl mx-auto text-center">

      <h1 className="text-3xl mb-6 font-bold">Заказ оформлен!</h1>

      <div className="bg-[#111] p-6 rounded border border-gray-700 mb-6">
        <div className="text-xl mb-2">Спасибо за ваш заказ</div>
        <div className="text-2xl font-bold text-[#D4AF37]">
          № {order?.user_order_number}
        </div>
      </div>

      <button
        style={buttonStyle}
        onClick={() => navigate("/catalog")}
      >
        Вернуться в каталог →
      </button>

      <button
        style={{ ...buttonStyle, marginTop: "12px" }}
        onClick={() => navigate("/orders")}
      >
        Перейти к моим заказам →
      </button>
    </div>
  );
}
