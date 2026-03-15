import { useNavigate } from "react-router-dom";

export default function AddToCartHandler({ product }) {
  const navigate = useNavigate();

  // Добавление товара в корзину
  async function handleAddToCart() {
    await fetch(`http://localhost:8000/cart/add/${product.id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });

    // Переход в корзину после добавления
    navigate("/cart");
  }

  return (
    <button onClick={handleAddToCart}>
      Добавить в корзину
    </button>
  );
}
