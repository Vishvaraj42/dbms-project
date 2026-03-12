from flask import Flask, render_template, request, redirect, url_for
from db_connection import get_connection

app = Flask(__name__)

# ------------------------- HOME -------------------------
@app.route('/')
def home():
    return render_template('index.html')


# ------------------------- STUDENTS -------------------------
@app.route("/students", methods=["GET", "POST"])
def students():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        dept_id = request.form["dept_id"]

        cursor.execute(
            "INSERT INTO student (name, email, dept_id) VALUES (%s, %s, %s)",
            (name, email, dept_id)
        )
        db.commit()

    # Fetch all students with department names
    cursor.execute("""
        SELECT s.student_id, s.name, s.email, d.dept_name
        FROM student s
        LEFT JOIN department d ON s.dept_id = d.dept_id
    """)
    students = cursor.fetchall()

    # Fetch departments for dropdown
    cursor.execute("SELECT dept_id, dept_name FROM department ORDER BY dept_name")
    departments = cursor.fetchall()

    db.close()
    return render_template("students.html", students=students, departments=departments)


# ------------------------- COURSES -------------------------
@app.route('/courses', methods=['GET', 'POST'])
def courses():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        credits = request.form['credits']
        dept_id = request.form['dept_id']
        prereq = request.form.get('prereq_id')

        prereq_id = prereq if prereq else None

        cursor.execute("""
            INSERT INTO course (title, credits, prereq_id, dept_id)
            VALUES (%s, %s, %s, %s)
        """, (title, credits, prereq_id, dept_id))
        db.commit()

    # For table view
    cursor.execute("""
        SELECT c.course_id, c.title, c.credits,
               d.dept_name,
               p.title AS prereq_title
        FROM course c
        LEFT JOIN department d ON c.dept_id = d.dept_id
        LEFT JOIN course p ON c.prereq_id = p.course_id
        ORDER BY c.course_id
    """)
    courses = cursor.fetchall()

    # For dropdowns
    cursor.execute("SELECT dept_id, dept_name FROM department ORDER BY dept_name")
    departments = cursor.fetchall()

    cursor.execute("SELECT course_id, title FROM course ORDER BY title")
    all_courses = cursor.fetchall()

    db.close()
    return render_template(
        'courses.html',
        courses=courses,
        departments=departments,
        all_courses=all_courses
    )


# ------------------------- FACULTY -------------------------
@app.route("/faculty", methods=["GET", "POST"])
def faculty():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        dept_id = request.form.get("dept_id")

        if name and dept_id:  # ensure not empty
            cursor.execute(
                "INSERT INTO faculty (name, email, dept_id) VALUES (%s, %s, %s)",
                (name, email, dept_id)
            )
            db.commit()

    # fetch faculty with department name
    cursor.execute("""
        SELECT f.faculty_id, f.name, f.email, d.dept_name
        FROM faculty f
        LEFT JOIN department d ON f.dept_id = d.dept_id
        ORDER BY f.faculty_id
    """)
    faculty = cursor.fetchall()

    # fetch department list for dropdown
    cursor.execute("SELECT dept_id, dept_name FROM department ORDER BY dept_name")
    departments = cursor.fetchall()

    db.close()
    return render_template("faculty.html", faculty=faculty, departments=departments)


# ------------------------- DEPARTMENTS -------------------------
@app.route("/departments", methods=["GET", "POST"])
def departments():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        dept_name = request.form.get("dept_name")
        building = request.form.get("building")

        if dept_name:
            cursor.execute(
                "INSERT INTO department (dept_name, building) VALUES (%s, %s)",
                (dept_name, building)
            )
            db.commit()

    cursor.execute("SELECT * FROM department ORDER BY dept_id")
    departments = cursor.fetchall()
    db.close()
    return render_template("departments.html", departments=departments)


# ------------------------- CLASSROOMS -------------------------
@app.route("/classrooms", methods=["GET", "POST"])
def classrooms():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        room_number = request.form.get("room_number")
        dept_id = request.form.get("dept_id")
        building = request.form.get("building")

        if room_number and dept_id:
            cursor.execute("""
                INSERT INTO classroom (room_number, dept_id, building)
                VALUES (%s, %s, %s)
            """, (room_number, dept_id, building))
            db.commit()

    # fetch joined data
    cursor.execute("""
        SELECT c.classroom_id, c.room_number, d.dept_name, c.building
        FROM classroom c
        LEFT JOIN department d ON c.dept_id = d.dept_id
        ORDER BY c.classroom_id
    """)
    classrooms = cursor.fetchall()

    # dropdown
    cursor.execute("SELECT dept_id, dept_name FROM department ORDER BY dept_name")
    departments = cursor.fetchall()

    db.close()
    return render_template("classrooms.html", classrooms=classrooms, departments=departments)


