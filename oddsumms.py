


# # using breakpoints in the code to check if they are working as intended 

# def div(x,y):
#     breakpoint()
#     z = x/y
#     return z
# def values():
#     a = int(input("enter the first number: "))
#     b =int(input("enter the seconf number: "))
#     u = div(a,b)
#     breakpoint()
#     return u
# k = values()
# print("the result of division is :",round(k,2))



"""
food_delivery_app.py

Console-based Food Delivery Application (Python + MySQL)
- View Menu
- Place Order (creates order header + order items)
- View Order Summary (by order id)
- Admin: add / remove menu items (simple password-protected)
"""

import mysql.connector
from mysql.connector import Error
import sys

# ------------------------
# Database configuration - EDIT these to match your local MySQL
# ------------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',        # <- enter your MySQL root password here
    'database': 'food_delivery',
    'port': 3306
}

# Simple admin password for the optional admin functions.
ADMIN_PASSWORD = "admin123"  # change this for real use

# ------------------------
# Database helper functions
# ------------------------
def get_connection():
    """Return a new database connection using DB_CONFIG."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("Error connecting to database:", e)
        return None

# ------------------------
# Feature: View Menu
# ------------------------
def view_menu():
    """Fetch and print all menu items."""
    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM menu_items ORDER BY id;")
        rows = cursor.fetchall()
        if not rows:
            print("\nNo menu items found.\n")
            return

        print("\n--- MENU ---")
        print(f"{'ID':<4} {'Item':<30} {'Price':>7}")
        print("-" * 45)
        for r in rows:
            print(f"{r[0]:<4} {r[1]:<30} £{float(r[2]):>6.2f}")
        print("-" * 45 + "\n")
    except Error as e:
        print("Database error while fetching menu:", e)
    finally:
        cursor.close()
        conn.close()

# ------------------------
# Feature: Place Order
# ------------------------
def place_order():
    """
    Interactive placing of an order:
    - display menu
    - user selects item by id and quantity repeatedly
    - create order entry and order_items entries
    - show order id and summary
    """
    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        # fetch menu to display and validate choices
        cursor.execute("SELECT id, name, price FROM menu_items ORDER BY id;")
        menu = cursor.fetchall()
        if not menu:
            print("\nNo menu items available. Contact admin.\n")
            return

        # Build quick lookup dict: id -> (name, price)
        menu_lookup = {r[0]: (r[1], float(r[2])) for r in menu}

        print("\nPlace your order. Enter item ID and quantity.")
        print("Type 'done' when finished or 'cancel' to cancel order.\n")
        print("Available items:")
        for r in menu:
            print(f"{r[0]:<4} {r[1]:<30} £{float(r[2]):>6.2f}")
        print("-" * 45)

        cart = {}  # menu_item_id -> quantity

        while True:
            choice = input("Item ID (or 'done'): ").strip().lower()
            if choice == 'done':
                break
            if choice == 'cancel':
                print("Order cancelled.\n")
                return
            if not choice.isdigit():
                print("Please enter a valid numeric item ID or 'done'.")
                continue
            item_id = int(choice)
            if item_id not in menu_lookup:
                print("Item ID not found. Try again.")
                continue

            qty_input = input("Quantity: ").strip()
            if not qty_input.isdigit() or int(qty_input) <= 0:
                print("Please enter a positive integer quantity.")
                continue
            qty = int(qty_input)
            cart[item_id] = cart.get(item_id, 0) + qty
            print(f"Added {qty} x {menu_lookup[item_id][0]} to cart.\n")

        if not cart:
            print("No items selected. Order not created.\n")
            return

        # Create order header
        cursor.execute("INSERT INTO orders () VALUES ();")
        conn.commit()
        order_id = cursor.lastrowid

        # Insert items and compute total
        total = 0.0
        insert_stmt = ("INSERT INTO order_items (order_id, menu_item_id, quantity, price) "
                       "VALUES (%s, %s, %s, %s);")
        for m_id, qty in cart.items():
            name, price = menu_lookup[m_id]
            line_total = price * qty
            total += line_total
            cursor.execute(insert_stmt, (order_id, m_id, qty, price))
        conn.commit()

        print("\nOrder created successfully!")
        print(f"Your order id is: {order_id}")
        print("Order Summary:")
        print(f"{'Item':<30} {'Qty':>3} {'Price':>8} {'Line':>8}")
        print("-" * 55)
        for m_id, qty in cart.items():
            name, price = menu_lookup[m_id]
            print(f"{name:<30} {qty:>3} £{price:>7.2f} £{price*qty:>7.2f}")
        print("-" * 55)
        print(f"{'Total':<30} {'':>3} {'':>8} £{total:>7.2f}\n")
    except Error as e:
        print("Error while placing order:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# ------------------------
# Feature: View Order Summary
# ------------------------
def view_order_summary():
    """Ask user for order id and print order summary with totals."""
    conn = get_connection()
    if not conn:
        return

    try:
        order_id_input = input("Enter order id to view (or 'last' for the most recent order): ").strip().lower()
        cursor = conn.cursor()

        if order_id_input == 'last':
            cursor.execute("SELECT order_id FROM orders ORDER BY created_at DESC LIMIT 1;")
            row = cursor.fetchone()
            if not row:
                print("No orders found.\n")
                return
            order_id = row[0]
        elif order_id_input.isdigit():
            order_id = int(order_id_input)
        else:
            print("Invalid input. Please enter an order id or 'last'.")
            return

        # Fetch order items
        stmt = ("SELECT mi.name, oi.quantity, oi.price "
                "FROM order_items oi JOIN menu_items mi ON oi.menu_item_id = mi.id "
                "WHERE oi.order_id = %s;")
        cursor.execute(stmt, (order_id,))
        items = cursor.fetchall()
        if not items:
            print(f"No items found for order id {order_id}.\n")
            return

        total = 0.0
        print(f"\nOrder ID: {order_id}")
        print(f"{'Item':<30} {'Qty':>3} {'Price':>8} {'Line':>8}")
        print("-" * 55)
        for name, qty, price in items:
            line = float(price) * qty
            total += line
            print(f"{name:<30} {qty:>3} £{float(price):>7.2f} £{line:>7.2f}")
        print("-" * 55)
        print(f"{'Total':<30} {'':>3} {'':>8} £{total:>7.2f}\n")
    except Error as e:
        print("Database error while viewing order:", e)
    finally:
        cursor.close()
        conn.close()

# ------------------------
# Admin functions
# ------------------------
def admin_add_menu_item():
    """Add a new menu item (admin only)."""
    pwd = input("Enter admin password: ").strip()
    if pwd != ADMIN_PASSWORD:
        print("Incorrect admin password.\n")
        return

    name = input("Enter new item name: ").strip()
    if not name:
        print("Item name cannot be empty.\n")
        return
    price_input = input("Enter price (e.g., 4.50): ").strip()
    try:
        price = float(price_input)
        if price <= 0:
            raise ValueError
    except ValueError:
        print("Invalid price. Use a positive number like 4.50.\n")
        return

    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO menu_items (name, price) VALUES (%s, %s);", (name, price))
        conn.commit()
        print(f"Added menu item '{name}' at £{price:.2f}\n")
    except Error as e:
        print("Error adding menu item:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def admin_remove_menu_item():
    """Remove a menu item by id (admin only)."""
    pwd = input("Enter admin password: ").strip()
    if pwd != ADMIN_PASSWORD:
        print("Incorrect admin password.\n")
        return

    view_menu()
    item_id_input = input("Enter item ID to remove (or 'cancel'): ").strip().lower()
    if item_id_input == 'cancel':
        return
    if not item_id_input.isdigit():
        print("Invalid item ID.\n")
        return
    item_id = int(item_id_input)

    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        # Check existence
        cursor.execute("SELECT name FROM menu_items WHERE id=%s;", (item_id,))
        row = cursor.fetchone()
        if not row:
            print("Item ID not found.\n")
            return

        cursor.execute("DELETE FROM menu_items WHERE id=%s;", (item_id,))
        conn.commit()
        print(f"Removed menu item '{row[0]}' (id {item_id}).\n")
    except Error as e:
        print("Error removing menu item:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# ------------------------
# Main menu and program loop
# ------------------------
def display_main_menu():
    print("""
--- Food Delivery App ---
1. View Menu
2. Place Order
3. View Order Summary
4. Admin: Add Menu Item
5. Admin: Remove Menu Item
6. Exit
""")

def main():
    print("Welcome to the Food Delivery App (Console)")
    # Basic check that DB is reachable
    conn = get_connection()
    if not conn:
        print("Cannot connect to database. Please check DB settings in script.")
        return
    conn.close()

    while True:
        display_main_menu()
        choice = input("Enter choice (1-6): ").strip()
        if choice == '1':
            view_menu()
        elif choice == '2':
            place_order()
        elif choice == '3':
            view_order_summary()
        elif choice == '4':
            admin_add_menu_item()
        elif choice == '5':
            admin_remove_menu_item()
        elif choice == '6':
            print("Exiting. Thank you!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Goodbye.")
        sys.exit(0)
