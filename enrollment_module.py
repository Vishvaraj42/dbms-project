
from db_connection import get_connection

def register_course():
    db = get_connection()
    cursor = db.cursor()
    student_id = int(input("Enter student ID: "))
    course_id = int(input("Enter course ID: "))

    cursor.execute("SELECT prereq_id FROM course WHERE course_id = %s", (course_id,))
    prereq = cursor.fetchone()

    if prereq and prereq[0] is not None:
        cursor.execute("""
            SELECT * FROM enrollment WHERE student_id = %s AND course_id = %s
        """, (student_id, prereq[0]))
        passed = cursor.fetchone()
        if not passed:
            print("Cannot register — prerequisite not completed.")
            db.close()
            return

    cursor.execute("INSERT INTO enrollment (student_id, course_id, grade) VALUES (%s, %s, NULL)",
                   (student_id, course_id))
    db.commit()
    print("Registration successful!")
    db.close()

def view_enrollments():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT e.enrollment_id, s.name, c.title, e.grade
        FROM enrollment e
        JOIN student s ON e.student_id = s.student_id
        JOIN course c ON e.course_id = c.course_id
    """)
    rows = cursor.fetchall()

    print("\n--- Enrollments ---")
    for r in rows:
        print(f"Enroll ID: {r[0]} | Student: {r[1]} | Course: {r[2]} | Grade: {r[3]}")
    db.close()
