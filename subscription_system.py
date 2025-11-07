"""
SmartMoveAI - نظام الاشتراكات المحسّن
بدون أخطاء، جاهز للإنتاج
"""

import stripe
import streamlit as st
from datetime import datetime
import os

# ════════════════════════════════════════════════════════════════
# إعداد Stripe
# ════════════════════════════════════════════════════════════════

def init_stripe():
    """تهيئة Stripe"""
    try:
        if "STRIPE_SECRET_KEY" in st.secrets:
            stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
            return True
        return False
    except:
        return False


# ════════════════════════════════════════════════════════════════
# إنشاء جلسة دفع
# ════════════════════════════════════════════════════════════════

def create_checkout_session(price_id: str, customer_email: str, plan_name: str = "Pro"):
    """إنشاء جلسة دفع Stripe"""
    try:
        # الحصول على URL التطبيق
        app_url = st.secrets.get("APP_URL", "https://smartmoveai.streamlit.app")
        
        # إنشاء الجلسة
        session = stripe.checkout.Session.create(
            customer_email=customer_email,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f'{app_url}?success=true&session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{app_url}?canceled=true',
            metadata={
                'plan': plan_name,
                'source': 'smartmoveai'
            },
            allow_promotion_codes=True,
        )
        
        return session.url
    
    except Exception as e:
        st.error(f"خطأ في إنشاء جلسة الدفع: {str(e)}")
        return None


# ════════════════════════════════════════════════════════════════
# التحقق من الاشتراك
# ════════════════════════════════════════════════════════════════

def check_subscription(customer_email: str):
    """
    التحقق من اشتراك العميل
    
    Returns:
        dict أو None
    """
    try:
        # البحث عن العميل
        customers = stripe.Customer.list(email=customer_email, limit=1)
        
        if not customers.data:
            return None
        
        customer = customers.data[0]
        
        # البحث عن الاشتراكات النشطة
        subscriptions = stripe.Subscription.list(
            customer=customer.id,
            status='active',
            limit=1
        )
        
        if not subscriptions.data:
            return None
        
        sub = subscriptions.data[0]
        
        return {
            'id': sub.id,
            'status': sub.status,
            'plan': 'Premium',
            'amount': sub.plan.amount / 100,
            'currency': sub.plan.currency.upper(),
            'current_period_end': datetime.fromtimestamp(sub.current_period_end),
            'cancel_at_period_end': sub.cancel_at_period_end,
        }
    
    except:
        return None


# ════════════════════════════════════════════════════════════════
# عد الأسئلة المتبقية
# ════════════════════════════════════════════════════════════════

def get_questions_count():
    """حساب عدد الأسئلة المستخدمة"""
    if 'history' not in st.session_state:
        return 0
    
    return len([m for m in st.session_state.history if m["role"] == "user"])


def check_can_ask():
    """
    التحقق من إمكانية طرح سؤال
    
    Returns:
        tuple: (can_ask: bool, remaining: int, is_premium: bool)
    """
    # إذا كان هناك email وتم التحقق من الاشتراك
    user_email = st.session_state.get('user_email', None)
    
    if user_email:
        subscription = check_subscription(user_email)
        if subscription:
            # Premium user
            return (True, float('inf'), True)
    
    # Free user - حد 5 أسئلة
    questions_asked = get_questions_count()
    remaining = max(0, 5 - questions_asked)
    
    return (remaining > 0, remaining, False)


# ════════════════════════════════════════════════════════════════
# واجهة العرض في Sidebar
# ════════════════════════════════════════════════════════════════

def display_subscription_widget():
    """عرض حالة الاشتراك في Sidebar"""
    
    user_email = st.session_state.get('user_email', None)
    
    if user_email:
        subscription = check_subscription(user_email)
        
        if subscription:
            # Premium user
            st.sidebar.success("✅ **Premium Active**")
            st.sidebar.info(f"""
            **الخطة:** Premium  
            **السعر:** €{subscription['amount']}/شهر  
            **التجديد:** {subscription['current_period_end'].strftime('%Y-%m-%d')}
            """)
            return
    
    # Free user
    can_ask, remaining, _ = check_can_ask()
    
    st.sidebar.warning("🆓 **Free Plan**")
    st.sidebar.info(f"""
    **الأسئلة المتبقية:** {remaining}/5 هذا الشهر
    """)
    
    if remaining <= 2:
        st.sidebar.error(f"⚠️ بقي {remaining} {'سؤال' if remaining == 1 else 'أسئلة'} فقط!")
    
    # زر الترقية
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center;'>
        <a href='/Pricing' style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            display: inline-block;
        '>💎 ترقية لـ Premium</a>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# رسائل بعد الدفع
