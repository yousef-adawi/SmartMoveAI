import streamlit as st
from openai import OpenAI
from typing import List, Dict
import os

# --- إعداد الصفحة ---
st.set_page_config(
    page_title="SmartMoveAI — Pricing",
    page_icon="💎",
    layout="wide"
)

# --- تصميم مخصص ---
st.markdown("""
<style>
    .pricing-header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 40px;
    }
    .pricing-card {
        background: white;
        padding: 40px 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        margin: 20px 0;
        border: 2px solid #e0e0e0;
    }
    .pricing-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.3);
    }
    .pricing-card.featured {
        border: 3px solid #667eea;
        transform: scale(1.05);
    }
    .price {
        font-size: 3.5em;
        font-weight: 900;
        color: #667eea;
        margin: 20px 0;
    }
    .price-period {
        font-size: 0.3em;
        color: #666;
    }
    .feature-list {
        text-align: right;
        margin: 30px 0;
        padding: 0;
        list-style: none;
    }
    .feature-list li {
        padding: 12px 0;
        border-bottom: 1px solid #f0f0f0;
        font-size: 1.1em;
    }
    .feature-list li:before {
        content: "✓ ";
        color: #4caf50;
        font-weight: bold;
        margin-left: 10px;
    }
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 18px 40px;
        font-size: 1.2em;
        font-weight: 700;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        transition: transform 0.3s;
    }
    .cta-button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class='pricing-header'>
    <h1 style='font-size: 3em; margin-bottom: 20px;'>💎 اختر الخطة المناسبة لك</h1>
    <p style='font-size: 1.3em; opacity: 0.95;'>
        ابدأ مجاناً، أو احصل على ميزات غير محدودة مع Premium
    </p>
</div>
""", unsafe_allow_html=True)

