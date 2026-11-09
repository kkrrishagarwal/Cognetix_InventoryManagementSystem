import sqlite3
import csv
import os

DB_FILE = "inventory.db"

def get_conn():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_product():
    conn = get_conn()
    c = conn.cursor()
    pid = input("Enter Product ID: ").strip()
    name = input("Enter Product Name: ").strip()
    cat = input("Enter Category: ").strip()
    try:
        qty = int(input("Enter Quantity: ").strip())
        price = float(input("Enter Price per unit: ").strip())
        c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", (pid, name, cat, qty, price))
        conn.commit()
        print("✅ Product added successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

def view_inventory():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("📂 Inventory is empty.")
        return

    print("\n" + "=" * 70)
    print(f"{'ID':<10} | {'Name':<16} | {'Category':<14} | {'Qty':<6} | {'Price':<10}")
    print("-" * 70)
    for r in rows:
        print(f"{r[0]:<10} | {r[1]:<16} | {r[2]:<14} | {r[3]:<6} | ₹{r[4]:<9,.2f}")
    print("=" * 70)

def generate_reports():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE quantity < 10")
    low_stock = c.fetchall()

    c.execute("SELECT COUNT(*), SUM(quantity), SUM(quantity * price) FROM products")
    summary = c.fetchone()
    conn.close()

    print("\n📊 --- INVENTORY REPORTS ---")
    print(f"Total Products : {summary[0] or 0}")
    print(f"Total Stock Qty: {summary[1] or 0}")
    print(f"Total Valuation: ₹{summary[2] or 0:,.2f}")

    print("\n⚠️ Low Stock Alert (< 10 items):")
    if low_stock:
        for r in low_stock:
            print(f" - ID: {r[0]}, Name: {r[1]}, Remaining Qty: {r[3]}")
    else:
        print(" None! All items are well-stocked.")

def bulk_update():
    path = input("Enter CSV file path for bulk update: ").strip()
    if not os.path.exists(path):
        print("❌ CSV file not found.")
        return
    conn = get_conn()
    c = conn.cursor()
    try:
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                c.execute("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?)",
                          (row["product_id"], row["name"], row["category"], int(row["quantity"]), float(row["price"])))
        conn.commit()
        print("✅ Bulk update completed successfully!")
    except Exception as e:
        print(f"❌ Bulk update failed: {e}")
    finally:
        conn.close()

def main():
    init_db()
    while True:
        print("\n==========================================")
        print("      INVENTORY MANAGEMENT SYSTEM         ")
        print("==========================================")
        print("1. Add Product")
        print("2. View Inventory")
        print("3. Low Stock & Valuation Reports")
        print("4. Bulk Update via CSV")
        print("5. Exit")
        print("------------------------------------------")
        choice = input("Enter choice (1-5): ").strip()
        if choice == "1": add_product()
        elif choice == "2": view_inventory()
        elif choice == "3": generate_reports()
        elif choice == "4": bulk_update()
        elif choice == "5": break

if __name__ == "__main__":
    main()