# ------------------------- PREREQUISITES -------------------------
@app.route('/prerequisites', methods=['GET', 'POST'])
def prerequisites():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        course_id = request.form['course_id']
        prereq_course_id = request.form['prereq_course_id']
        cursor.execute("""
            INSERT INTO prerequisite (course_id, prereq_course_id)
            VALUES (%s, %s)
        """, (course_id, prereq_course_id))
        db.commit()

    cursor.execute("""
        SELECT p.prereq_id, c1.title AS course, c2.title AS prerequisite
        FROM prerequisite p
        JOIN course c1 ON p.course_id = c1.course_id
        JOIN course c2 ON p.prereq_course_id = c2.course_id
    """)
    prerequisites = cursor.fetchall()

    cursor.execute("SELECT course_id, title FROM course ORDER BY title")
    courses = cursor.fetchall()

    db.close()
    return render_template("prerequisites.html", prerequisites=prerequisites, courses=courses)

# ------------------------- ENROLLMENTS -------------------------
@app.route("/enrollments", methods=["GET", "POST"])
def enrollments():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        student_id = request.form.get("student_id")
        course_id = request.form.get("course_id")
        grade = request.form.get("grade")

        if student_id and course_id:
            cursor.execute("""
                INSERT INTO enrollment (student_id, course_id, grade)
                VALUES (%s, %s, %s)
            """, (student_id, course_id, grade))
            db.commit()

    # Fetch enrollment table with student & course names
    cursor.execute("""
        SELECT e.enrollment_id, s.name AS student_name, c.title AS course_title, e.grade
        FROM enrollment e
        LEFT JOIN student s ON e.student_id = s.student_id
        LEFT JOIN course c ON e.course_id = c.course_id
        ORDER BY e.enrollment_id
    """)
    enrollments = cursor.fetchall()

    # Fetch data for dropdowns
    cursor.execute("SELECT student_id, name FROM student ORDER BY name")
    students = cursor.fetchall()

    cursor.execute("SELECT course_id, title FROM course ORDER BY title")
    courses = cursor.fetchall()

    db.close()
    return render_template("enrollments.html", enrollments=enrollments, students=students, courses=courses)


# ------------------------- ATTENDANCE -------------------------
@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        enrollment_id = request.form.get("enrollment_id")
        attendance_date = request.form.get("attendance_date")
        status = request.form.get("status")

        if enrollment_id and attendance_date and status:
            cursor.execute("""
                INSERT INTO attendance (enrollment_id, attendance_date, status)
                VALUES (%s, %s, %s)
            """, (enrollment_id, attendance_date, status))
            db.commit()

    # Display attendance joined with student + course names
    cursor.execute("""
        SELECT a.attendance_id, s.name AS student_name, c.title AS course_title,
               a.attendance_date, a.status
        FROM attendance a
        JOIN enrollment e ON a.enrollment_id = e.enrollment_id
        JOIN student s ON e.student_id = s.student_id
        JOIN course c ON e.course_id = c.course_id
        ORDER BY a.attendance_id
    """)
    attendance = cursor.fetchall()

    # Dropdown for enrollments (student-course)
    cursor.execute("""
        SELECT e.enrollment_id,
               CONCAT(s.name, ' - ', c.title) AS student_course
        FROM enrollment e
        JOIN student s ON e.student_id = s.student_id
        JOIN course c ON e.course_id = c.course_id
        ORDER BY s.name
    """)
    enrollments = cursor.fetchall()

    db.close()
    return render_template("attendance.html", attendance=attendance, enrollments=enrollments)

