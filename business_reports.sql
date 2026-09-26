-- =========================================================
-- BUSINESS REPORTS
-- API-to-PostgreSQL Data Pipeline
-- =========================================================


-- =========================================================
-- 1. CUSTOMER ORDER REPORT
-- =========================================================

SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity) AS total_items,
    ROUND(SUM(oi.quantity * oi.price), 2) AS total_amount
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city
ORDER BY total_amount DESC;


-- =========================================================
-- 2. PRODUCT SALES REPORT
-- =========================================================

SELECT
    p.product_id,
    p.title,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.price), 2) AS revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.title,
    p.category
ORDER BY revenue DESC;