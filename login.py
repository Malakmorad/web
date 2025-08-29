import mysql.connector

def login(user_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="exam_system"
    )
    cursor = conn.cursor()

    if user_name.lower() == "admin":
        print("Welcome Admin! Redirecting to Dashboard...")
        # هنا ممكن تضيف كود فتح الداشبورد
        return "admin"

    cursor.execute("SELECT student_id FROM students WHERE student_name = %s", (user_name,))
    student = cursor.fetchone()

    if not student:
        print(f"{user_name} not found, adding to the database...")
        cursor.execute("INSERT INTO students (student_name) VALUES (%s)", (user_name,))
        conn.commit()
        student_id = cursor.lastrowid
    else:
        student_id = student[0]

    cursor.execute("""
        SELECT e.exam_name, sc.score
        FROM exams e
        LEFT JOIN student_scores sc ON sc.exam_id = e.exam_id AND sc.student_id = %s
    """, (student_id,))
    results = cursor.fetchall()

    print(f"Results for {user_name}:")
    for r in results:
        print(f"Exam: {r[0]}, Score: {r[1] if r[1] is not None else 'N/A'}")

    cursor.close()
    conn.close()
    return "student"
