# print("🚀 Running connection test...")
# import mysql.connector


# # try:
# #     conn = mysql.connector.connect(
# #         host="localhost",
# #         user="root",
# #         password="Amadestiny@1",
# #         database="food_delivery",
# #         port=3306  # add this explicitly
# #     )
# #     print("✅ Connected successfully!\n")

# #     cursor = conn.cursor()
# #     cursor.execute("SELECT DATABASE();")
# #     print("Current Database:", cursor.fetchone())

# #     cursor.execute("SHOW TABLES;")
# #     print("Tables:", cursor.fetchall())

# #     cursor.execute("SELECT * FROM menu_items;")
# #     results = cursor.fetchall()
# #     print("\n🍔 Menu Items Found:")
# #     for row in results:
# #         print(row)

# #     conn.close()
# # except mysql.connector.Error as err:
# #     print("❌ Connection Error:", err)



# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Amadestiny@1",
#     database="food_delivery",
#     port=3306 # try changing this to match your MySQL port
# )



import unittest
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Amadestiny@1",
        database="food_delivery",
        port=3306
    )

def view_menu():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM menu_items;")
    items = cursor.fetchall()
    print("\n🍔 Available Menu Items:")
    print("-" * 35)
    for item in items:
        print(f"{item[0]}. {item[1]} - ${item[2]:.2f}")
    print("-" * 35)
    cursor.close()
    connection.close()
    return items

class TestMenuOperations(unittest.TestCase):
    def test_view_menu(self):
        items = view_menu()
        self.assertIsNotNone(items)
        self.assertIsInstance(items, list)