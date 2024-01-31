import mysql.connector

# Replace these values with your actual MySQL database credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'my_food',
}

def get_order_status(order_id):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Execute the SQL query to retrieve the status based on order_id
        query = "SELECT status FROM order_tracking WHERE order_id=%s"
        cursor.execute(query, (order_id,))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            order_status = result[0]
            return order_status
        else:
            return "not found in the system. Please make sure that you are entering your order id right."

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()

def get_next_order_id():             # bunu kullanmadım sonra kullanırım belki!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Execute the SQL query to retrieve the status based on order_id
        query = "SELECT MAX(order_id) from order_tracking"
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchone()

        if result:
            max_order_id = result[0]
            return max_order_id + 1
        else:
            return 1

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()

def insert_order_tracking(next_order_id, status):
    # 1. order_tracking'e order_id ve status ekleme
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Execute the SQL query to retrieve the status based on order_id
        query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        values = (next_order_id, status)
        cursor.execute(query, values)

        # Commit the changes to the database
        connection.commit()

        return f"Data inserted successfully with Order ID: {next_order_id}"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Oops... Something went wrong, your order cannot be placed. Please try again."

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()

def insert_orders(food_item:str, quantity:int, next_order_id:int):
    try:
        # Assume db_config, next_order_id, and order are defined
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        item_id = get_item_id_by_name(food_item)

        total_price = get_total_price(item_id, quantity)

        # SQL query to insert values into the orders table
        insert_query = (
            "INSERT INTO orders VALUES (%s, %s, %s, %s)"
        )

        # Execute the query with the provided values
        cursor.execute(insert_query, (next_order_id, item_id, quantity, total_price))

        # Commit the changes
        connection.commit()

        return 1

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()

        return -1

    finally:
        # Close the cursor and connection in the finally block
        if 'cursor' in locals() and cursor is not None:
            cursor.close()


def get_item_id_by_name(food_name):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # SQL query to retrieve the item_id based on the food name
        select_query = "SELECT item_id FROM food_items WHERE name = %s"

        # Execute the query with the provided values
        cursor.execute(select_query, (food_name,))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            item_id = result[0]
            return item_id
        else:
            print(f"No item found with name '{food_name}'")
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Close the cursor (Note: Connection is not closed to allow reuse)
        cursor.close()

def get_total_price(item_id, quantity): # itemid ile price ı bul quantitiy ile çarp return et
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Execute the SQL query to retrieve the status based on order_id
        query = "SELECT price FROM food_items WHERE item_id=%s"
        cursor.execute(query, (item_id,))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            price = result[0]
            total_price = int(price) * int(quantity)
            return total_price
        else:
            return 0

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()