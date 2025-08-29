#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل شامل لنظام مقارنة الاختبارات التعليمية
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def _make_hyperlink(url: str, text: str | None = None) -> str:
    """Return an OSC 8 clickable hyperlink escape sequence.

    Falls back gracefully in terminals that don't support it (they'll just see the raw URL text).
    """
    if not text:
        text = url
    # OSC 8: ESC ] 8 ; ; url ST text ESC ] 8 ; ; ST
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

def print_banner():
    """طباعة شعار النظام"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🎓 نظام مقارنة الاختبارات التعليمية 🎓              ║
    ║                                                              ║
    ║        تم التطوير بواسطة فريق التطوير المتخصص                ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """التحقق من وجود المكتبات المطلوبة"""
    print("🔍 التحقق من المكتبات المطلوبة...")
    
    required_packages = ['flask', 'sqlite3']
    missing_packages = []
    
    try:
        import flask
        print("✅ Flask متوفر")
    except ImportError:
        missing_packages.append('flask')
        print("❌ Flask غير متوفر")
    
    try:
        import sqlite3
        print("✅ SQLite3 متوفر")
    except ImportError:
        missing_packages.append('sqlite3')
        print("❌ SQLite3 غير متوفر")
    
    if missing_packages:
        print(f"\n⚠️  المكتبات المفقودة: {', '.join(missing_packages)}")
        print("يرجى تثبيت المكتبات المفقودة باستخدام:")
        print("pip install flask")
        return False
    
    print("✅ جميع المكتبات متوفرة")
    return True

def setup_database():
    """إعداد قاعدة البيانات"""
    print("\n🗄️  إعداد قاعدة البيانات...")
    
    try:
        # تشغيل سكريبت ملء البيانات
        result = subprocess.run([sys.executable, 'populate_comparison_data.py'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ تم إعداد قاعدة البيانات بنجاح")
            return True
        else:
            print(f"❌ خطأ في إعداد قاعدة البيانات: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في إعداد قاعدة البيانات: {e}")
        return False

def start_server():
    """تشغيل الخادم"""
    print("\n🚀 تشغيل الخادم...")
    
    try:
        # تشغيل التطبيق في الخلفية
        process = subprocess.Popen([sys.executable, 'app.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 cwd=os.getcwd())
        
        # انتظار قليل للتأكد من تشغيل الخادم
        time.sleep(3)
        
        # التحقق من أن الخادم يعمل
        if process.poll() is None:
            print("✅ تم تشغيل الخادم بنجاح")
            base_url = "http://127.0.0.1:5000"
            print(f"🌐 الخادم يعمل على: {base_url}  →  " + _make_hyperlink(base_url))
            return process
        else:
            print("❌ فشل في تشغيل الخادم")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        return None

def open_browser():
    """فتح المتصفح"""
    print("\n🌐 فتح المتصفح...")
    
    urls = [
        "http://127.0.0.1:5000",
        "http://127.0.0.1:5000/dashboard",
        "http://127.0.0.1:5000/comparison"
    ]
    
    try:
        # فتح الصفحة الرئيسية
        webbrowser.open(urls[0])
        print("✅ تم فتح المتصفح")
        print(f"📋 الروابط المتاحة:")
        print(f"   🏠 الصفحة الرئيسية: {urls[0]}  →  " + _make_hyperlink(urls[0]))
        print(f"   📊 لوحة التحكم: {urls[1]}  →  " + _make_hyperlink(urls[1]))
        print(f"   📈 صفحة المقارنة: {urls[2]}  →  " + _make_hyperlink(urls[2]))
        
    except Exception as e:
        print(f"❌ خطأ في فتح المتصفح: {e}")
        print("يرجى فتح المتصفح يدوياً والذهاب إلى:")
        print("http://127.0.0.1:5000")

def show_usage_instructions():
    """عرض تعليمات الاستخدام"""
    instructions = """
    
    📋 تعليمات الاستخدام:
    
    1. 🏠 الصفحة الرئيسية: http://127.0.0.1:5000
       - صفحة الترحيب بالنظام
    
    2. 📊 لوحة التحكم: http://127.0.0.1:5000/dashboard
       - عرض الإحصائيات العامة
       - روابط للاختبارات المختلفة
       - رابط صفحة المقارنة
    
    3. 📈 صفحة المقارنة: http://127.0.0.1:5000/comparison
       - مقارنة بين المجموعتين (قبل التعلم وبعد التعلم)
       - عرض المتوسطات والإحصائيات
       - رسوم بيانية تفاعلية
    
    4. 🧪 الاختبارات المتاحة:
       - test1, test2, test3, test4 (قبل التعلم)
       - test1(2), testtashely, mlahza (بعد التعلم)
    
    ⚠️  ملاحظات مهمة:
    - تأكد من أن المنفذ 5000 متاح
    - لا تغلق نافذة الطرفية أثناء تشغيل النظام
    - للخروج من النظام، اضغط Ctrl+C
    
    """
    print(instructions)

def main():
    """الدالة الرئيسية"""
    print_banner()
    
    # التحقق من المكتبات
    if not check_dependencies():
        print("\n❌ فشل في التحقق من المكتبات. يرجى تثبيت المكتبات المفقودة.")
        return
    
    # إعداد قاعدة البيانات
    if not setup_database():
        print("\n❌ فشل في إعداد قاعدة البيانات.")
        return
    
    # تشغيل الخادم
    server_process = start_server()
    if not server_process:
        print("\n❌ فشل في تشغيل الخادم.")
        return
    
    # فتح المتصفح
    open_browser()
    
    # عرض تعليمات الاستخدام
    show_usage_instructions()
    
    print("\n🎉 تم تشغيل النظام بنجاح!")
    print("💡 للخروج من النظام، اضغط Ctrl+C")
    
    try:
        # انتظار حتى يتم إيقاف الخادم
        server_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 إيقاف النظام...")
        server_process.terminate()
        print("✅ تم إيقاف النظام بنجاح")

if __name__ == "__main__":
    main()
