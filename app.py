
from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Use SQLite instead of MySQL for easier setup
def get_db_connection():
    try:
        conn = sqlite3.connect('exam_system.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print("Error connecting to SQLite:", e)
        return None

# إنشاء الجداول لو مش موجودة
def create_tables():
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exams (
                exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_name TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_scores (
                score_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                exam_id INTEGER,
                score INTEGER,
                flag TEXT,
                FOREIGN KEY(student_id) REFERENCES students(student_id),
                FOREIGN KEY(exam_id) REFERENCES exams(exam_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS digital_intelligence_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                total_score INTEGER NOT NULL,
                percentage REAL NOT NULL,
                grade TEXT NOT NULL,
                submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_logins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN DEFAULT 1
            )
        """)
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
        conn.commit()
        return True
    except Exception as e:
        print("Error creating tables:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# مسح البيانات القديمة
def clear_data():
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM student_scores")
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM exams")
        conn.commit()
        return True
    except Exception as e:
        print("Error clearing data:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# إضافة طلاب افتراضيين
def create_students(names=None):
    if names is None:
        names = ["Ali", "Sara", "Omar", "Laila", "Khalid", "Mona", "Hassan", "Nada", "Fadi", "Reem"]
    
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    try:
        for name in names:
            try:
                cursor.execute("INSERT INTO students (student_name) VALUES (?)", (name,))
            except:
                pass
        conn.commit()
        return True
    except Exception as e:
        print("Error creating students:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# إضافة امتحانات افتراضية
def create_exams():
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    try:
        exams = ["Math", "Physics", "Chemistry", "English", "Biology"]
        for exam in exams:
            cursor.execute("INSERT OR IGNORE INTO exams (exam_name) VALUES (?)", (exam,))
        conn.commit()
        return True
    except Exception as e:
        print("Error creating exams:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# إضافة درجات افتراضية لكل طالب لكل امتحان
def populate_scores():
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT student_id FROM students")
        students = cursor.fetchall()
        cursor.execute("SELECT exam_id FROM exams")
        exams = cursor.fetchall()

        for s in students:
            for e in exams:
                score = 50 + int((s[0]*e[0]) % 50)
                cursor.execute(
                    "INSERT INTO student_scores (student_id, exam_id, score, flag) VALUES (?, ?, ?, ?)",
                    (s[0], e[0], score, None)
                )
        conn.commit()
        return True
    except Exception as e:
        print("Error populating scores:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# تسجيل الدخول وربطه بالواجهة الأمامية
def login(user_name):
    if user_name.lower() in ["naglaa saed", "heba heseen"]:
        return "dashboard.html"  # رابط صفحة الادمن

    # التأكد من وجود الطالب
    conn = get_db_connection()
    if not conn:
        return "error.html"
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT student_id FROM students WHERE student_name = ?", (user_name,))
        student = cursor.fetchone()
        if not student:
            print(f"{user_name} not found, adding to the database...")
            create_students([user_name])
            student_id = cursor.lastrowid
        else:
            student_id = student[0]

        # عرض النتائج
        cursor.execute("""
            SELECT e.exam_name, sc.score
            FROM exams e
                LEFT JOIN student_scores sc ON sc.exam_id = e.exam_id AND sc.student_id = ?
        """, (student_id,))
        results = cursor.fetchall()
        
        print(f"Results for {user_name}:")
        for r in results:
            print(f"Exam: {r[0]}, Score: {r[1] if r[1] is not None else 'N/A'}")
        
        return "results.html"  # رابط صفحة الطالب
    except Exception as e:
        print("Error in login:", e)
        return "error.html"
    finally:
        cursor.close()
        conn.close()

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test1')
def test1():
    return render_template('test1.html')

@app.route('/test2')
def test2():
    return render_template('test2.html')

@app.route('/test3')
def test3():
    return render_template('test3.html')

@app.route('/test4')
def test4():
    return render_template('test4.html')

@app.route('/test1(2)')
def test1_2():
    return render_template('test1(2).html')

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_route():
    try:
        data = request.get_json()
        username = data.get('username', '')
        password = data.get('password', '')
        
        # Save login attempt to database
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        try:
            # Check if user exists and password is correct
            users = {}
            
            # Add specific admins
            users['naglaa saed'] = {'password': 'admin123', 'role': 'admin'}
            users['heba heseen'] = {'password': 'admin456', 'role': 'admin'}
            
            # Add regular users (user1, user2, user3, etc.)
            for i in range(1, 99):
                user_key = f'user{i}'
                users[user_key] = {'password': f'user{i}pass', 'role': 'user'}
            
            # Check credentials
            if username in users and users[username]['password'] == password:
                # Save successful login
                cursor.execute("""
                    INSERT INTO user_logins (username, password, role, success)
                    VALUES (?, ?, ?, ?)
                """, (username, password, users[username]['role'], True))
                conn.commit()
                
                # Determine redirect page
                if users[username]['role'] == 'admin':
                    return jsonify({'redirect': '/dashboard', 'success': True})
                else:
                    return jsonify({'redirect': '/test1', 'success': True})
            else:
                # Save failed login attempt
                cursor.execute("""
                    INSERT INTO user_logins (username, password, role, success)
                    VALUES (?, ?, ?, ?)
                """, (username, password, 'unknown', False))
                conn.commit()
                
                return jsonify({'error': 'Invalid credentials', 'success': False}), 401
                
        except Exception as e:
            print("Error in login:", e)
            return jsonify({'error': 'Database error'}), 500
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        print("Error in login_route:", e)
        return jsonify({'error': 'Server error'}), 500

@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    try:
        data = request.get_json()
        
        # Save to database
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        try:
            # Save to test_results table
            cursor.execute("""
                INSERT INTO test_results 
                (student_name, test_type, score, percentage, grade, submission_date) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data.get('student_name', 'Unknown'),
                data.get('test_type', 'Digital Intelligence'),
                data.get('total_score', 0),
                data.get('percentage', 0),
                data.get('grade', 'Unknown'),
                data.get('submission_date', datetime.now().isoformat())
            ))
            
            # Also save to digital_intelligence_scores for backward compatibility
            cursor.execute("""
                INSERT INTO digital_intelligence_scores 
                (student_name, total_score, percentage, grade) 
                VALUES (?, ?, ?, ?)
            """, (
                data.get('student_name', 'Unknown'),
                data.get('total_score', 0),
                data.get('percentage', 0),
                data.get('grade', 'Unknown')
            ))
            
            conn.commit()
            
            return jsonify({
                'message': 'تم حفظ التقييم بنجاح!',
                'success': True
            })
        except Exception as e:
            print("Error saving exam:", e)
            return jsonify({'error': 'Database error'}), 500
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        print("Error in submit_exam:", e)
        return jsonify({'error': 'Server error'}), 500

@app.route('/test3.html')
def test3_html():
    return render_template('test3.html')

@app.route('/a_aural')
def a_aural():
    return render_template('a_aural.html')

@app.route('/a_aural.html')
def a_aural_html():
    return render_template('a_aural.html')

@app.route('/b_visual')
def b_visual():
    return render_template('b_visual.html')

@app.route('/b_visual.html')
def b_visual_html():
    return render_template('b_visual.html')

@app.route('/dino')
def dino():
    return render_template("dino.html")

# Added routes for aural flow pages
@app.route('/testtashely')
def testtashely_route():
    return render_template('testtashely.html')

@app.route('/observation-ar')
def observation_ar_route():
    return render_template('ملاحظه.html')

@app.route('/congratulations')
def congratulations_route():
    return render_template('congratulations.html')



@app.route('/dashboard')
def dashboard():
    # Get dashboard statistics
    conn = get_db_connection()
    if not conn:
        return render_template('dashboard.html', stats={})
    
    cursor = conn.cursor()
    try:
        # Get total users
        cursor.execute("SELECT COUNT(DISTINCT username) FROM user_logins WHERE success = 1")
        total_users = cursor.fetchone()[0]
        
        # Get total test results
        cursor.execute("SELECT COUNT(*) FROM test_results")
        total_tests = cursor.fetchone()[0]
        
        # Get average score
        cursor.execute("SELECT AVG(percentage) FROM test_results")
        avg_score = cursor.fetchone()[0] or 0
        
        # Get recent logins
        cursor.execute("""
            SELECT username, login_time, success 
            FROM user_logins 
            ORDER BY login_time DESC 
            LIMIT 10
        """)
        recent_logins = cursor.fetchall()
        
        # Get recent test results
        cursor.execute("""
            SELECT student_name, test_type, score, percentage, grade, submission_date 
            FROM test_results 
            ORDER BY submission_date DESC 
            LIMIT 10
        """)
        recent_tests = cursor.fetchall()
        
        stats = {
            'total_users': total_users,
            'total_tests': total_tests,
            'avg_score': round(avg_score, 1),
            'recent_logins': recent_logins,
            'recent_tests': recent_tests
        }
        
        return render_template('dashboard.html', stats=stats)
        
    except Exception as e:
        print("Error getting dashboard data:", e)
        return render_template('dashboard.html', stats={})
    finally:
        cursor.close()
        conn.close()

@app.route('/dashboard.html')
def dashboard_html():
    return render_template('dashboard.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/comparison')
def comparison():
    return render_template('comparison.html')

@app.route('/api/comparison-data')
def get_comparison_data():
    """API endpoint للحصول على بيانات المقارنة من قاعدة البيانات"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'})
    
    cursor = conn.cursor()
    try:
        # تعريف المجموعات
        before_tests = ['test1', 'test2', 'test3', 'test4']
        after_tests = ['test1(2)', 'testtashely', 'mlahza']
        
        # جمع بيانات المجموعة الأولى (قبل التعلم)
        before_scores = []
        for test in before_tests:
            cursor.execute("""
                SELECT AVG(percentage) as avg_score, COUNT(*) as count
                FROM test_results 
                WHERE test_type = ?
            """, (test,))
            result = cursor.fetchone()
            if result and result[0]:
                before_scores.append({
                    'test': test,
                    'average': round(result[0], 1),
                    'count': result[1]
                })
        
        # جمع بيانات المجموعة الثانية (بعد التعلم)
        after_scores = []
        for test in after_tests:
            cursor.execute("""
                SELECT AVG(percentage) as avg_score, COUNT(*) as count
                FROM test_results 
                WHERE test_type = ?
            """, (test,))
            result = cursor.fetchone()
            if result and result[0]:
                after_scores.append({
                    'test': test,
                    'average': round(result[0], 1),
                    'count': result[1]
                })
       


        # حساب المتوسطات الإجمالية
        before_avg = sum(score['average'] for score in before_scores) / len(before_scores) if before_scores else 0
        after_avg = sum(score['average'] for score in after_scores) / len(after_scores) if after_scores else 0
        
        # حساب معدل التحسن
        improvement_rate = 0
        if before_avg > 0:
            improvement_rate = ((after_avg - before_avg) / before_avg) * 100
        
        # إحصائيات إضافية
        cursor.execute("SELECT COUNT(DISTINCT student_name) FROM test_results")
        total_students = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM test_results")
        total_tests_taken = cursor.fetchone()[0]
        
        # أفضل اختبار
        cursor.execute("""
            SELECT test_type, AVG(percentage) as avg_score
            FROM test_results 
            GROUP BY test_type 
            ORDER BY avg_score DESC 
            LIMIT 1
        """)
        best_test_result = cursor.fetchone()
        best_test = best_test_result[0] if best_test_result else '--'
        
        return jsonify({
            'before_tests': before_scores,
            'after_tests': after_scores,
            'before_average': round(before_avg, 1),
            'after_average': round(after_avg, 1),
            'improvement_rate': round(improvement_rate, 1),
            'total_students': total_students,
            'total_tests_taken': total_tests_taken,
            'best_test': best_test
        })
        
    except Exception as e:
        print("Error getting comparison data:", e)
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/api/save-test-result', methods=['POST'])
def save_test_result():
    """API endpoint لحفظ نتائج الاختبارات"""
    try:
        data = request.get_json()
        student_name = data.get('student_name')
        test_type = data.get('test_type')
        score = data.get('score')
        percentage = data.get('percentage')
        grade = data.get('grade')
        
        if not all([student_name, test_type, score, percentage, grade]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO test_results (student_name, test_type, score, percentage, grade)
                VALUES (?, ?, ?, ?, ?)
            """, (student_name, test_type, score, percentage, grade))
            conn.commit()
            
            return jsonify({'success': True, 'message': 'Test result saved successfully'})
            
        except Exception as e:
            print("Error saving test result:", e)
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        print("Error in save_test_result:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize database
    if create_tables():
        clear_data()
        create_students()
        create_exams()
        populate_scores()
        print("Database initialized successfully")
    else:
        print("Failed to initialize database")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
