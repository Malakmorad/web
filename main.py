# main.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import json

# تهيئة تطبيق Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # مفتاح سري للتطبيق

# تكوين قاعدة البيانات
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'digital_research.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# تهيئة قاعدة البيانات
db = SQLAlchemy(app)

# نموذج المستخدم
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# نموذج التقدم في التعلم
class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

# إنشاء الجداول في قاعدة البيانات
with app.app_context():
    db.create_all()

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# صفحة الدورة التعليمية
@app.route('/course')
def course():
    return render_template('course.html')

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='اسم المستخدم أو كلمة المرور غير صحيحة')
    
    return render_template('login.html')

# صفحة التسجيل
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return render_template('register.html', error='كلمات المرور غير متطابقة')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='اسم المستخدم موجود مسبقاً')
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='البريد الإلكتروني موجود مسبقاً')
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        
        return redirect(url_for('index'))
    
    return render_template('register.html')

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# واجهة برمجة التطبيقات (API) لحفظ التقدم
@app.route('/api/progress', methods=['POST'])
def save_progress():
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401
    
    data = request.get_json()
    module = data.get('module')
    completed = data.get('completed', False)
    score = data.get('score', 0)
    
    # التحقق من وجود تقدم سابق
    progress = Progress.query.filter_by(
        user_id=session['user_id'], 
        module=module
    ).first()
    
    if progress:
        progress.completed = completed
        progress.score = score
        progress.completed_at = datetime.utcnow()
    else:
        progress = Progress(
            user_id=session['user_id'],
            module=module,
            completed=completed,
            score=score
        )
        db.session.add(progress)
    
    db.session.commit()
    
    return jsonify({'message': 'تم حفظ التقدم بنجاح'})

# واجهة برمجة التطبيقات (API) لجلب التقدم
@app.route('/api/progress')
def get_progress():
    if 'user_id' not in session:
        return jsonify({'error': 'يجب تسجيل الدخول أولاً'}), 401
    
    progress_list = Progress.query.filter_by(user_id=session['user_id']).all()
    
    progress_data = []
    for progress in progress_list:
        progress_data.append({
            'module': progress.module,
            'completed': progress.completed,
            'score': progress.score,
            'completed_at': progress.completed_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(progress_data)

# صفحة الملف الشخصي
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    progress_list = Progress.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('profile.html', user=user, progress_list=progress_list)

# صفحة حول المنصة
@app.route('/about')
def about():
    return render_template('about.html')

# صفحة الاتصال
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # هنا يمكنك إضافة رمز لإرسال البريد الإلكتروني أو حفظ الرسالة في قاعدة البيانات
        print(f"رسالة جديدة من {name} ({email}): {message}")
        
        return render_template('contact.html', success=True)
    
    return render_template('contact.html')

# معالج الأخطاء 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)