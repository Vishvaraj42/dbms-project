import csv, os, random
from faker import Faker

fake = Faker()
os.makedirs("csv_data", exist_ok=True)

# -----------------------------
# 1️⃣ Departments (12 total)
# -----------------------------
departments = [
    ("Computer Science", "Block-A"),
    ("Information Technology", "Block-A"),
    ("Mechanical", "Block-B"),
    ("Civil", "Block-B"),
    ("Electrical", "Block-C"),
    ("Electronics", "Block-C"),
    ("Mathematics", "Block-D"),
    ("Physics", "Block-D"),
    ("Chemistry", "Block-E"),
    ("Biotechnology", "Block-E"),
    ("Business Administration", "Block-F"),
    ("Economics", "Block-F"),
]

with open("csv_data/departments.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["dept_name", "building"])
    writer.writerows(departments)
print("✅ departments.csv created")

# -----------------------------
# 2️⃣ Courses (100 courses)
# -----------------------------
courses = []
for i in range(1, 101):
    dept = random.choice(departments)
    title = f"{dept[0]} {fake.word().capitalize()} {i}"
    credits = random.randint(2, 5)
    prereq = None if random.random() > 0.7 else f"Course-{random.randint(1, i)}"
    courses.append([title, credits, prereq, dept[0]])

with open("csv_data/courses.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "credits", "prereq_title", "dept_name"])
    writer.writerows(courses)
print("✅ courses.csv created")

# -----------------------------
# 3️⃣ Faculty (250)
# -----------------------------
faculty = []
for i in range(250):
    name = fake.name()
    email = fake.unique.email()
    dept = random.choice(departments)
    faculty.append([name, email, dept[0]])

with open("csv_data/faculty.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "email", "dept_name"])
    writer.writerows(faculty)
print("✅ faculty.csv created")

# -----------------------------
# 4️⃣ Students (4000)
# -----------------------------
students = []
for i in range(4000):
    name = fake.name()
    email = fake.unique.email()
    dept = random.choice(departments)
    students.append([name, email, dept[0]])

with open("csv_data/students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "email", "dept_name"])
    writer.writerows(students)
print("✅ students.csv created")

# -----------------------------
# 5️⃣ Classrooms (80)
# -----------------------------
classrooms = []
for i in range(80):
    building = random.choice([d[1] for d in departments])
    room_number = str(random.randint(100, 499))
    capacity = random.randint(40, 120)
    classrooms.append([building, room_number, capacity])

with open("csv_data/classrooms.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["building", "room_number", "capacity"])
    writer.writerows(classrooms)
print("✅ classrooms.csv created")

# -----------------------------
# 6️⃣ Enrollments (5000)
# -----------------------------
enrollments = []
for i in range(5000):
    student_id = random.randint(1, 4000)
    course_id = random.randint(1, 100)
    grade = random.choice(["A", "B", "C", "D", "E", "F"])
    enrollments.append([student_id, course_id, grade])

with open("csv_data/enrollments.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["student_id", "course_id", "grade"])
    writer.writerows(enrollments)
print("✅ enrollments.csv created")

# -----------------------------
# 7️⃣ Attendance (15000)
# -----------------------------
attendance = []
for i in range(15000):
    enrollment_id = random.randint(1, 5000)
    date = fake.date_this_year()
    status = random.choice(["Present", "Absent"])
    attendance.append([enrollment_id, date, status])

with open("csv_data/attendance.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["enrollment_id", "attendance_date", "status"])
    writer.writerows(attendance)
print("✅ attendance.csv created")

print("\n🎉 All relational CSVs generated in 'csv_data/' folder successfully!")
