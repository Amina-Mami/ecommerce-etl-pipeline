CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id         SERIAL PRIMARY KEY,
    order_id        VARCHAR(50) NOT NULL,
    product_id      INT NOT NULL,
    customer_id     INT,
    quantity        INT NOT NULL,
    unit_price      NUMERIC(10, 2) NOT NULL,
    total_amount    NUMERIC(10, 2) NOT NULL,
    sale_date       DATE NOT NULL,
    source_system   VARCHAR(20) NOT NULL,  
    loaded_at       TIMESTAMP DEFAULT NOW()
);

-- Dimension produit
CREATE TABLE IF NOT EXISTS dim_product (
    product_id      INT PRIMARY KEY,
    product_name    VARCHAR(255),
    category        VARCHAR(100),
    price           NUMERIC(10, 2)
);

-- Dimension client
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id     INT PRIMARY KEY,
    customer_name   VARCHAR(255),
    email           VARCHAR(255),
    country         VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales(product_id);