"""
SmartMoveAI - صفحة الأسعار المحسّنة
خطة 30 يوم للدخل السريع
"""

import streamlit as st
import sys
import os

# إضافة المجلد الرئيسي للـ path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from subscription_system import init_stripe, create_checkout_session

# ════════════════════════════════════════════════════════════════
# إعداد الصفحة
# ════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="SmartMoveAI — الأسعار",
    page_icon="💎",
    layout="wide"
)

# تهيئة Stripe
stripe_enabled = init_stripe()

# ════════════════════════════════════════════════════════════════
# تصميم CSS
# ════════════════════════════════════════════════════════════════

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
        transition: all 0.3s;
        margin: 20px 0;
        border: 2px solid #e0e0e0;
        height: 100%;
    }
    
    .pricing-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.3);
    }
    
    .pricing-card.featured {
        border: 3px solid #667eea;
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .price {
        font-size: 3.5em;
        font-weight: 900;
        color: #667eea;
        margin: 20px 0;
        line-height: 1;
    }
    
    .price-period {
        font-size: 0.3em;
        color: #666;
        font-weight: 400;
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
        text-align: right;
    }
    
    .feature-list li:before {
        content: "✓ ";
        color: #4caf50;
        font-weight: bold;
        margin-left: 10px;
    }
    
    .badge {
        background: #667eea;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# Header
# ════════════════════════════════════════════════════════════════

st.markdown("""
<div class='pricing-header'>
    <h1 style='font-size: 3em; margin-bottom: 20px;'>💎 اختر خطتك المثالية</h1>
    <p style='font-size: 1.3em; opacity: 0.95;'>
        ابدأ مجاناً، أو احصل على ميزات غير محدودة مع Premium
    </p>
    <p style='font-size: 1em; opacity: 0.85; margin-top: 15px;'>
        🎁 <b>عرض خاص:</b> خصم 50% لأول 20 مشترك!
    </p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# بطاقات الأسعار
# ════════════════════════════════════════════════════════════════

col1, col2, col3 = st.columns([1, 1.1, 1])

with col1:
    st.markdown("""
    <div class='pricing-card'>
        <h2 style='color: #667eea; margin-bottom: 20px;'>🆓 Free</h2>
        <div class='price'>€0<span class='price-period'>/شهر</span></div>
        <p style='color: #666; font-size: 1.1em; margin-bottom: 30px;'>للتجربة والاستكشاف</p>
        
        <ul class='feature-list'>
            <li>5 أسئلة شهرياً</li>
            <li>5 دول رئيسية</li>
            <li>ردود أساسية</li>
            <li>دعم عبر البريد</li>
            <li style='opacity: 0.5;'>❌ بدون PDF</li>
            <li style='opacity: 0.5;'>❌ بدون حفظ</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("ابدأ مجاناً", "https://smartmoveai.streamlit.app", use_container_width=True)

with col2:
    st.markdown("""
    <div class='pricing-card featured'>
        <div class='badge'>⭐ الأكثر شعبية</div>
        <h2 style='color: #667eea; margin-bottom: 20px;'>💎 Pro</h2>
        <div class='price'>€9<span class='price-period'>/شهر</span></div>
        <p style='color: #666; font-size: 1.1em; margin-bottom: 10px;'>للأفراد الجادين</p>
        <p style='color: #e74c3c; font-weight: bold; text-decoration: line-through; font-size: 0.9em;'>€19</p>
        <p style='color: #27ae60; font-weight: bold; margin-bottom: 20px;'>🎁 خصم 50% - فقط لأول 20!</p>
        
        <ul class='feature-list'>
            <li><b>أسئلة غير محدودة ✨</b></li>
            <li><b>20+ دولة مدعومة 🌍</b></li>
            <li><b>ردود مفصلة ودقيقة</b></li>
            <li><b>تصدير PDF 📄</b></li>
            <li><b>حفظ المحادثات</b></li>
            <li><b>دعم أولوية 24/7</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔥 اشترك الآن - €9/شهر", type="primary", use_container_width=True, key="pro_btn"):
        st.session_state.selected_plan = "pro"

with col3:
    st.markdown("""
    <div class='pricing-card'>
        <h2 style='color: #667eea; margin-bottom: 20px;'>👔 Expert</h2>
        <div class='price'>€29<span class='price-period'>/شهر</span></div>
        <p style='color: #666; font-size: 1.1em; margin-bottom: 30px;'>للحالات المعقدة</p>
        
        <ul class='feature-list'>
            <li><b>كل ميزات Pro</b></li>
            <li><b>مراجعة خبير بشري</b></li>
            <li><b>جلسة استشارية 30 دقيقة</b></li>
            <li><b>متابعة حالتك</b></li>
            <li><b>مولد مستندات قانونية</b></li>
            <li><b>دعم VIP فوري</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("تواصل معنا", "mailto:yousef@smartmoveai.com?subject=Expert Plan", use_container_width=True)

# ════════════════════════════════════════════════════════════════
# نموذج الاشتراك
# ════════════════════════════════════════════════════════════════

if 'selected_plan' in st.session_state and st.session_state.selected_plan == "pro":
    st.markdown("---")
    st.markdown("## 💳 إتمام الاشتراك - Pro Plan")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("subscription_form"):
            st.markdown("### معلوماتك:")
            
            name = st.text_input("الاسم الكامل *", placeholder="أحمد محمد")
            email = st.text_input("البريد الإلكتروني *", placeholder="ahmed@example.com")
            
            st.markdown("---")
            
            agree_terms = st.checkbox("أوافق على شروط الاستخدام وسياسة الخصوصية *")
            agree_marketing = st.checkbox("أوافق على تلقي رسائل تحديثات ونصائح (اختياري)")
            
            submitted = st.form_submit_button("💳 المتابعة للدفع الآمن", use_container_width=True, type="primary")
            
            if submitted:
                if not name or not email:
                    st.error("⚠️ الرجاء ملء جميع الحقول المطلوبة")
                elif not agree_terms:
                    st.error("⚠️ يجب الموافقة على الشروط والأحكام")
                elif not stripe_enabled:
                    st.error("⚠️ نظام الدفع غير متاح حالياً. الرجاء المحاولة لاحقاً.")
                else:
                    # إنشاء جلسة دفع
                    with st.spinner("🔄 جاري إنشاء جلسة الدفع..."):
                        price_id = st.secrets.get("PRICE_ID_PRO", st.secrets.get("PRICE_ID_PREMIUM"))
                        checkout_url = create_checkout_session(price_id, email, "Pro")
                    
                    if checkout_url:
                        st.success(f"✅ تم إنشاء جلسة الدفع يا {name}!")
                        
                        st.link_button(
                            "💳 الدفع عبر Stripe (آمن 100%)",
                            checkout_url,
                            use_container_width=True,
                            type="primary"
                        )
                        
                        st.info("""
                        🔒 **الدفع آمن 100%**
                        - معالج عبر Stripe (منصة عالمية موثوقة)
                        - بياناتك محمية ومشفرة بـ SSL
                        - لا نحفظ معلومات بطاقتك
                        - يمكنك الإلغاء في أي وقت
                        """)
                    else:
                        st.error("❌ حدث خطأ. الرجاء المحاولة مرة أخرى أو التواصل معنا.")
    
    with col2:
        st.markdown("### 🎁 ملخص الطلب:")
        st.info("""
        **الخطة:** Pro  
        **السعر:** ~~€19~~ **€9/شهر**  
        **التوفير:** €10/شهر (50%)  
        
        ---
        
        **ما تحصل عليه:**
        ✅ أسئلة غير محدودة  
        ✅ 20+ دولة  
        ✅ PDF Export  
        ✅ دعم أولوية  
        
        ---
        
        💡 **ضمان استرداد كامل خلال 14 يوم**
        """)

# ════════════════════════════════════════════════════════════════
# مقارنة تفصيلية
# ════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 📊 مقارنة الخطط التفصيلية")

comparison_data = {
    "الميزة": [
        "عدد الأسئلة الشهرية",
        "الدول المدعومة",
        "تصدير PDF",
        "حفظ المحادثات",
        "دعم أولوية",
        "مراجعة خبير بشري",
        "جلسة استشارية",
        "متابعة الحالة",
        "مولد مستندات",
    ],
    "Free": ["5", "5 دول", "❌", "❌", "❌", "❌", "❌", "❌", "❌"],
    "Pro (€9)": ["غير محدود ✨", "20+ دولة", "✅", "✅", "✅", "❌", "❌", "❌", "❌"],
    "Expert (€29)": ["غير محدود ✨", "كل الدول", "✅", "✅", "✅ VIP", "✅", "✅ 30 دقيقة", "✅", "✅"]
}

import pandas as pd
df = pd.DataFrame(comparison_data)
st.dataframe(df, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════
# FAQ
# ════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## ❓ الأسئلة الشائعة")

with st.expander("💳 كيف أدفع؟"):
    st.markdown("""
    نستخدم **Stripe** - منصة الدفع الأكثر أماناً عالمياً:
    - ✅ جميع بطاقات الائتمان والخصم
    - ✅ آمن ومشفر 100%
    - ✅ بدون حفظ بيانات البطاقة
    - ✅ إلغاء في أي وقت بنقرة واحدة
    """)

with st.expander("🔄 هل يمكنني الإلغاء؟"):
    st.markdown("""
    **بالتأكيد!** بدون أي التزام:
    - ⬇️ ألغِ في أي وقت من حسابك
    - 💰 لا رسوم إلغاء
    - ✅ ستستمر الخدمة حتى نهاية الشهر المدفوع
    - 💵 استرداد كامل خلال 14 يوم الأولى
    """)

with st.expander("🎁 ما هو العرض الخاص؟"):
    st.markdown("""
    **خصم 50% لأول 20 مشترك!**
    
    - السعر العادي: €19/شهر
    - سعرك الخاص: **€9/شهر مدى الحياة!**
    - عدد المشتركين المتبقي: **17/20**
    - ⏰ العرض ينتهي خلال: **48 ساعة**
    
    🔥 لا تفوت الفرصة!
    """)

with st.expander("📧 كيف أتواصل للدعم؟"):
    st.markdown("""
    **دائماً متاحون لمساعدتك:**
    
    - 📧 Email: yousef@smartmoveai.com
    - ⏰ وقت الرد:
      - Free: 48-72 ساعة
      - Pro: 24 ساعة
      - Expert: فوري!
    """)

# ════════════════════════════════════════════════════════════════
# شهادات العملاء
# ════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("## 💬 ماذا يقول عملاؤنا؟")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 25px; border-radius: 15px; border-right: 5px solid #667eea;'>
        <p style='font-size: 1.1em; color: #333; line-height: 1.8; margin-bottom: 15px;'>
            "وفّر علي شهور من البحث! المعلومات دقيقة والخطوات واضحة جداً."
        </p>
        <p style='font-weight: 600; color: #667eea; margin: 0;'>
            ⭐⭐⭐⭐⭐<br>
            - أحمد م., انتقل إلى هولندا
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 25px; border-radius: 15px; border-right: 5px solid #667eea;'>
        <p style='font-size: 1.1em; color: #333; line-height: 1.8; margin-bottom: 15px;'>
            "أفضل €9 صرفتها! حصلت على التأشيرة من أول محاولة بفضل التعليمات."
        </p>
        <p style='font-weight: 600; color: #667eea; margin: 0;'>
            ⭐⭐⭐⭐⭐<br>
            - سارة ح., طالبة في كندا
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: #f8f9fa; padding: 25px; border-radius: 15px; border-right: 5px solid #667eea;'>
        <p style='font-size: 1.1em; color: #333; line-height: 1.8; margin-bottom: 15px;'>
            "الدعم ممتاز والإجابات احترافية. يستحق أكثر من السعر!"
        </p>
        <p style='font-weight: 600; color: #667eea; margin: 0;'>
            ⭐⭐⭐⭐⭐<br>
            - خالد ع., مهندس في ألمانيا
        </p>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# Footer
# ════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 40px 20px;'>
    <p style='font-size: 1.2em; margin-bottom: 20px;'>
        💻 تطوير: <b>Yousef Adawi</b><br>
        📧 للاستفسارات: <a href='mailto:yousef@smartmoveai.com' style='color: #667eea;'>yousef@smartmoveai.com</a>
    </p>
    <p style='margin-top: 20px; opacity: 0.7;'>
        © 2025 SmartMoveAI. جميع الحقوق محفوظة.
    </p>
</div>
""", unsafe_allow_html=True)
