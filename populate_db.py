import mysql.connector
from mysql.connector import Error

# الاتصال بقاعدة البيانات
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="exam_system"
    )
    cursor = conn.cursor()
except Error as e:
    print("Error connecting to MySQL:", e)
    exit()

# إنشاء الجداول لو مش موجودة
def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(100) NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            exam_id INT AUTO_INCREMENT PRIMARY KEY,
            exam_name VARCHAR(100) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_scores (
            score_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            exam_id INT,
            score INT,
            flag VARCHAR(20),
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(exam_id) REFERENCES exams(exam_id)
        )
    """)
    conn.commit()

# مسح البيانات القديمة
def clear_data():
    cursor.execute("DELETE FROM student_scores")
    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM exams")
    conn.commit()

# إضافة طلاب افتراضيين
def create_students(names=None):
    if names is None:
        names = ["Ali", "Sara", "Omar", "Laila", "Khalid", "Mona", "Hassan", "Nada", "Fadi", "Reem"]
    for name in names:
        try:
            cursor.execute("INSERT INTO students (student_name) VALUES (%s)", (name,))
        except:
            pass
    conn.commit()

# إضافة امتحانات افتراضية
def create_exams():
    exams = ["Math", "Physics", "Chemistry", "English", "Biology"]
    for exam in exams:
        cursor.execute("INSERT IGNORE INTO exams (exam_name) VALUES (%s)", (exam,))
    conn.commit()

# إضافة درجات افتراضية لكل طالب لكل امتحان
def populate_scores():
    cursor.execute("SELECT student_id FROM students")
    students = cursor.fetchall()
    cursor.execute("SELECT exam_id FROM exams")
    exams = cursor.fetchall()

    for s in students:
        for e in exams:
            score = 50 + int((s[0]*e[0]) % 50)
            cursor.execute(
                "INSERT INTO student_scores (student_id, exam_id, score, flag) VALUES (%s, %s, %s, %s)",
                (s[0], e[0], score, None)
            )
    conn.commit()

# تنفيذ الدوال
if __name__ == "__main__":
    create_tables()
    clear_data()
    create_students()
    create_exams()
    populate_scores()
    print("Database populated successfully!")

cursor.close()
conn.close()
