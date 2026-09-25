import requests
import sqlite3

# -----------------------------------
# 1. API URLs
# -----------------------------------

USERS_API = "https://dummyjson.com/users"
PRODUCTS_API = "https://dummyjson.com/products"
CARTS_API = "https://dummyjson.com/carts"


# -----------------------------------
# 2. Extract data from APIs
# -----------------------------------

print("Extracting data from APIs...")

users_response = requests.get(USERS_API)
products_response = requests.get(PRODUCTS_API)
carts_response = requests.get(CARTS_API)

users_data = users_response.json()["users"]
products_data = products_response.json()["products"]
carts_data = carts_response.json()["carts"]

print("Users extracted:", len(users_data))
print("Products extracted:", len(products_data))
print("Orders extracted:", len(carts_data))


# -----------------------------------
# 3. Create SQLite Database
# -----------------------------------

connection = sqlite3.connect("ecommerce.db")
cursor = connection.cursor()

print("\nCreating database tables...")


# Customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    city TEXT,
    state TEXT
)
""")


# Products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    title TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
)
""")


# Orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER
)
""")


# Order items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL
)
""")


# -----------------------------------
# 4. Load Customers
# -----------------------------------

for user in users_data:

    cursor.execute("""
    INSERT OR REPLACE INTO customers
    (customer_id, first_name, last_name, email, city, state)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user["id"],
        user["firstName"],
        user["lastName"],
        user["email"],
        user["address"]["city"],
        user["address"]["state"]
    ))


# -----------------------------------
# 5. Load Products
# -----------------------------------

for product in products_data:

    cursor.execute("""
    INSERT OR REPLACE INTO products
    (product_id, title, category, price, stock)
    VALUES (?, ?, ?, ?, ?)
    """, (
        product["id"],
        product["title"],
        product["category"],
        product["price"],
        product["stock"]
    ))


# -----------------------------------
# 6. Load Orders and Order Items
# -----------------------------------

for cart in carts_data:

    cursor.execute("""
    INSERT OR REPLACE INTO orders
    (order_id, customer_id)
    VALUES (?, ?)
    """, (
        cart["id"],
        cart["userId"]
    ))

    for item in cart["products"]:

        cursor.execute("""
        INSERT INTO order_items
        (order_id, product_id, quantity, price)
        VALUES (?, ?, ?, ?)
        """, (
            cart["id"],
            item["id"],
            item["quantity"],
            item["price"]
        ))


# Save changes
connection.commit()

print("Data successfully loaded into database.")


# -----------------------------------
# 7. Business Report using JOIN
# -----------------------------------

print("\n========== CUSTOMER ORDER REPORT ==========")

query = """
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
ORDER BY total_amount DESC
"""

cursor.execute(query)

results = cursor.fetchall()

for row in results:
    print(row)


# -----------------------------------
# 8. Product Sales Report
# -----------------------------------

print("\n========== PRODUCT SALES REPORT ==========")

query2 = """
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
ORDER BY revenue DESC
"""

cursor.execute(query2)

results2 = cursor.fetchall()

for row in results2:
    print(row)


# -----------------------------------
# 9. Close database
# -----------------------------------

connection.close()

print("\nPipeline completed successfully!")