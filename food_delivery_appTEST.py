import mysql.connector
from mysql.connector import Error
import sys

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Amadestiny@1",  # Replace with your actual password
            database="food_delivery",
            port=3306
        )    
      
      
        return connection
    except mysql_connector.Error as err:
             print(f"❌ Database connection error: {err}")
        
        
    return None


# -------------------- MENU DISPLAY --------------------
# def view_menu():
#     connection = connect_db()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM menu_items;")
#     items = cursor.fetchall()
#     print("\n🍔 Available Menu Items:")
#     print("-" * 35)
#     for item in items:
#         print(f"{item[0]}. {item[1]} - ${item[2]:.2f}")
#     print("-" * 35)
#     cursor.close()
#     connection.close()


# def view_menu():
#     connection = connect_db()
#     if not connection:
#         print("⚠️ Could not connect to the database.")
#         return

#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM menu_items;")
#     items = cursor.fetchall()

#     print("\n🍔 Available Menu Items:")
#     print("-" * 35)
#     if not items:
#         print("⚠️ No menu items found in the database.")
#     for item in items:
#         print(f"{item[0]}. {item[1]} - ${item[2]:.2f}")
#     print("-" * 35)

#     cursor.close()
#     connection.close()






def view_menu():
    connection = connect_db()
    if not connection:
        print("⚠️ Could not connect to the database.")
        return

    try:
        cursor = connection.cursor()
        
        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'menu_items'")
        if not cursor.fetchone():
            print("⚠️ Menu items table does not exist!")
            return
            
        cursor.execute("SELECT * FROM menu_items;")
        items = cursor.fetchall()

        print("\n🍔 Available Menu Items:")
        print("-" * 35)
        if not items:
            print("⚠️ No menu items found in the database.")
        else:
            for item in items:
                print(f"{item[0]}. {item[1]} - ${item[2]:.2f}")
        print("-" * 35)

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        connection.close()


# -------------------- PLACE ORDER --------------------
def place_order():
    connection = connect_db()
    cursor = connection.cursor()

    view_menu()
    order_items = []
    total_cost = 0

    while True:
        try:
            item_id = int(input("Enter the item number to order (0 to finish): "))
            if item_id == 0:
                break

            cursor.execute("SELECT name, price FROM menu_items WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            if item:
                quantity = int(input(f"Enter quantity for {item[0]}: "))
                cost = item[1] * quantity
                total_cost += cost
                order_items.append((item[0], quantity, cost))
                print(f"✅ Added {quantity} x {item[0]} (${cost:.2f})")
            else:
                print("⚠️ Invalid item number. Try again.")
        except ValueError:
            print("⚠️ Please enter a valid number.")

    if order_items:
        for order in order_items:
            cursor.execute(
                "INSERT INTO orders (item_name, quantity, total_price) VALUES (%s, %s, %s)",
                (order[0], order[1], order[2])
            )
        connection.commit()
        print("\n🧾 Order Summary:")
        for order in order_items:
            print(f"{order[1]} x {order[0]} = ${order[2]:.2f}")
        print(f"Total: ${total_cost:.2f}")
        print("✅ Order placed successfully!")
    else:
        print("⚠️ No items ordered.")

    cursor.close()
    connection.close()


# -------------------- VIEW ORDERS --------------------
def view_order_summary():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders;")
    orders = cursor.fetchall()
    print("\n📦 Current Orders:")
    print("-" * 40)
    for order in orders:
        print(f"#{order[0]} | {order[1]} x{order[2]} = ${order[3]:.2f}")
    print("-" * 40)
    cursor.close()
    connection.close()


# -------------------- ADMIN: ADD/REMOVE ITEMS --------------------
def add_menu_item():
    connection = connect_db()
    cursor = connection.cursor()
    name = input("Enter new food name: ")
    price = float(input("Enter price: "))
    cursor.execute("INSERT INTO menu_items (name, price) VALUES (%s, %s)", (name, price))
    connection.commit()
    print(f"✅ '{name}' added to menu successfully!")
    cursor.close()
    connection.close()


def remove_menu_item():
    connection = connect_db()
    cursor = connection.cursor()
    view_menu()
    try:
        item_id = int(input("Enter the item number to remove: "))
        cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
        connection.commit()
        print(f"🗑️ Item #{item_id} removed successfully!")
    except ValueError:
        print("⚠️ Invalid input.")
    cursor.close()
    connection.close()


# -------------------- MAIN MENU --------------------
def main_menu():
    while True:
        print("\n========== 🍴 FOOD DELIVERY APP ==========")
        print("1. View Menu")
        print("2. Place Order")
        print("3. View Orders")
        print("4. Add Menu Item (Admin)")
        print("5. Remove Menu Item (Admin)")
        print("6. Exit")
        print("=========================================")

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


# -------------------- RUN THE PROGRAM --------------------
if __name__ == "__main__":
    main_menu()

# To access the MySQL command line:
# mysql -u root -p
