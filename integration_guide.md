# دليل تكامل نظام المقارنة مع الاختبارات الموجودة

## نظرة عامة

هذا الدليل يوضح كيفية ربط الاختبارات الموجودة (test1, test2, test3, test4, test1(2), testtashely, mlahza) مع نظام المقارنة الجديد.

## الخطوات المطلوبة

### 1. تحديث صفحات الاختبارات الموجودة

#### أ. إضافة كود حفظ النتائج

أضف الكود التالي في نهاية كل صفحة اختبار (قبل إغلاق وسم `</body>`):

```javascript
// دالة لحفظ نتيجة الاختبار
async function saveTestResult(score, percentage, grade) {
    const testType = getCurrentTestType(); // دالة لتحديد نوع الاختبار الحالي
    const studentName = localStorage.getItem('student_name') || 'طالب مجهول';
    
    const testData = {
        student_name: studentName,
        test_type: testType,
        score: score,
        percentage: percentage,
        grade: grade
    };
    
    try {
        const response = await fetch('/api/save-test-result', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('تم حفظ النتيجة بنجاح');
            // يمكن إضافة رسالة تأكيد للمستخدم هنا
        } else {
            console.error('خطأ في حفظ النتيجة:', result.error);
        }
        
    } catch (error) {
        console.error('خطأ في الاتصال:', error);
    }
}

// دالة لتحديد نوع الاختبار الحالي
function getCurrentTestType() {
    const currentPage = window.location.pathname;
    
    if (currentPage.includes('test1') && !currentPage.includes('test1(2)')) {
        return 'test1';
    } else if (currentPage.includes('test1(2)')) {
        return 'test1(2)';
    } else if (currentPage.includes('test2')) {
        return 'test2';
    } else if (currentPage.includes('test3')) {
        return 'test3';
    } else if (currentPage.includes('test4')) {
        return 'test4';
    } else if (currentPage.includes('testtashely')) {
        return 'testtashely';
    } else if (currentPage.includes('mlahza')) {
        return 'mlahza';
    }
    
    return 'unknown';
}
```

#### ب. استدعاء دالة الحفظ عند انتهاء الاختبار

في كل صفحة اختبار، عند حساب النتيجة النهائية، أضف:

```javascript
// مثال: عند انتهاء الاختبار وحساب النتيجة
function finishTest() {
    const score = calculateFinalScore(); // دالة حساب النتيجة النهائية
    const percentage = (score / totalQuestions) * 100;
    const grade = getGrade(percentage); // دالة تحديد التقدير
    
    // حفظ النتيجة في قاعدة البيانات
    saveTestResult(score, percentage, grade);
    
    // عرض النتيجة للمستخدم
    showResult(score, percentage, grade);
}

// دالة تحديد التقدير
function getGrade(percentage) {
    if (percentage >= 90) return "ممتاز";
    if (percentage >= 80) return "جيد جداً";
    if (percentage >= 70) return "جيد";
    if (percentage >= 60) return "مقبول";
    return "ضعيف";
}
```

### 2. تحديث صفحات الاختبارات المحددة

#### صفحة test1.html
```javascript
// في نهاية الملف، قبل إغلاق وسم body
<script>
    // إضافة الكود المذكور أعلاه هنا
    
    // تحديث دالة انتهاء الاختبار الموجودة
    function submitTest() {
        // الكود الموجود حالياً...
        
        // إضافة حفظ النتيجة
        const finalScore = calculateScore();
        const percentage = (finalScore / totalQuestions) * 100;
        const grade = getGrade(percentage);
        
        saveTestResult(finalScore, percentage, grade);
    }
</script>
```

#### صفحة test2.html
```javascript
// نفس الإجراء مع تحديث دالة انتهاء الاختبار
```

#### صفحة test3.html
```javascript
// نفس الإجراء مع تحديث دالة انتهاء الاختبار
```

#### صفحة test4.html
```javascript
// نفس الإجراء مع تحديث دالة انتهاء الاختبار
```

#### صفحة test1(2).html
```javascript
// نفس الإجراء مع تحديث دالة انتهاء الاختبار
```

#### صفحة testtashely.html
```javascript
// نفس الإجراء مع تحديث دالة انتهاء الاختبار
```

#### صفحة mlahza.html
```javascript
// نفس الإجراء مع تحديث دالة انتهاء الاختبار
```

### 3. إضافة رابط للمقارنة في كل صفحة اختبار

أضف هذا الكود في كل صفحة اختبار لعرض رابط للمقارنة:

```html
<!-- إضافة في نهاية الصفحة، قبل إغلاق وسم body -->
<div style="text-align: center; margin: 20px 0;">
    <a href="/comparison" style="
        background: #3498db;
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 8px;
        display: inline-block;
        margin: 10px;
    ">📊 عرض مقارنة النتائج</a>
    <a href="/dashboard" style="
        background: #2ecc71;
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 8px;
        display: inline-block;
        margin: 10px;
    ">🏠 العودة للوحة التحكم</a>
</div>
```

## اختبار التكامل

### 1. تشغيل التطبيق
```bash
python app.py
```

### 2. اختبار الاختبارات
1. اذهب إلى أي اختبار (مثل test1)
2. أكمل الاختبار
3. تحقق من حفظ النتيجة في قاعدة البيانات
4. اذهب إلى صفحة المقارنة
5. تحقق من ظهور النتيجة في المقارنة

### 3. التحقق من قاعدة البيانات
```bash
# يمكنك استخدام أداة مثل DB Browser for SQLite لفحص قاعدة البيانات
# أو إضافة endpoint جديد لعرض البيانات
```

## استكشاف الأخطاء

### مشكلة: لا تظهر النتائج في المقارنة
**الحل:**
1. تحقق من أن دالة `saveTestResult` تعمل بشكل صحيح
2. تحقق من أن نوع الاختبار محدد بشكل صحيح
3. تحقق من قاعدة البيانات

### مشكلة: خطأ في الاتصال بالخادم
**الحل:**
1. تأكد من أن التطبيق يعمل على المنفذ الصحيح
2. تحقق من أن API endpoint متاح
3. تحقق من console المتصفح للأخطاء

### مشكلة: البيانات لا تتحدث تلقائياً
**الحل:**
1. تأكد من أن JavaScript يعمل بشكل صحيح
2. تحقق من أن interval التحديث يعمل
3. تحقق من network tab في developer tools

## ملاحظات مهمة

1. **أمان البيانات**: تأكد من التحقق من صحة البيانات قبل حفظها
2. **أداء النظام**: قد تحتاج لتحسين الاستعلامات إذا زاد عدد الطلاب
3. **النسخ الاحتياطي**: قم بعمل نسخة احتياطية من قاعدة البيانات بانتظام
4. **التوثيق**: وثق أي تغييرات تجريها على النظام

## الدعم

إذا واجهت أي مشاكل في التكامل، يرجى:
1. مراجعة console المتصفح للأخطاء
2. مراجعة logs الخادم
3. التحقق من قاعدة البيانات
4. التواصل مع فريق التطوير


