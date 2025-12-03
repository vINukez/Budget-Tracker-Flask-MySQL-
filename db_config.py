import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="budget_user",
        password="=6-.MWH7u3fo0wy1ws_KRV",
        database="budget_tracker"

    )
    return connection

# MySQL Root user und pw
# user: root
# pw: Root1234!