@app.route("/attendance_report")
def attendance_report():
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            s.name AS student_name,
            c.title AS course_title,
            SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS attended,
            COUNT(a.attendance_id) AS total_classes,
            ROUND(SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) / COUNT(a.attendance_id) * 100, 2) AS percentage
        FROM attendance a
        JOIN enrollment e ON a.enrollment_id = e.enrollment_id
        JOIN student s ON e.student_id = s.student_id
        JOIN course c ON e.course_id = c.course_id
        GROUP BY s.name, c.title
        ORDER BY s.name, c.title
    """)
    report = cursor.fetchall()

    db.close()
    return render_template("attendance_report.html", report=report)


# ============================================================
# DELETE ROUTES FOR ALL TABLES
# ============================================================

# ---- STUDENT ----
@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
    db.commit()
    db.close()
    return redirect(url_for('students'))

# ---- COURSE ----
@app.route("/delete_course/<int:course_id>")
def delete_course(course_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
    db.commit()
    db.close()
    return redirect(url_for('courses'))

# ---- FACULTY ----
@app.route("/delete_faculty/<int:faculty_id>")
def delete_faculty(faculty_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM faculty WHERE faculty_id = %s", (faculty_id,))
    db.commit()
    db.close()
    return redirect(url_for('faculty'))

# ---- DEPARTMENT ----
@app.route("/delete_department/<int:dept_id>")
def delete_department(dept_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM department WHERE dept_id = %s", (dept_id,))
    db.commit()
    db.close()
    return redirect(url_for('departments'))

# ---- CLASSROOM ----
@app.route("/delete_classroom/<int:classroom_id>")
def delete_classroom(classroom_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM classroom WHERE classroom_id = %s", (classroom_id,))
    db.commit()
    db.close()
    return redirect(url_for('classrooms'))

# ---- ENROLLMENT ----
@app.route("/delete_enrollment/<int:enrollment_id>")
def delete_enrollment(enrollment_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM enrollment WHERE enrollment_id = %s", (enrollment_id,))
    db.commit()
    db.close()
    return redirect(url_for('enrollments'))

# ---- ATTENDANCE ----
@app.route("/delete_attendance/<int:attendance_id>")
def delete_attendance(attendance_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM attendance WHERE attendance_id = %s", (attendance_id,))
    db.commit()
    db.close()
    return redirect(url_for('attendance'))

# ---- PREREQUISITE ----
@app.route("/delete_prerequisite/<int:prereq_id>")
def delete_prerequisite(prereq_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM prerequisite WHERE prereq_id = %s", (prereq_id,))
    db.commit()
    db.close()
    return redirect(url_for('prerequisites'))

# ------------------------- UNIVERSAL SEARCH -------------------------
@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return render_template("search.html", results=None, query=query)

    db = get_connection()
    c = db.cursor(dictionary=True)

    # Try to detect if query is numeric (for IDs)
    is_id = query.isdigit()
    like = f"%{query}%"

    results = {}

    # Search Students
    if is_id:
        c.execute("SELECT * FROM student WHERE student_id = %s", (query,))
    else:
        c.execute("SELECT * FROM student WHERE name LIKE %s OR email LIKE %s", (like, like))
    results["students"] = c.fetchall()

    # Search Faculty
    if is_id:
        c.execute("SELECT * FROM faculty WHERE faculty_id = %s", (query,))
    else:
        c.execute("SELECT * FROM faculty WHERE name LIKE %s OR email LIKE %s", (like, like))
    results["faculty"] = c.fetchall()

    # Search Courses
    if is_id:
        c.execute("SELECT * FROM course WHERE course_id = %s", (query,))
    else:
        c.execute("SELECT * FROM course WHERE title LIKE %s", (like,))
    results["courses"] = c.fetchall()

    # Search Departments
    if is_id:
        c.execute("SELECT * FROM department WHERE dept_id = %s", (query,))
    else:
        c.execute("SELECT * FROM department WHERE dept_name LIKE %s", (like,))
    results["departments"] = c.fetchall()

    # Search Classrooms
    if is_id:
        c.execute("SELECT * FROM classroom WHERE classroom_id = %s", (query,))
    else:
        c.execute("SELECT * FROM classroom WHERE building LIKE %s OR room_number LIKE %s", (like, like))
    results["classrooms"] = c.fetchall()

    # Search Enrollments
    if is_id:
        c.execute("SELECT * FROM enrollment WHERE enrollment_id = %s", (query,))
    else:
        c.execute("""
            SELECT e.enrollment_id, s.name AS student, c.title AS course, e.grade
            FROM enrollment e
            JOIN student s ON e.student_id = s.student_id
            JOIN course c ON e.course_id = c.course_id
            WHERE s.name LIKE %s OR c.title LIKE %s
        """, (like, like))
    results["enrollments"] = c.fetchall()

    # Search Attendance
    if is_id:
        c.execute("SELECT * FROM attendance WHERE attendance_id = %s", (query,))
    else:
        c.execute("""
            SELECT a.attendance_id, s.name, c.title, a.attendance_date, a.status
            FROM attendance a
            JOIN enrollment e ON a.enrollment_id = e.enrollment_id
            JOIN student s ON e.student_id = s.student_id
            JOIN course c ON e.course_id = c.course_id
            WHERE s.name LIKE %s OR c.title LIKE %s
        """, (like, like))
    results["attendance"] = c.fetchall()

    db.close()

    return render_template("search.html", results=results, query=query)



# ------------------------- MAIN -------------------------
if __name__ == '__main__':
    app.run(debug=True)
