
from db_connection import get_connection

def add_department():
    """Add a new department."""
    try:
        db = get_connection()
        if db is None:
            print("Database connection failed.")
            return

        cursor = db.cursor()

        dept_name = input("Enter department name: ")
        building = input("Enter building/block name: ")

        query = "INSERT INTO department (dept_name, building) VALUES (%s, %s)"
        cursor.execute(query, (dept_name, building))
        db.commit()

        print("Department added successfully!")

    except Exception as e:
        print("Error adding department:", e)
    finally:
        if db.is_connected():
            cursor.close()
            db.close()


def view_departments():
    """Display all departments."""
    try:
        db = get_connection()
        if db is None:
            print("Database connection failed.")
            return

        cursor = db.cursor()
        cursor.execute("SELECT * FROM department")
        records = cursor.fetchall()

        print("\nDepartment List:")
        print("-" * 40)
        for row in records:
            print(f"ID: {row[0]}, Name: {row[1]}, Building: {row[2]}")
        print("-" * 40)

    except Exception as e:
        print("Error viewing departments:", e)
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
