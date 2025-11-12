import mysql.connector
from mysql.connector import Error

# -------------------- DATABASE CONNECTION --------------------
def connect_db():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Leave empty if no password in XAMPP
            database="food_delivery",
            port=3306
        )
        return connection
    except Error as err:
        print(f"❌ Database connection error: {err}")
        return None


# -------------------- VIEW MENU --------------------
def view_menu():
    """Fetch and display all available menu items."""
    connection = connect_db()
    if not connection:
        print("⚠️ Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM menu_items;")
        items = cursor.fetchall()

        print("\n🍔 Available Menu Items:")
        print("-" * 40)
        if not items:
            print("⚠️ No menu items found.")
        else:
            for item in items:
                print(f"{item[0]}. {item[1]} - ${item[2]:.2f}")
        print("-" * 40)

    except Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# -------------------- PLACE ORDER --------------------
def place_order():
    """Allow user to select items, place order, and save it in DB."""
    connection = connect_db()
    if not connection:
        print("⚠️ Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()

        user_name = input("Enter your name: ")
        phone = input("Enter your phone number: ")

        # Add or find user
        cursor.execute("SELECT user_id FROM users WHERE user_name=%s AND phone=%s", (user_name, phone))
        user = cursor.fetchone()

        if not user:
            cursor.execute("INSERT INTO users (user_name, phone) VALUES (%s, %s)", (user_name, phone))
            connection.commit()
            user_id = cursor.lastrowid
        else:
            user_id = user[0]

        order_items = []
        total_amount = 0.0

        view_menu()

        while True:
            try:
                item_id = int(input("Enter the item ID to order (0 to finish): "))
                if item_id == 0:
                    break

                cursor.execute("SELECT item_name, price FROM menu_items WHERE item_id = %s", (item_id,))
                item = cursor.fetchone()
                if item:
                    quantity = int(input(f"Enter quantity for {item[0]}: "))
                    subtotal = item[1] * quantity
                    total_amount += subtotal
                    order_items.append((item_id, quantity, subtotal))
                    print(f"✅ Added {quantity} x {item[0]} (${subtotal:.2f})")
                else:
                    print("⚠️ Invalid item ID.")
            except ValueError:
                print("⚠️ Please enter a valid number.")

        if not order_items:
            print("⚠️ No items selected. Order not placed.")
            return

        # Create order
        cursor.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)", (user_id, total_amount))
        order_id = cursor.lastrowid

        # Insert each order item
        for item_id, quantity, subtotal in order_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, item_id, quantity, subtotal) VALUES (%s, %s, %s, %s)",
                (order_id, item_id, quantity, subtotal)
            )

        connection.commit()

        print("\n🧾 Order Summary:")
        for item_id, quantity, subtotal in order_items:
            cursor.execute("SELECT item_name FROM menu_items WHERE item_id = %s", (item_id,))
            item_name = cursor.fetchone()[0]
            print(f"{quantity} x {item_name} = ${subtotal:.2f}")
        print(f"Total Amount: ${total_amount:.2f}")
        print("✅ Order placed successfully!")

    except Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# -------------------- VIEW ORDER SUMMARY --------------------
def view_order_summary():
    """Display a summary of all orders with details."""
    connection = connect_db()
    if not connection:
        print("⚠️ Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()
        query = """
            SELECT o.order_id, u.user_name, mi.item_name, oi.quantity, oi.subtotal, o.total_amount, o.order_date
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN menu_items mi ON oi.item_id = mi.item_id
            ORDER BY o.order_date DESC;
        """
        cursor.execute(query)
        records = cursor.fetchall()

        print("\n📦 All Orders Summary:")
        print("-" * 80)
        for row in records:
            print(f"Order #{row[0]} | Customer: {row[1]} | {row[3]} x {row[2]} | "
                  f"Subtotal: ${row[4]:.2f} | Total: ${row[5]:.2f} | Date: {row[6]}")
        print("-" * 80)
    except Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# -------------------- ADMIN FUNCTIONS --------------------
def add_menu_item():
    """Admin can add new food item."""
    connection = connect_db()
    if not connection:
        print("⚠️ Could not connect to the database.")
        return

    try:
        name = input("Enter new food name: ")
        price = float(input("Enter price: "))
        cursor = connection.cursor()
        cursor.execute("INSERT INTO menu_items (item_name, price) VALUES (%s, %s)", (name, price))
        connection.commit()
        print(f"✅ '{name}' added to menu successfully!")
    except Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def remove_menu_item():
    """Admin can remove a menu item."""
    connection = connect_db()
    if not connection:
        print("⚠️ Could not connect to the database.")
        return

    try:
        view_menu()
        item_id = int(input("Enter the item ID to remove: "))
        cursor = connection.cursor()
        cursor.execute("DELETE FROM menu_items WHERE item_id = %s", (item_id,))
        connection.commit()
        print(f"🗑️ Item #{item_id} removed successfully!")
    except ValueError:
        print("⚠️ Invalid input.")
    except Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# -------------------- MAIN MENU --------------------
def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\n========== 🍴 FOOD DELIVERY APP ==========")
        print("1. View Menu")
        print("2. Place Order")
        print("3. View All Orders")
        print("4. Add Menu Item (Admin)")
        print("5. Remove Menu Item (Admin)")
        print("6. Exit")
        print("==========================================")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            view_menu()
        elif choice == '2':
            place_order()
        elif choice == '3':
            view_order_summary()
        elif choice == '4':
            add_menu_item()
        elif choice == '5':
            remove_menu_item()
        elif choice == '6':
            print("👋 Thank you for using Food Delivery App!")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    main_menu()

