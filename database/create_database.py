import sqlite3
import random
from datetime import date, timedelta
from pathlib import Path


# --------------------------------------------------
# 1. Database path
# --------------------------------------------------

DB_PATH = Path(__file__).parent / "retail.db"


# --------------------------------------------------
# 2. Connect to database
# --------------------------------------------------

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# --------------------------------------------------
# 3. Create customers table
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region TEXT NOT NULL,
    customer_segment TEXT NOT NULL
)
""")


# --------------------------------------------------
# 4. Create products table
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
)
""")


# --------------------------------------------------
# 5. Create orders table
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    revenue REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")


# --------------------------------------------------
# 6. Generate customers
# --------------------------------------------------

regions = ["North", "South", "East", "West"]
segments = ["Consumer", "Corporate", "Small Business"]

customers = []

for i in range(1, 101):
    customers.append((
        i,
        f"Customer_{i:03d}",
        random.choice(regions),
        random.choice(segments)
    ))

cursor.executemany("""
INSERT INTO customers
(customer_id, customer_name, region, customer_segment)
VALUES (?, ?, ?, ?)
""", customers)


# --------------------------------------------------
# 7. Add products
# --------------------------------------------------

products = [
    (1, "Wireless Mouse", "Electronics", 25.99),
    (2, "Mechanical Keyboard", "Electronics", 79.99),
    (3, "USB-C Hub", "Electronics", 39.99),
    (4, "Bluetooth Headphones", "Electronics", 59.99),
    (5, "Laptop Stand", "Electronics", 45.99),

    (6, "Office Chair", "Furniture", 189.99),
    (7, "Standing Desk", "Furniture", 349.99),
    (8, "Desk Lamp", "Furniture", 42.99),
    (9, "Bookshelf", "Furniture", 129.99),
    (10, "Filing Cabinet", "Furniture", 99.99),

    (11, "Notebook", "Stationery", 6.99),
    (12, "Ballpoint Pen Set", "Stationery", 9.99),
    (13, "Planner", "Stationery", 14.99),
    (14, "Marker Set", "Stationery", 12.99),
    (15, "Sticky Notes Pack", "Stationery", 5.49),

    (16, "Coffee Maker", "Appliances", 89.99),
    (17, "Electric Kettle", "Appliances", 49.99),
    (18, "Air Fryer", "Appliances", 119.99),
    (19, "Blender", "Appliances", 69.99),
    (20, "Toaster", "Appliances", 39.99),

    (21, "Backpack", "Accessories", 49.99),
    (22, "Travel Mug", "Accessories", 19.99),
    (23, "Water Bottle", "Accessories", 24.99),
    (24, "Laptop Sleeve", "Accessories", 29.99),
    (25, "Phone Stand", "Accessories", 15.99),

    (26, "Running Shoes", "Sports", 89.99),
    (27, "Yoga Mat", "Sports", 29.99),
    (28, "Dumbbell Set", "Sports", 79.99),
    (29, "Resistance Bands", "Sports", 24.99),
    (30, "Fitness Tracker", "Sports", 99.99)
]

cursor.executemany("""
INSERT INTO products
(product_id, product_name, category, price)
VALUES (?, ?, ?, ?)
""", products)


# --------------------------------------------------
# 8. Generate orders
# --------------------------------------------------

orders = []

start_date = date(2024, 1, 1)
end_date = date(2025, 12, 31)

order_count = 5000

for order_id in range(1, order_count + 1):

    customer_id = random.randint(1, 100)
    product_id = random.randint(1, 30)

    random_days = random.randint(
        0,
        (end_date - start_date).days
    )

    order_date = start_date + timedelta(days=random_days)

    quantity = random.randint(1, 5)

    cursor.execute(
        "SELECT price FROM products WHERE product_id = ?",
        (product_id,)
    )

    price = cursor.fetchone()[0]

    revenue = round(price * quantity, 2)

    orders.append((
        order_id,
        customer_id,
        product_id,
        order_date.isoformat(),
        quantity,
        revenue
    ))


cursor.executemany("""
INSERT INTO orders
(order_id, customer_id, product_id, order_date, quantity, revenue)
VALUES (?, ?, ?, ?, ?, ?)
""", orders)


# --------------------------------------------------
# 9. Save changes
# --------------------------------------------------

conn.commit()


# --------------------------------------------------
# 10. Close connection
# --------------------------------------------------

conn.close()

print("Retail database created successfully!")
print(f"Database location: {DB_PATH}")
print("Customers: 100")
print("Products: 30")
print("Orders: 5,000")