# --- Pricing Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='pricing-card'>
        <h2 style='color: #667eea; margin-bottom: 20px;'>🆓 Free</h2>
        <div class='price'>€0<span class='price-period'>/شهر</span></div>
        <p style='color: #666; font-size: 1.1em;'>للتجربة والاستكشاف</p>
        
        <ul class='feature-list'>
            <li>10 أسئلة شهرياً</li>
            <li>دول محدودة (5 دول)</li>
            <li>ردود أساسية</li>
            <li>دعم عبر البريد</li>
            <li>❌ بدون تصدير PDF</li>
            <li>❌ بدون حفظ المحادثات</li>
        </ul>
        
        <a href='https://smartmoveai.streamlit.app' class='cta-button'>ابدأ مجاناً</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='pricing-card featured'>
        <div style='background: #667eea; color: white; padding: 10px; border-radius: 10px; margin-bottom: 20px;'>
            ⭐ الأكثر شعبية
        </div>
        <h2 style='color: #667eea; margin-bottom: 20px;'>💎 Premium</h2>
        <div class='price'>€19.99<span class='price-period'>/شهر</span></div>
        <p style='color: #666; font-size: 1.1em;'>للأفراد الجادين</p>
        
        <ul class='feature-list'>
            <li><b>أسئلة غير محدودة ✨</b></li>
            <li><b>كل الدول (20+ دولة) 🌍</b></li>
            <li><b>ردود مفصلة ودقيقة</b></li>
            <li><b>تصدير PDF 📄</b></li>
            <li><b>حفظ المحادثات</b></li>
            <li><b>دعم أولوية 24/7</b></li>
            <li><b>تحديثات أسبوعية</b></li>
        </ul>
        
        <a href='#subscribe-premium' class='cta-button'>اشترك الآن</a>
        <p style='margin-top: 15px; color: #666; font-size: 0.9em;'>🎉 خصم 20% للسنة الأولى!</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='pricing-card'>
        <h2 style='color: #667eea; margin-bottom: 20px;'>🏢 Business</h2>
        <div class='price'>€99<span class='price-period'>/شهر</span></div>
        <p style='color: #666; font-size: 1.1em;'>للشركات والمؤسسات</p>
        
        <ul class='feature-list'>
            <li><b>كل ميزات Premium</b></li>
            <li><b>10 مستخدمين</b></li>
            <li><b>API access</b></li>
            <li><b>تقارير شهرية</b></li>
            <li><b>تدريب الفريق</b></li>
            <li><b>دعم مخصص 24/7</b></li>
            <li><b>SLA مضمون</b></li>
        </ul>
        
        <a href='mailto:yousef@smartmoveai.com?subject=Business Plan Inquiry' class='cta-button'>تواصل معنا</a>
    </div>
    """, unsafe_allow_html=True)

# --- Feature Comparison ---
st.markdown("---")
st.markdown("## 📊 مقارنة الميزات التفصيلية")

comparison_data = {
    "الميزة": [
        "عدد الأسئلة الشهرية",
        "الدول المدعومة",
        "تصدير PDF",
        "حفظ المحادثات",
        "دعم أولوية",
        "تحديثات المحتوى",
        "API Access",
        "تقارير وإحصائيات",
        "تدريب الفريق",
        "SLA مضمون"
    ],
    "Free": [
        "10",
        "5 دول",
        "❌",
        "❌",
        "❌",
        "شهرياً",
        "❌",
        "❌",
        "❌",
        "❌"
    ],
    "Premium": [
        "غير محدود ✨",
        "20+ دولة 🌍",
        "✅",
        "✅",
        "✅",
        "أسبوعياً",
        "❌",
        "✅",
        "❌",
        "❌"
    ],
    "Business": [
        "غير محدود ✨",
        "كل الدول 🌍",
        "✅",
        "✅",
        "✅ VIP",
        "يومياً",
        "✅",
        "✅",
        "✅",
        "✅ 99.9%"
    ]
}

import pandas as pd
df = pd.DataFrame(comparison_data)
st.dataframe(df, use_container_width=True, hide_index=True)

# --- FAQ ---
st.markdown("---")
st.markdown("## ❓ الأسئلة الشائعة")

with st.expander("💳 كيف يتم الدفع؟"):
    st.markdown("""
    نستخدم **Stripe** - منصة الدفع الآمنة عالمياً:
    - ✅ جميع بطاقات الائتمان
    - ✅ دفع آمن ومشفر
    - ✅ إلغاء في أي وقت
    - ✅ استرداد كامل خلال 14 يوم
    """)

with st.expander("🔄 هل يمكنني تغيير الخطة لاحقاً؟"):
    st.markdown("""
    **بالتأكيد!** يمكنك:
    - ⬆️ الترقية من Free إلى Premium في أي وقت
    - ⬇️ التخفيض من Premium إلى Free
    - 🔄 التبديل إلى Business
    - الفرق في السعر يُحسب تلقائياً
    """)

with st.expander("💰 هل توجد رسوم خفية؟"):
    st.markdown("""
    **لا إطلاقاً!** السعر المعروض هو السعر النهائي:
    - ✅ شامل جميع الميزات
    - ✅ بدون رسوم إضافية
    - ✅ بدون تكاليف خفية
    - ⚠️ قد تُضاف ضريبة VAT حسب بلدك
    """)

with st.expander("🎁 هل توجد فترة تجريبية؟"):
    st.markdown("""
    **نعم!**
    - 🆓 **Free Plan** - مجاني للأبد (10 أسئلة/شهر)
    - 🎁 **Premium** - خصم 20% أول سنة
    - 💎 استرداد كامل خلال 14 يوم إذا لم تعجبك الخدمة
    """)

with st.expander("📧 كيف أتواصل للدعم؟"):
    st.markdown("""
    **متاحون دائماً!**
    - 📧 Email: yousef@smartmoveai.com
    - 💬 Chat: مباشرة من التطبيق (Premium)
    - ⏰ وقت الرد: 24 ساعة (Free) | 2 ساعات (Premium) | فوري (Business)
    """)

# --- Subscription Form (Premium) ---
st.markdown("---")
st.markdown("<div id='subscribe-premium'></div>", unsafe_allow_html=True)
st.markdown("## 💎 اشترك في Premium الآن")

with st.form("premium_subscription"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("الاسم الكامل *", placeholder="يوسف عدوي")
        email = st.text_input("البريد الإلكتروني *", placeholder="yousef@example.com")
    
    with col2:
        country = st.selectbox("البلد *", [
            "Netherlands", "Germany", "Belgium", "Sweden", "Denmark",
            "Canada", "Australia", "USA", "UK", "France", "UAE", "Saudi Arabia", "Other"
        ])
        plan_duration = st.radio("مدة الاشتراك", ["شهري - €19.99/شهر", "سنوي - €191.90/سنة (وفّر 20%!)"])
    
    st.markdown("---")
    
    agree_terms = st.checkbox("أوافق على شروط الاستخدام وسياسة الخصوصية *")
    agree_marketing = st.checkbox("أوافق على تلقي رسائل تسويقية (اختياري)")
    
    submit_button = st.form_submit_button("💳 المتابعة للدفع", use_container_width=True, type="primary")
    
    if submit_button:
        if not name or not email:
            st.error("⚠️ الرجاء ملء جميع الحقول المطلوبة")
        elif not agree_terms:
            st.error("⚠️ يجب الموافقة على الشروط والأحكام")
        else:
            # هنا سيتم التكامل مع Stripe
            st.success(f"""
            ✅ تم استلام طلبك يا {name}!
            
            📧 سنرسل لك رابط الدفع الآمن عبر Stripe إلى: {email}
            
            💎 الخطة: {plan_duration}
            
            ⏰ يرجى التحقق من بريدك الإلكتروني خلال 5 دقائق.
            """)
            
            st.info("""
            🔒 **الدفع آمن 100%**
            - معالج عبر Stripe (منصة عالمية موثوقة)
            - بياناتك محمية ومشفرة
            - لا نحفظ معلومات بطاقتك
            """)

# --- Testimonials ---
st.markdown("---")
st.markdown("## 💬 ماذا يقول عملاؤنا؟")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 25px; border-radius: 15px; border-right: 5px solid #667eea;'>
        <p style='font-size: 1.1em; color: #333; line-height: 1.8;'>
            "SmartMoveAI وفّر علي أسابيع من البحث! الإجابات دقيقة ومفصلة جداً."
        </p>
        <p style='margin-top: 15px; font-weight: 600; color: #667eea;'>
            - أحمد م., انتقل إلى هولندا
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 25px; border-radius: 15px; border-right: 5px solid #667eea;'>
        <p style='font-size: 1.1em; color: #333; line-height: 1.8;'>
            "أفضل استثمار! Premium يستحق كل سنت. حصلت على التأشيرة من أول محاولة!"
        </p>
        <p style='margin-top: 15px; font-weight: 600; color: #667eea;'>
            - سارة ح., انتقلت إلى كندا
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 25px; border-radius: 15px; border-right: 5px solid #667eea;'>
        <p style='font-size: 1.1em; color: #333; line-height: 1.8;'>
            "نستخدم Business Plan لفريقنا. التكامل مع API رائع والدعم ممتاز!"
        </p>
        <p style='margin-top: 15px; font-weight: 600; color: #667eea;'>
            - شركة Global Talent
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 40px 20px;'>
    <p style='font-size: 1.2em; margin-bottom: 20px;'>
        💻 تطوير: <b>Yousef Adawi</b><br>
        📧 للاستفسارات: <a href='mailto:yousef@smartmoveai.com' style='color: #667eea;'>yousef@smartmoveai.com</a>
    </p>
    <p style='margin-top: 20px; font-size: 0.9em;'>
        🔗 <a href='https://smartmoveai.streamlit.app' style='color: #667eea;'>التطبيق</a> | 
        <a href='https://github.com/yousef-adawi/SmartMoveAI' style='color: #667eea;'>GitHub</a> | 
        <a href='#' style='color: #667eea;'>Privacy Policy</a> | 
        <a href='#' style='color: #667eea;'>Terms of Service</a>
    </p>
    <p style='margin-top: 20px; opacity: 0.7;'>
        © 2025 SmartMoveAI. جميع الحقوق محفوظة.
    </p>
</div>
""", unsafe_allow_html=True)
