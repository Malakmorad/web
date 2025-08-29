// ملف JavaScript لصفحة المقارنة
class ComparisonManager {
    constructor() {
        this.beforeTests = ['test1', 'test2', 'test3', 'test4'];
        this.afterTests = ['test1(2)', 'testtashely', 'mlahza'];
        this.updateInterval = 5000; // تحديث كل 5 ثوانٍ
        this.init();
    }

    async init() {
        await this.loadComparisonData();
        this.startAutoUpdate();
        this.setupEventListeners();
    }

    async loadComparisonData() {
        try {
            const response = await fetch('/api/comparison-data');
            const data = await response.json();
            
            if (data.error) {
                this.showError('خطأ في تحميل البيانات: ' + data.error);
                return;
            }
            
            this.updateUI(data);
            this.updateCharts(data);
            this.showComparisonResult(data);
            
        } catch (error) {
            console.error('Error loading comparison data:', error);
            this.showError('خطأ في الاتصال بالخادم');
        }
    }

    updateUI(data) {
        // تحديث بيانات المجموعة الأولى
        data.before_tests.forEach(test => {
            const elementId = test.test.replace('(', '').replace(')', '') + '-score';
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = test.average + '%';
                element.style.color = this.getScoreColor(test.average);
            }
        });
        
        // تحديث بيانات المجموعة الثانية
        data.after_tests.forEach(test => {
            const elementId = test.test === 'test1(2)' ? 'test1-2-score' : test.test + '-score';
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = test.average + '%';
                element.style.color = this.getScoreColor(test.average);
            }
        });
        
        // تحديث المتوسطات
        document.getElementById('avg-before').textContent = data.before_average;
        document.getElementById('avg-after').textContent = data.after_average;
        
        // تحديث الإحصائيات
        document.getElementById('total-tests').textContent = data.total_tests_taken;
        document.getElementById('total-students').textContent = data.total_students;
        document.getElementById('improvement-rate').textContent = data.improvement_rate + '%';
        document.getElementById('best-test').textContent = data.best_test;
        
        // تحديث ألوان المتوسطات
        document.getElementById('avg-before').style.color = this.getScoreColor(data.before_average);
        document.getElementById('avg-after').style.color = this.getScoreColor(data.after_average);
    }

    updateCharts(data) {
        const beforeProgress = document.getElementById('before-progress');
        const afterProgress = document.getElementById('after-progress');
        const beforePercentage = document.getElementById('before-percentage');
        const afterPercentage = document.getElementById('after-percentage');
        
        // تحديث شريط التقدم مع تأثير متحرك
        this.animateProgress(beforeProgress, data.before_average);
        this.animateProgress(afterProgress, data.after_average);
        
        beforePercentage.textContent = data.before_average + '%';
        afterPercentage.textContent = data.after_average + '%';
    }

    animateProgress(element, percentage) {
        element.style.transition = 'width 1s ease-in-out';
        element.style.width = percentage + '%';
    }

    showComparisonResult(data) {
        if (data.before_average > 0 && data.after_average > 0) {
            const comparisonResult = document.getElementById('comparison-result');
            const comparisonText = document.getElementById('comparison-text');
            
            let resultHTML = '';
            
            if (data.after_average > data.before_average) {
                const improvement = (data.after_average - data.before_average).toFixed(1);
                resultHTML = `
                    <div class="improvement">
                        🎉 تحسن الأداء بنسبة ${improvement}%
                    </div>
                    <p>أداء المجموعة الثانية (بعد التعلم) أفضل من المجموعة الأولى</p>
                    <div class="improvement-details">
                        <small>معدل التحسن: ${data.improvement_rate}%</small>
                    </div>
                `;
            } else if (data.after_average < data.before_average) {
                const decline = (data.before_average - data.after_average).toFixed(1);
                resultHTML = `
                    <div class="decline">
                        ⚠️ انخفاض في الأداء بنسبة ${decline}%
                    </div>
                    <p>أداء المجموعة الأولى (قبل التعلم) أفضل من المجموعة الثانية</p>
                    <div class="decline-details">
                        <small>معدل الانخفاض: ${Math.abs(data.improvement_rate)}%</small>
                    </div>
                `;
            } else {
                resultHTML = `
                    <div style="color: var(--warning-color); font-weight: bold;">
                        ⚖️ الأداء متساوي بين المجموعتين
                    </div>
                    <p>لا يوجد فرق معنوي في الأداء بين المجموعتين</p>
                `;
            }
            
            comparisonText.innerHTML = resultHTML;
            comparisonResult.style.display = 'block';
            
            // إضافة تأثير ظهور تدريجي
            comparisonResult.style.opacity = '0';
            comparisonResult.style.transform = 'translateY(20px)';
            comparisonResult.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                comparisonResult.style.opacity = '1';
                comparisonResult.style.transform = 'translateY(0)';
            }, 100);
        }
    }

    getScoreColor(score) {
        if (score >= 90) return '#27ae60'; // أخضر داكن
        if (score >= 80) return '#2ecc71'; // أخضر
        if (score >= 70) return '#f39c12'; // برتقالي
        if (score >= 60) return '#e67e22'; // برتقالي داكن
        return '#e74c3c'; // أحمر
    }

    showError(message) {
        // إنشاء عنصر تنبيه للخطأ
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-alert';
        errorDiv.innerHTML = `
            <div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px; margin: 20px 0; border: 1px solid #f5c6cb;">
                <strong>خطأ:</strong> ${message}
            </div>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(errorDiv, container.firstChild);
        
        // إزالة التنبيه بعد 5 ثوانٍ
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    startAutoUpdate() {
        setInterval(() => {
            this.loadComparisonData();
        }, this.updateInterval);
    }

    setupEventListeners() {
        // إضافة مستمع لزر التحديث اليدوي
        const refreshButton = document.createElement('button');
        refreshButton.textContent = '🔄 تحديث البيانات';
        refreshButton.className = 'refresh-btn';
        refreshButton.style.cssText = `
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            margin: 10px;
            font-size: 14px;
        `;
        
        refreshButton.addEventListener('click', () => {
            this.loadComparisonData();
            refreshButton.textContent = '⏳ جاري التحديث...';
            setTimeout(() => {
                refreshButton.textContent = '🔄 تحديث البيانات';
            }, 1000);
        });
        
        // إضافة الزر إلى الصفحة
        const header = document.querySelector('h1');
        header.parentNode.insertBefore(refreshButton, header.nextSibling);
        
        // إضافة مستمع لتصغير/تكبير الرسوم البيانية
        const chartContainer = document.querySelector('.chart-container');
        if (chartContainer) {
            chartContainer.addEventListener('click', () => {
                chartContainer.classList.toggle('expanded');
            });
        }
    }

    // دالة لحفظ نتيجة اختبار جديدة
    async saveTestResult(testData) {
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
                console.log('Test result saved successfully');
                // تحديث البيانات بعد الحفظ
                setTimeout(() => this.loadComparisonData(), 1000);
            } else {
                console.error('Error saving test result:', result.error);
            }
            
        } catch (error) {
            console.error('Error saving test result:', error);
        }
    }
}

// تهيئة مدير المقارنة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    new ComparisonManager();
});

// إضافة CSS إضافي للتحسينات
const additionalCSS = `
    .refresh-btn:hover {
        background: #2980b9 !important;
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    .chart-container.expanded {
        transform: scale(1.05);
        transition: transform 0.3s ease;
    }
    
    .improvement-details, .decline-details {
        margin-top: 10px;
        font-size: 0.9em;
        opacity: 0.8;
    }
    
    .test-item {
        transition: all 0.3s ease;
    }
    
    .test-item:hover {
        transform: translateX(-5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    .stat-card {
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
`;

// إضافة CSS إلى الصفحة
const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style);


