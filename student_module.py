
from db_connection import get_connection

def add_student():
    db = get_connection()
    cursor = db.cursor()
    name = input("Enter student name: ")
    email = input("Enter Email ID: ")
    dept_id = input("Enter department ID")

    cursor.execute("INSERT INTO student (name, email, dept_id) VALUES (%s, %s, %s)", (name, email, dept_id))
    db.commit()
    print("Student added successfully!")
    db.close()

def view_students():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()

    print("\n--- Student List ---")
    for r in rows:
        print(f"ID: {r[0]} | Name: {r[1]} | Department: {r[2]}")
    db.close()
