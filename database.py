import mysql.connector

# الاتصال بقاعدة البيانات
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="exam_system"
)
cursor = conn.cursor()

# إضافة طلاب افتراضيين
def create_students():
    students = ["Ali", "Sara", "Omar", "Laila", "Khalid", "Mona", "Hassan", "Nada", "Fadi", "Reem"]
    for name in students:
        cursor.execute("INSERT INTO students (student_name) VALUES (%s)", (name,))
    conn.commit()

# إضافة درجات افتراضية لكل طالب لكل امتحان
def populate_scores():
    cursor.execute("SELECT student_id FROM students")
    students = cursor.fetchall()
    cursor.execute("SELECT exam_id FROM exams")
    exams = cursor.fetchall()

    for s in students:
        for e in exams:
            score = 50 + int((s[0]*e[0]) % 50)  # درجات افتراضية عشوائية
            cursor.execute(
                "INSERT INTO student_scores (student_id, exam_id, score, flag) VALUES (%s, %s, %s, %s)",
                (s[0], e[0], score, None)
            )
    conn.commit()

# إنشاء البيانات عند التشغيل
create_students()
populate_scores()

cursor.close()
conn.close()
print("Database populated successfully!")
