@echo off
chcp 65001 >nul
title نظام مقارنة الاختبارات التعليمية

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        🎓 نظام مقارنة الاختبارات التعليمية 🎓              ║
echo ║                                                              ║
echo ║        تم التطوير بواسطة فريق التطوير المتخصص                ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت أو غير موجود في PATH
    echo يرجى تثبيت Python من https://python.org
    pause
    exit /b 1
)
echo ✅ Python متوفر

echo.
echo 🗄️ إعداد قاعدة البيانات...
python populate_comparison_data.py
if errorlevel 1 (
    echo ❌ خطأ في إعداد قاعدة البيانات
    pause
    exit /b 1
)
echo ✅ تم إعداد قاعدة البيانات بنجاح

echo.
echo 🚀 تشغيل الخادم...
echo 🌐 الخادم سيعمل على: http://127.0.0.1:5000
echo.
echo 📋 الروابط المتاحة:
echo    🏠 الصفحة الرئيسية: http://127.0.0.1:5000
echo    📊 لوحة التحكم: http://127.0.0.1:5000/dashboard
echo    📈 صفحة المقارنة: http://127.0.0.1:5000/comparison
echo.
echo 💡 للخروج من النظام، اضغط Ctrl+C
echo.

python app.py

echo.
echo 🛑 تم إيقاف النظام
pause