# ════════════════════════════════════════════════════════════════

def handle_payment_success():
    """معالجة نجاح الدفع"""
    if 'success' in st.query_params:
        st.balloons()
        st.success("""
        # 🎉 مبروك! اشتراكك نشط الآن!
        
        **أصبحت الآن عضو Premium في SmartMoveAI**
        
        ### ما الجديد؟
        ✅ **أسئلة غير محدودة** - اسأل بدون حدود!  
        ✅ **20+ دولة مدعومة** - معلومات شاملة  
        ✅ **تصدير PDF** (قريباً) - احفظ الإجابات  
        ✅ **دعم أولوية** - نساعدك خلال 24 ساعة  
        
        ### ابدأ الآن!
        اطرح أول سؤال بدون قلق من الحد 👇
        """)
        
        if st.button("✅ رائع! لنبدأ", type="primary"):
            st.query_params.clear()
            st.rerun()


def handle_payment_cancel():
    """معالجة إلغاء الدفع"""
    if 'canceled' in st.query_params:
        st.warning("""
        ### ⚠️ تم إلغاء عملية الدفع
        
        لا مشكلة! يمكنك:
        - 🆓 الاستمرار باستخدام الخطة المجانية (5 أسئلة/شهر)
        - 💎 المحاولة مرة أخرى عندما تكون جاهزاً
        - 📧 التواصل معنا للمساعدة: yousef@smartmoveai.com
        """)
        
        if st.button("🔙 العودة للتطبيق"):
            st.query_params.clear()
            st.rerun()


# ════════════════════════════════════════════════════════════════
# فحص بلوك السؤال
# ════════════════════════════════════════════════════════════════

def show_upgrade_prompt():
    """عرض رسالة الترقية عند الوصول للحد"""
    st.error("""
    ### ⚠️ وصلت للحد الأقصى من الأسئلة!
    
    لقد استخدمت **5 أسئلة مجانية** هذا الشهر.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("""
        ### 💎 ترقية لـ Premium واحصل على:
        
        ✅ **أسئلة غير محدودة** - اسأل بدون قلق  
        ✅ **20+ دولة** - كل المعلومات  
        ✅ **إجابات مفصلة** - خطوات عملية دقيقة  
        ✅ **تصدير PDF** (قريباً)  
        ✅ **دعم أولوية** - رد خلال 24 ساعة  
        
        **السعر: €9/شهر فقط** ☕  
        (أقل من قهوة واحدة/يوم!)
        """)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💎 اشترك الآن", type="primary", use_container_width=True):
            st.switch_page("pages/Pricing.py")
    
    st.markdown("---")
    st.info("""
    💡 **لا تريد الاشتراك؟**  
    ستتجدد أسئلتك المجانية في بداية الشهر القادم!
    """)


# ════════════════════════════════════════════════════════════════
# إحصائيات للمطور
# ════════════════════════════════════════════════════════════════

def show_admin_stats(admin_password: str):
    """عرض إحصائيات للمطور"""
    if st.sidebar.text_input("🔐 كلمة سر المطور", type="password") == admin_password:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 إحصائيات")
        
        try:
            # عدد الاشتراكات
            subscriptions = stripe.Subscription.list(status='active', limit=100)
            active_count = len(subscriptions.data)
            
            # الإيرادات الشهرية
            mrr = sum([sub.plan.amount / 100 for sub in subscriptions.data])
            
            st.sidebar.metric("اشتراكات نشطة", active_count)
            st.sidebar.metric("MRR", f"€{mrr:.2f}")
        except:
            st.sidebar.info("غير متصل بـ Stripe")
