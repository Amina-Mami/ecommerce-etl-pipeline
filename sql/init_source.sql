CREATE TABLE IF NOT EXISTS orders (
    order_id        VARCHAR(50) PRIMARY KEY,
    customer_id     INT,
    product_id      INT,
    quantity        INT,
    unit_price      NUMERIC(10, 2),
    order_date      DATE
);


INSERT INTO orders (order_id, customer_id, product_id, quantity, unit_price, order_date) VALUES
('ORD-1001', 101, 1, 2, 25.99, '2026-08-01'),
('ORD-1002', 102, 3, 1, 89.50, '2026-08-02'),
('ORD-1003', 101, 2, 3, 12.00, '2026-08-03'),
('ORD-1004', 103, 5, 1, 199.99, '2026-08-04'),
('ORD-1005', 104, 1, 5, 25.99, '2026-08-05')
ON CONFLICT (order_id) DO NOTHING;