
from db_connection import get_connection

def add_faculty():
    try:
        db = get_connection()
        cursor = db.cursor()

        name = input("Enter faculty name: ")
        department = input("Enter department: ")
        email = input("Enter email: ")

        query = "INSERT INTO faculty (name, department, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, department, email))
        db.commit()
        print("Faculty added successfully!")

    except Exception as e:
        print("Error adding faculty:", e)
    finally:
        if db.is_connected():
            db.close()

def view_faculty():
    try:
        db = get_connection()
        cursor = db.cursor()

        query = "SELECT * FROM faculty"
        cursor.execute(query)
        records = cursor.fetchall()

        print("\n Faculty List:")
        for row in records:
            print(f"ID: {row[0]}, Name: {row[1]}, Department: {row[2]}, Email: {row[3]}")

    except Exception as e:
        print("Error viewing faculty:", e)
    finally:
        if db.is_connected():
            db.close()
