import csv
import os
import mysql.connector
from db_connection import get_connection
from tqdm import tqdm  # progress bar

CSV_DIR = "csv_data"


# ---------------------- Utility Helpers ----------------------

def _clean(val):
    """Trim whitespace and normalize empty strings."""
    if val is None:
        return None
    val = str(val).strip()
    return val if val != "" else None


def _to_int(val):
    """Convert string to int safely."""
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def _map_id(cursor, sql, val):
    """Safely map a string value to an ID using SQL lookup."""
    if val is None or str(val).strip() == "":
        return None
    try:
        cursor.execute(sql, (val,))
        result = cursor.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"⚠️ Lookup failed for '{val}': {err}")
        return None


def _count(cursor, table):
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    return cursor.fetchone()[0]


# ---------------------- Import Functions ----------------------

def import_departments(path=os.path.join(CSV_DIR, "departments.csv")):
    if not os.path.exists(path):
        print("⚠️ departments.csv not found, skipping")
        return

    db = get_connection()
    c = db.cursor()
    ins = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        print(f"\n📂 Importing {len(reader)} departments...")
        for r in tqdm(reader, desc="Departments", ncols=80, colour="green"):
            dept_name = _clean(r.get("dept_name"))
            building = _clean(r.get("building"))

            if not dept_name:
                continue

            try:
                c.execute(
                    "INSERT IGNORE INTO department (dept_name, building) VALUES (%s, %s)",
                    (dept_name, building)
                )
                ins += c.rowcount
            except mysql.connector.Error as err:
                tqdm.write(f"⚠️ Skipped department '{dept_name}': {err}")

    db.commit()
    print(f"✅ departments: {ins} inserted (now {_count(c, 'department')})")
    db.close()


def import_faculty(path=os.path.join(CSV_DIR, "faculty.csv")):
    if not os.path.exists(path):
        print("⚠️ faculty.csv not found, skipping")
        return

    db = get_connection()
    c = db.cursor()
    ins = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        print(f"\n📂 Importing {len(reader)} faculty members...")
        for r in tqdm(reader, desc="Faculty", ncols=80, colour="yellow"):
            name = _clean(r.get("name"))
            email = _clean(r.get("email"))
            dept_name = _clean(r.get("department"))

            dept_id = _map_id(c, "SELECT dept_id FROM department WHERE dept_name=%s", dept_name)

            if not name or dept_id is None:
                continue

            try:
                c.execute(
                    "INSERT IGNORE INTO faculty (name, email, dept_id) VALUES (%s, %s, %s)",
                    (name, email, dept_id)
                )
                ins += c.rowcount
            except mysql.connector.Error as err:
                tqdm.write(f"⚠️ Skipped faculty '{name}': {err}")

    db.commit()
    print(f"✅ faculty: {ins} inserted (now {_count(c, 'faculty')})")
    db.close()


def import_students(path=os.path.join(CSV_DIR, "students.csv")):
    if not os.path.exists(path):
        print("⚠️ students.csv not found, skipping")
        return

    db = get_connection()
    c = db.cursor()
    ins = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        print(f"\n📂 Importing {len(reader)} students...")
        for r in tqdm(reader, desc="Students", ncols=80, colour="cyan"):
            name = _clean(r.get("name"))
            email = _clean(r.get("email"))
            dept_name = _clean(r.get("department"))

            dept_id = _map_id(c, "SELECT dept_id FROM department WHERE dept_name=%s", dept_name)

            if not name or dept_id is None:
                continue

            try:
                c.execute(
                    "INSERT IGNORE INTO student (name, email, dept_id) VALUES (%s, %s, %s)",
                    (name, email, dept_id)
                )
                ins += c.rowcount
            except mysql.connector.Error as err:
                tqdm.write(f"⚠️ Skipped student '{name}': {err}")

    db.commit()
    print(f"✅ students: {ins} inserted (now {_count(c, 'student')})")
    db.close()


