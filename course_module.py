from db_connection import get_connection

def add_course():
    db = get_connection()
    cursor = db.cursor()
    title = input("Enter course title: ")
    credits = int(input("Enter credits: "))
    prereq = input("Enter prerequisite course ID (or press Enter if none): ")
    prereq = int(prereq) if prereq else None

    cursor.execute("INSERT INTO course (title, credits, prereq_id) VALUES (%s, %s, %s)",
                   (title, credits, prereq))
    db.commit()
    print("Course added successfully!")
    db.close()

def view_courses():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM course")
    rows = cursor.fetchall()

    print("\n--- Course List ---")
    for r in rows:
        print(f"ID: {r[0]} | Title: {r[1]} | Credits: {r[2]} | Prerequisite: {r[3]}")
    db.close()
