
from student_module import add_student, view_students
from course_module import add_course, view_courses
from enrollment_module import register_course, view_enrollments
from prerequisite_module import add_prerequisite, view_prerequisites
from faculty_module import add_faculty, view_faculty
from department_module import add_department, view_departments
from classroom_module import add_classroom, view_classrooms
from attendance_module import mark_attendance, view_attendance


def main_menu():
    while True:
        print("  UNIVERSITY COURSE MANAGEMENT SYSTEM")
        print("1.  Add Student")
        print("2.  View Students")
        print("3.  Add Course")
        print("4.  View Courses")
        print("5.  Register Student to Course")
        print("6.  View Enrollments")
        print("7.  Add Prerequisite")
        print("8.  View Prerequisites")
        print("9.  Add Faculty")
        print("10. View Faculty")
        print("11. Add Department")
        print("12. View Departments")
        print("13. Add Classroom")
        print("14. View Classrooms")
        print("15. Mark Attendance")
        print("16. View Attendance")
        print("17. Exit")
        

        choice = input("Enter your choice (1-17): ").strip()

        try:
            if choice == '1':
                add_student()
            elif choice == '2':
                view_students()
            elif choice == '3':
                add_course()
            elif choice == '4':
                view_courses()
            elif choice == '5':
                register_course()
            elif choice == '6':
                view_enrollments()
            elif choice == '7':
                add_prerequisite()
            elif choice == '8':
                view_prerequisites()
            elif choice == '9':
                add_faculty()
            elif choice == '10':
                view_faculty()
            elif choice == '11':
                add_department()
            elif choice == '12':
                view_departments()
            elif choice == '13':
                add_classroom()
            elif choice == '14':
                view_classrooms()
            elif choice == '15':
                mark_attendance()
            elif choice == '16':
                view_attendance()

            elif choice == '17':
                print("\n Exiting... Thank you for using the system!")
                break
            else:
                print(" Invalid choice! Please enter a number between 1 and 17.")
        except Exception as e:
            print(" Error occurred:", e)

if __name__ == "__main__":
    main_menu()
