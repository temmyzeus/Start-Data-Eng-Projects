CREATE TABLE IF NOT EXISTS user_purchases (
    invoice_number VARCHAR,
    stock_code VARCHAR,
    description VARCHAR,
    quantity INTEGER,
    invoice_date TIMESTAMP,
    unit_price DECIMAL,
    customer_id INTEGER,
    country VARCHAR
);

COPY user_purchases
FROM '/data/OnlineRetail.csv' WITH (FORMAT CSV, DELIMITER ',', HEADER);
