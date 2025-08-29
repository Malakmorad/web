import sqlite3
from datetime import datetime, timedelta
import random

def get_db_connection():
    try:
        conn = sqlite3.connect('exam_system.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print("Error connecting to SQLite:", e)
        return None

def populate_comparison_data():
    """ملء قاعدة البيانات ببيانات تجريبية للمقارنة"""
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    cursor = conn.cursor()
    
    try:
        # إنشاء جدول test_results إذا لم يكن موجوداً
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                test_type TEXT NOT NULL,
                score INTEGER NOT NULL,
                percentage REAL NOT NULL,
                grade TEXT NOT NULL,
                submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # مسح البيانات الموجودة
        cursor.execute("DELETE FROM test_results")
        
        # قائمة أسماء الطلاب
        students = [
            "أحمد محمد", "فاطمة علي", "محمد أحمد", "عائشة حسن", "علي محمود",
            "مريم عبدالله", "حسن إبراهيم", "خديجة محمد", "إبراهيم علي", "زينب أحمد",
            "محمود حسن", "نور الدين", "سارة محمد", "عبدالله أحمد", "ليلى علي",
            "يوسف محمد", "آمنة حسن", "عمر أحمد", "رنا محمد", "كريم علي"
        ]
        
        # تعريف المجموعات
        before_tests = ['test1', 'test2', 'test3', 'test4']
        after_tests = ['test1(2)', 'testtashely', 'mlahza']
        
        # بيانات تجريبية للمجموعة الأولى (قبل التعلم) - أداء منخفض نسبياً
        before_scores = {
            'test1': {'min': 40, 'max': 70, 'avg': 55},
            'test2': {'min': 35, 'max': 65, 'avg': 50},
            'test3': {'min': 30, 'max': 60, 'avg': 45},
            'test4': {'min': 45, 'max': 75, 'avg': 60}
        }
        
        # بيانات تجريبية للمجموعة الثانية (بعد التعلم) - أداء أعلى نسبياً
        after_scores = {
            'test1(2)': {'min': 60, 'max': 90, 'avg': 75},
            'testtashely': {'min': 65, 'max': 95, 'avg': 80},
            'mlahza': {'min': 70, 'max': 100, 'avg': 85}
        }
        
        # إدراج بيانات المجموعة الأولى
        print("إدراج بيانات المجموعة الأولى (قبل التعلم)...")
        for student in students:
            for test_type, score_range in before_scores.items():
                # توليد درجة عشوائية مع توزيع طبيعي حول المتوسط
                score = random.normalvariate(score_range['avg'], 10)
                score = max(score_range['min'], min(score_range['max'], score))
                score = int(score)
                
                percentage = score
                grade = get_grade(percentage)
                
                # تاريخ عشوائي في الشهر الماضي
                random_days = random.randint(30, 60)
                submission_date = datetime.now() - timedelta(days=random_days)
                
                cursor.execute("""
                    INSERT INTO test_results (student_name, test_type, score, percentage, grade, submission_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (student, test_type, score, percentage, grade, submission_date))
        
        # إدراج بيانات المجموعة الثانية
        print("إدراج بيانات المجموعة الثانية (بعد التعلم)...")
        for student in students:
            for test_type, score_range in after_scores.items():
                # توليد درجة عشوائية مع توزيع طبيعي حول المتوسط
                score = random.normalvariate(score_range['avg'], 8)
                score = max(score_range['min'], min(score_range['max'], score))
                score = int(score)
                
                percentage = score
                grade = get_grade(percentage)
                
                # تاريخ عشوائي في الأسبوع الماضي
                random_days = random.randint(1, 7)
                submission_date = datetime.now() - timedelta(days=random_days)
                
                cursor.execute("""
                    INSERT INTO test_results (student_name, test_type, score, percentage, grade, submission_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (student, test_type, score, percentage, grade, submission_date))
        
        conn.commit()
        print(f"تم إدراج {len(students) * (len(before_tests) + len(after_tests))} نتيجة اختبار بنجاح")
        
        # عرض إحصائيات سريعة
        print("\nإحصائيات سريعة:")
        for test_type in before_tests + after_tests:
            cursor.execute("""
                SELECT AVG(percentage) as avg_score, COUNT(*) as count
                FROM test_results 
                WHERE test_type = ?
            """, (test_type,))
            result = cursor.fetchone()
            if result:
                print(f"{test_type}: متوسط {result[0]:.1f}% من {result[1]} اختبار")
        
    except Exception as e:
        print(f"Error populating comparison data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_grade(percentage):
    """تحديد التقدير بناءً على النسبة المئوية"""
    if percentage >= 90:
        return "ممتاز"
    elif percentage >= 80:
        return "جيد جداً"
    elif percentage >= 70:
        return "جيد"
    elif percentage >= 60:
        return "مقبول"
    else:
        return "ضعيف"

if __name__ == "__main__":
    print("بدء ملء قاعدة البيانات ببيانات المقارنة...")
    populate_comparison_data()
    print("تم الانتهاء من ملء قاعدة البيانات!")


