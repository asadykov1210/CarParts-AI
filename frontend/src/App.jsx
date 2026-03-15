import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import VinSearch from "./pages/VinSearch";
import Catalog from "./pages/Catalog";
import EditProfile from "./pages/EditProfile";
import Assistant from "./pages/Assistant";
import PartPage from "./pages/PartPage";

import AdminProducts from "./pages/admin/AdminProducts";
import EditProductPage from "./pages/admin/EditProductPage";
import CreateProductPage from "./pages/admin/CreateProductPage";
import AdminDeletedProducts from "./pages/admin/AdminDeletedProducts";
import AdminLogsPage from "./pages/admin/AdminLogsPage";
import ManagerRequests from "./pages/admin/ManagerRequests";

import CartPage from "./pages/CartPage";
import CheckoutPage from "./pages/CheckoutPage";
import OrderSuccessPage from "./pages/OrderSuccessPage";
import OrdersPage from "./pages/OrdersPage";
import OrderDetailsPage from "./pages/OrderDetailsPage";

function App() {
  return (
    <BrowserRouter>
      {/* Toast уведомления */}
      <Toaster position="top-right" />

      <Navbar />

      <div style={{ padding: "24px" }}>
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />

          <Route
            path="/profile/edit"
            element={
              <ProtectedRoute>
                <EditProfile />
              </ProtectedRoute>
            }
          />

          <Route
            path="/vin"
            element={
              <ProtectedRoute>
                <VinSearch />
              </ProtectedRoute>
            }
          />

          <Route
            path="/catalog"
            element={
              <ProtectedRoute>
                <Catalog />
              </ProtectedRoute>
            }
          />

          <Route
            path="/assistant"
            element={
              <ProtectedRoute>
                <Assistant />
              </ProtectedRoute>
            }
          />

          <Route
            path="/catalog/:part_number"
            element={
              <ProtectedRoute>
                <PartPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin/products"
            element={
              <ProtectedRoute adminOnly={true}>
                <AdminProducts />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin/products/:id"
            element={
              <ProtectedRoute adminOnly={true}>
                <EditProductPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin/products/new"
            element={
              <ProtectedRoute adminOnly={true}>
                <CreateProductPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin/products/deleted"
            element={
              <ProtectedRoute adminOnly={true}>
                <AdminDeletedProducts />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin/logs"
            element={
              <ProtectedRoute adminOnly={true}>
                <AdminLogsPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin/manager-requests"
            element={
              <ProtectedRoute adminOnly={true}>
                <ManagerRequests />
              </ProtectedRoute>
            }
          />

          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/order-success/:id" element={<OrderSuccessPage />} />
          <Route path="/orders" element={<OrdersPage />} />
          <Route path="/orders/:id" element={<OrderDetailsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
