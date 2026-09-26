import requests
import psycopg2
from getpass import getpass


# ==========================================
# 1. API URLs
# ==========================================

USERS_API = "https://dummyjson.com/users"
PRODUCTS_API = "https://dummyjson.com/products?limit=0"
CARTS_API = "https://dummyjson.com/carts"


# ==========================================
# 2. PostgreSQL Connection
# ==========================================

print("Connecting to PostgreSQL...")

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ecommerce_db"
DB_USER = "postgres"

DB_PASSWORD = getpass("Enter PostgreSQL password: ")

connection = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = connection.cursor()

print("Connected to PostgreSQL successfully!")


try:

    # ==========================================
    # 3. Extract data from APIs
    # ==========================================

    print("\nExtracting data from APIs...")

    users_response = requests.get(USERS_API, timeout=30)
    products_response = requests.get(PRODUCTS_API, timeout=30)
    carts_response = requests.get(CARTS_API, timeout=30)

    # Check API responses
    users_response.raise_for_status()
    products_response.raise_for_status()
    carts_response.raise_for_status()

    users_data = users_response.json()["users"]
    products_data = products_response.json()["products"]
    carts_data = carts_response.json()["carts"]

    print("Users extracted:", len(users_data))
    print("Products extracted:", len(products_data))
    print("Orders extracted:", len(carts_data))


    # ==========================================
    # 4. Create PostgreSQL Tables
    # ==========================================

    print("\nCreating PostgreSQL tables...")

    # Customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        city TEXT,
        state TEXT
    )
    """)

    # Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT,
        price NUMERIC(10, 2),
        stock INTEGER
    )
    """)

    # Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
    )
    """)

    # Order items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id SERIAL PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        FOREIGN KEY (order_id)
            REFERENCES orders(order_id),
        FOREIGN KEY (product_id)
            REFERENCES products(product_id)
    )
    """)

    connection.commit()

    print("Tables created successfully!")


    # ==========================================
    # 5. Clear Previous Data
    # ==========================================

    print("\nClearing previous data...")

    cursor.execute("""
    TRUNCATE TABLE
        order_items,
        orders,
        products,
        customers
    RESTART IDENTITY CASCADE
    """)

    connection.commit()

    print("Previous data cleared.")


    # ==========================================
    # 6. Load Customers
    # ==========================================

    print("\nLoading customers...")

    for user in users_data:

        cursor.execute("""
        INSERT INTO customers
        (
            customer_id,
            first_name,
            last_name,
            email,
            city,
            state
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user["id"],
            user["firstName"],
            user["lastName"],
            user["email"],
            user["address"]["city"],
            user["address"]["state"]
        ))

    print("Customers loaded:", len(users_data))


    # ==========================================
    # 7. Load Products
    # ==========================================

    print("\nLoading products...")

    for product in products_data:

        cursor.execute("""
        INSERT INTO products
        (
            product_id,
            title,
            category,
            price,
            stock
        )
        VALUES (%s, %s, %s, %s, %s)
        """, (
            product["id"],
            product["title"],
            product["category"],
            product["price"],
            product["stock"]
        ))

    print("Products loaded:", len(products_data))


    # ==========================================
    # 8. Load Orders and Order Items
    # ==========================================

    print("\nLoading orders and order items...")

    order_count = 0
    order_item_count = 0

    for cart in carts_data:

        # Insert order
        cursor.execute("""
        INSERT INTO orders
        (
            order_id,
            customer_id
        )
        VALUES (%s, %s)
        """, (
            cart["id"],
            cart["userId"]
        ))

        order_count += 1

        # Insert order items
        for item in cart["products"]:

            cursor.execute("""
            INSERT INTO order_items
            (
                order_id,
                product_id,
                quantity,
                price
            )
            VALUES (%s, %s, %s, %s)
            """, (
                cart["id"],
                item["id"],
                item["quantity"],
                item["price"]
            ))

            order_item_count += 1

    connection.commit()

    print("Orders loaded:", order_count)
    print("Order items loaded:", order_item_count)

    print("\nData successfully loaded into PostgreSQL!")


    # ==========================================
    # 9. Customer Order Report
    # ==========================================

    print("\n")
    print("=" * 80)
    print("CUSTOMER ORDER REPORT")
    print("=" * 80)

    customer_report_query = """
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

    cursor.execute(customer_report_query)

    customer_results = cursor.fetchall()

    for row in customer_results:
        print(row)


    # ==========================================
    # 10. Product Sales Report
    # ==========================================

    print("\n")
    print("=" * 80)
    print("PRODUCT SALES REPORT")
    print("=" * 80)

    product_report_query = """
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

    cursor.execute(product_report_query)

    product_results = cursor.fetchall()

    for row in product_results:
        print(row)


    # ==========================================
    # 11. Close PostgreSQL Connection
    # ==========================================

    cursor.close()
    connection.close()

    print("\n")
    print("=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 80)


except Exception as error:

    # Rollback if any error occurs
    connection.rollback()

    print("\n")
    print("=" * 80)
    print("PIPELINE FAILED")
    print("=" * 80)
    print("Error:", error)

    cursor.close()
    connection.close()