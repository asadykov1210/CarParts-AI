CREATE DATABASE carparts_ai;
USE carparts_ai;

SET FOREIGN_KEY_CHECKS = 0;

-- ============================
-- TABLE: users
-- ============================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(255),
    password_hash VARCHAR(255),
    role VARCHAR(50),
    phone VARCHAR(50),
    city VARCHAR(100),
    country VARCHAR(100)
) ENGINE=InnoDB;

-- ============================
-- TABLE: parts
-- ============================
CREATE TABLE IF NOT EXISTS parts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vin VARCHAR(255),
    brand VARCHAR(255),
    model VARCHAR(255),
    year INT,
    engine VARCHAR(255),
    category VARCHAR(255),
    sub_category VARCHAR(255),
    part_number VARCHAR(255),
    part_name VARCHAR(255),
    oem VARCHAR(255),
    price FLOAT,
    stock INT
) ENGINE=InnoDB;

-- ============================
-- TABLE: admin_logs
-- ============================
CREATE TABLE IF NOT EXISTS admin_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(255) NOT NULL,
    product_id INT,
    `before` TEXT,
    `after` TEXT,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (product_id) REFERENCES parts(id)
) ENGINE=InnoDB;

-- ============================
-- TABLE: cart_items
-- ============================
CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT,
    FOREIGN KEY (product_id) REFERENCES parts(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

-- ============================
-- TABLE: orders
-- ============================
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    user_order_number INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    payment_method VARCHAR(255),
    status VARCHAR(255),
    total_amount FLOAT NOT NULL,
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

-- ============================
-- TABLE: order_items
-- ============================
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    product_name VARCHAR(255),
    quantity INT,
    price_at_moment FLOAT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES parts(id)
) ENGINE=InnoDB;

-- ============================
-- TABLE: reviews
-- ============================
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(255),
    FOREIGN KEY (product_id) REFERENCES parts(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

-- ============================
-- INDEXES
-- ============================
CREATE INDEX idx_admin_logs_id ON admin_logs(id);
CREATE INDEX idx_cart_items_id ON cart_items(id);
CREATE INDEX idx_orders_id ON orders(id);
CREATE INDEX idx_parts_part_number ON parts(part_number);
CREATE INDEX idx_parts_vin ON parts(vin);
CREATE INDEX idx_reviews_id ON reviews(id);
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_id ON users(id);

SET FOREIGN_KEY_CHECKS = 1;
