import mysql.connector
from datetime import date

# Connect to MySQL database
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@amulya123",
    database="student_attendence"
)

cursor = con.cursor()


# 1. Add a student
def add_student():
    name = input("Enter student name: ")
    course = input("Enter course: ")

    sql = "INSERT INTO students (name, course) VALUES (%s, %s)"
    cursor.execute(sql, (name, course))
    con.commit()

    print("Student added successfully!")


# 2. View all students
def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("No students found.")
        return

    print("\n--- Student Details ---")
    for student in students:
        print(
            f"ID: {student[0]}, "
            f"Name: {student[1]}, "
            f"Course: {student[2]}"
        )


# 3. Mark attendance
def mark_attendance():
    view_students()

    try:
        student_id = int(input("\nEnter student ID: "))
    except ValueError:
        print("Please enter a valid student ID.")
        return

    status = input("Enter status (Present/Absent): ").strip().title()

    if status not in ("Present", "Absent"):
        print("Invalid status. Enter Present or Absent.")
        return

    today = date.today()

    sql = """
        INSERT INTO attendance
        (student_id, attendance_date, status)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE status = %s
    """

    try:
        cursor.execute(
            sql, (student_id, today, status, status)
        )
        con.commit()
        print("Attendance marked successfully!")

    except mysql.connector.Error as error:
        con.rollback()
        print("Error:", error)


# 4. View attendance records
def view_attendance():
    sql = """
        SELECT s.student_id, s.name,
               a.attendance_date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        ORDER BY a.attendance_date DESC, s.name
    """

    cursor.execute(sql)
    records = cursor.fetchall()

    if not records:
        print("No attendance records found.")
        return

    print("\n--- Attendance Records ---")
    for record in records:
        print(
            f"ID: {record[0]}, "
            f"Name: {record[1]}, "
            f"Date: {record[2]}, "
            f"Status: {record[3]}"
        )


# 5. View attendance for a particular date
def attendance_by_date():
    date_input = input("Enter date (YYYY-MM-DD): ")

    try:
        selected_date = date.fromisoformat(date_input)
    except ValueError:
        print("Invalid date format.")
        return

    sql = """
        SELECT s.student_id, s.name, a.status
        FROM students s
        LEFT JOIN attendance a
        ON s.student_id = a.student_id
        AND a.attendance_date = %s
        ORDER BY s.student_id
    """

    cursor.execute(sql, (selected_date,))
    records = cursor.fetchall()

    print(f"\n--- Attendance for {selected_date} ---")
    for record in records:
        status = record[2] if record[2] else "Not Marked"
        print(f"ID: {record[0]}, Name: {record[1]}, Status: {status}")


# Main menu
while True:
    print("\n===== Student Attendance Management System =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Mark Attendance")
    print("4. View All Attendance")
    print("5. View Attendance by Date")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        mark_attendance()
    elif choice == "4":
        view_attendance()
    elif choice == "5":
        attendance_by_date()
    elif choice == "6":
        print("Thank you for using the system!")
        break
    else:
        print("Invalid choice. Please try again.")

cursor.close()
con.close()
