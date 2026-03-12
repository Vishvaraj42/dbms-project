
from db_connection import get_connection

def add_prerequisite():
    try:
        db = get_connection()
        cursor = db.cursor()

        course_id = input("Enter course ID (main course): ")
        prereq_course_id = input("Enter prerequisite course ID: ")

        query = "INSERT INTO prerequisite (course_id, prereq_course_id) VALUES (%s, %s)"
        cursor.execute(query, (course_id, prereq_course_id))
        db.commit()
        print(" Prerequisite added successfully!")

    except Exception as e:
        print("Error adding prerequisite:", e)
    finally:
        if db.is_connected():
            db.close()

def view_prerequisites():
    try:
        db = get_connection()
        cursor = db.cursor()

        query = """
        SELECT c1.title AS Course, c2.title AS Prerequisite
        FROM prerequisite p
        JOIN course c1 ON p.course_id = c1.course_id
        JOIN course c2 ON p.prereq_course_id = c2.course_id;
        """
        cursor.execute(query)
        records = cursor.fetchall()

        print("\n List of Course Prerequisites:")
        for row in records:
            print(f"Course: {row[0]} → Prerequisite: {row[1]}")

    except Exception as e:
        print("Error viewing prerequisites:", e)
    finally:
        if db.is_connected():
            db.close()
