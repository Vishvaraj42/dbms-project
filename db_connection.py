
import mysql.connector

def get_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vishu@189",
            database="university_db"
        )
        return db
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None