def import_courses(path=os.path.join(CSV_DIR, "courses.csv")):
    if not os.path.exists(path):
        print("⚠️ courses.csv not found, skipping")
        return

    db = get_connection()
    c = db.cursor()
    ins = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        print(f"\n📂 Importing {len(reader)} courses...")
        for r in tqdm(reader, desc="Courses", ncols=80, colour="magenta"):
            title = _clean(r.get("title"))
            credits = _to_int(r.get("credits"))
            dept_name = _clean(r.get("dept_name"))
            prereq_title = _clean(r.get("prereq_title"))

            dept_id = _map_id(c, "SELECT dept_id FROM department WHERE dept_name=%s", dept_name)
            prereq_id = _map_id(c, "SELECT course_id FROM course WHERE title=%s", prereq_title)

            if not title or dept_id is None:
                continue

            try:
                c.execute(
                    "INSERT IGNORE INTO course (title, credits, prereq_id, dept_id) VALUES (%s, %s, %s, %s)",
                    (title, credits, prereq_id, dept_id)
                )
                ins += c.rowcount
            except mysql.connector.Error as err:
                tqdm.write(f"⚠️ Skipped course '{title}': {err}")

    db.commit()
    print(f"✅ courses: {ins} inserted (now {_count(c, 'course')})")
    db.close()


def import_enrollments(path=os.path.join(CSV_DIR, "enrollments.csv")):
    if not os.path.exists(path):
        print("⚠️ enrollments.csv not found, skipping")
        return

    db = get_connection()
    c = db.cursor()
    ins = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        print(f"\n📂 Importing {len(reader)} enrollments...")

        for r in tqdm(reader, desc="Enrollments", ncols=80, colour="blue"):
            # read both possible formats
            student_id = _to_int(r.get("student_id"))
            course_id = _to_int(r.get("course_id"))
            student_email = _clean(r.get("student_email"))
            course_title = _clean(r.get("course_title"))
            grade = _clean(r.get("grade"))

            # if id missing, fall back to lookup by email/title
            if not student_id and student_email:
                student_id = _map_id(c, "SELECT student_id FROM student WHERE email=%s", student_email)
            if not course_id and course_title:
                course_id = _map_id(c, "SELECT course_id FROM course WHERE title=%s", course_title)

            # skip invalid rows
            if not student_id or not course_id:
                tqdm.write(f"⚠️ Skipped enrollment (invalid IDs): student_id={student_id}, course_id={course_id}")
                continue

            try:
                c.execute(
                    "INSERT IGNORE INTO enrollment (student_id, course_id, grade) VALUES (%s, %s, %s)",
                    (student_id, course_id, grade)
                )
                ins += c.rowcount
            except mysql.connector.Error as err:
                tqdm.write(f"⚠️ Skipped enrollment: {err}")

    db.commit()
    print(f"✅ enrollments: {ins} inserted (now {_count(c, 'enrollment')})")
    db.close()


def import_attendance(path=os.path.join(CSV_DIR, "attendance.csv")):
    if not os.path.exists(path):
        print("⚠️ attendance.csv not found, skipping")
        return

    db = get_connection()
    c = db.cursor()
    ins = 0

    with open(path, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        print(f"\n📂 Importing {len(reader)} attendance records...")

        for r in tqdm(reader, desc="Attendance", ncols=80, colour="white"):
            enrollment_id = _to_int(r.get("enrollment_id"))
            attendance_date = _clean(r.get("attendance_date"))
            status = _clean(r.get("status"))

            if not enrollment_id or not attendance_date:
                tqdm.write(f"⚠️ Skipped attendance (invalid row): enrollment_id={enrollment_id}")
                continue

            try:
                c.execute(
                    "INSERT IGNORE INTO attendance (enrollment_id, attendance_date, status) VALUES (%s, %s, %s)",
                    (enrollment_id, attendance_date, status)
                )
                ins += c.rowcount
            except mysql.connector.Error as err:
                tqdm.write(f"⚠️ Skipped attendance: {err}")

    db.commit()
    print(f"✅ attendance: {ins} inserted (now {_count(c, 'attendance')})")
    db.close()


# ---------------------- Master Import Runner ----------------------

def import_all():
    print("🚀 Starting CSV data import...\n")
    import_departments()
    import_faculty()
    import_students()
    import_courses()
    import_enrollments()
    import_attendance()
    print("\n🎉 All CSV imports completed successfully!")


if __name__ == "__main__":
    import_all()
