
from db_connection import get_connection

def mark_attendance():
    """Marks attendance for a student (based on enrollment ID)."""
    try:
        db = get_connection()
        if db is None:
            print("Database connection failed.")
            return

        cursor = db.cursor()

        
        enrollment_id = int(input("Enter Enrollment ID: "))
        attendance_date = input("Enter Attendance Date (YYYY-MM-DD): ")
        status = input("Enter Status (Present/Absent): ").capitalize()

        if status not in ['Present', 'Absent']:
            print("Invalid status! Enter either 'Present' or 'Absent'.")
            return

      
        cursor.execute("SELECT * FROM enrollment WHERE enrollment_id = %s", (enrollment_id,))
        enrollment = cursor.fetchone()

        if not enrollment:
            print("Invalid Enrollment ID! No such student-course record exists.")
            return

     
        query = """
            INSERT INTO attendance (enrollment_id, attendance_date, status)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (enrollment_id, attendance_date, status))
        db.commit()

        print("✅ Attendance marked successfully!")

    except Exception as e:
        print("Error marking attendance:", e)

    finally:
        if db.is_connected():
            cursor.close()
            db.close()


def view_attendance():
    """Displays all attendance records."""
    try:
        db = get_connection()
        if db is None:
            print("Database connection failed.")
            return

        cursor = db.cursor()

        query = """
            SELECT 
                a.attendance_id,
                s.name AS student_name,
                c.title,
                a.attendance_date,
                a.status
            FROM attendance a
            JOIN enrollment e ON a.enrollment_id = e.enrollment_id
            JOIN student s ON e.student_id = s.student_id
            JOIN course c ON e.course_id = c.course_id
            ORDER BY a.attendance_date DESC;
        """
        cursor.execute(query)
        records = cursor.fetchall()

        print("\nAttendance Records:")
        print("-" * 60)
        for row in records:
            print(f"ID: {row[0]}, Student: {row[1]}, Course: {row[2]}, Date: {row[3]}, Status: {row[4]}")
        print("-" * 60)

    except Exception as e:
        print("Error viewing attendance:", e)

    finally:
        if db.is_connected():
            cursor.close()
            db.close()
