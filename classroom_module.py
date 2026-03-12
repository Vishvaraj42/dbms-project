
from db_connection import get_connection

def add_classroom():
    """Add a new classroom."""
    try:
        db = get_connection()
        if db is None:
            print("Database connection failed.")
            return

        cursor = db.cursor()

        building = input("Enter building/block name: ")
        room_number = input("Enter room number: ")
        capacity = int(input("Enter classroom capacity: "))

        query = "INSERT INTO classroom (building, room_number, capacity) VALUES (%s, %s, %s)"
        cursor.execute(query, (building, room_number, capacity))
        db.commit()

        print("Classroom added successfully!")

    except Exception as e:
        print("Error adding classroom:", e)
    finally:
        if db.is_connected():
            cursor.close()
            db.close()


def view_classrooms():
    """Display all classrooms."""
    try:
        db = get_connection()
        if db is None:
            print("Database connection failed.")
            return

        cursor = db.cursor()
        cursor.execute("SELECT * FROM classroom")
        records = cursor.fetchall()

        print("\nClassroom List:")
        print("-" * 40)
        for row in records:
            print(f"ID: {row[0]}, Building: {row[1]}, Room: {row[2]}, Capacity: {row[3]}")
        print("-" * 40)

    except Exception as e:
        print("Error viewing classrooms:", e)
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
