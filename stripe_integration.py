"""
SmartMoveAI - Stripe Integration Module
تكامل كامل مع Stripe للاشتراكات والمدفوعات
"""

import stripe
import streamlit as st
from datetime import datetime, timedelta

# ════════════════════════════════════════════════════════════════
# إعداد Stripe
# ════════════════════════════════════════════════════════════════

def init_stripe():
    """تهيئة Stripe بالمفتاح السري"""
    try:
        if "STRIPE_SECRET_KEY" not in st.secrets:
            return False
        stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
        return True
    except Exception as e:
        st.sidebar.warning(f"⚠️ Stripe غير مفعّل")
        return False


# ════════════════════════════════════════════════════════════════
# إنشاء Checkout Session
# ════════════════════════════════════════════════════════════════

def create_checkout_session(price_id: str, customer_email: str, customer_name: str = ""):
    """
    إنشاء جلسة دفع Stripe
    
    Args:
        price_id: معرف السعر من Stripe
        customer_email: بريد العميل
        customer_name: اسم العميل (اختياري)
    
    Returns:
        URL جلسة الدفع أو None في حال الخطأ
    """
    try:
        # إنشاء الجلسة
        session = stripe.checkout.Session.create(
            customer_email=customer_email,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f'{st.secrets.get("APP_URL", "https://smartmoveai.streamlit.app")}?success=true&session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{st.secrets.get("APP_URL", "https://smartmoveai.streamlit.app")}?canceled=true',
            metadata={
                'customer_name': customer_name,
                'plan': 'premium' if 'premium' in price_id.lower() else 'business'
            },
            allow_promotion_codes=True,  # السماح بكودات الخصم
        )
        
        return session.url
    
    except stripe.error.StripeError as e:
        st.error(f"❌ خطأ في Stripe: {e.user_message}")
        return None
    except Exception as e:
        st.error(f"❌ خطأ غير متوقع: {str(e)}")
        return None


# ════════════════════════════════════════════════════════════════
# التحقق من الاشتراك
# ════════════════════════════════════════════════════════════════

def get_customer_subscription(customer_email: str):
    """
    التحقق من اشتراك العميل
    
    Args:
        customer_email: بريد العميل
    
    Returns:
        dict مع معلومات الاشتراك أو None
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
        
        # استخراج معلومات الاشتراك
        return {
            'id': sub.id,
            'status': sub.status,
            'plan': sub.plan.nickname or 'Premium',
            'amount': sub.plan.amount / 100,  # تحويل من cents
            'currency': sub.plan.currency.upper(),
            'current_period_end': datetime.fromtimestamp(sub.current_period_end),
            'cancel_at_period_end': sub.cancel_at_period_end,
        }
    
    except Exception as e:
        print(f"خطأ في التحقق من الاشتراك: {e}")
        return None


# ════════════════════════════════════════════════════════════════
# إلغاء الاشتراك
# ════════════════════════════════════════════════════════════════

def cancel_subscription(subscription_id: str):
    """
    إلغاء اشتراك في نهاية الفترة الحالية
    
    Args:
        subscription_id: معرف الاشتراك
    
    Returns:
        True في حال النجاح
    """
    try:
        stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
        )
        return True
    except Exception as e:
        st.error(f"❌ خطأ في إلغاء الاشتراك: {e}")
        return False


# ════════════════════════════════════════════════════════════════
# استرجاع الاشتراك
# ════════════════════════════════════════════════════════════════

def reactivate_subscription(subscription_id: str):
    """
    إعادة تفعيل اشتراك ملغي
    
    Args:
        subscription_id: معرف الاشتراك
    
    Returns:
        True في حال النجاح
    """
    try:
        stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False
        )
        return True
    except Exception as e:
        st.error(f"❌ خطأ في إعادة تفعيل الاشتراك: {e}")
        return False


# ════════════════════════════════════════════════════════════════
# إدارة حد الأسئلة
# ════════════════════════════════════════════════════════════════

def check_question_limit(user_email: str = None):
    """
    التحقق من حد الأسئلة للمستخدم
    
    Returns:
        tuple: (is_allowed: bool, remaining: int, limit: int, is_premium: bool)
    """
    # إذا لم يكن هناك email - اعتبره Free user
    if not user_email:
        questions_asked = len([m for m in st.session_state.get('history', []) if m["role"] == "user"])
        remaining = max(0, 10 - questions_asked)
        return (remaining > 0, remaining, 10, False)
    
    # التحقق من الاشتراك
    subscription = get_customer_subscription(user_email)
    
    if subscription and subscription['status'] == 'active':
        # Premium user - بدون حد
        return (True, float('inf'), float('inf'), True)
    else:
        # Free user - 10 أسئلة
        questions_asked = len([m for m in st.session_state.get('history', []) if m["role"] == "user"])
        remaining = max(0, 10 - questions_asked)
        return (remaining > 0, remaining, 10, False)


# ════════════════════════════════════════════════════════════════
# واجهة عرض حالة الاشتراك
# ════════════════════════════════════════════════════════════════

def display_subscription_status(user_email: str):
    """
    عرض حالة الاشتراك في Sidebar
    
    Args:
        user_email: بريد المستخدم
    """
    subscription = get_customer_subscription(user_email)
    
    if subscription:
        st.sidebar.success("✅ **Premium Active**")
        st.sidebar.info(f"""
        **الخطة:** {subscription['plan']}  
        **المبلغ:** {subscription['amount']} {subscription['currency']}/شهر  
        **ينتهي في:** {subscription['current_period_end'].strftime('%Y-%m-%d')}
        """)
        
        if subscription['cancel_at_period_end']:
            st.sidebar.warning("⚠️ سيتم إلغاء الاشتراك في نهاية الفترة")
            if st.sidebar.button("♻️ إعادة تفعيل"):
                if reactivate_subscription(subscription['id']):
                    st.sidebar.success("✅ تم إعادة التفعيل!")
                    st.rerun()
        else:
            if st.sidebar.button("❌ إلغاء الاشتراك"):
                if cancel_subscription(subscription['id']):
                    st.sidebar.success("✅ سيتم الإلغاء في نهاية الفترة")
                    st.rerun()
    else:
        is_allowed, remaining, limit, _ = check_question_limit(user_email)
        
        st.sidebar.warning("🆓 **Free Plan**")
        st.sidebar.info(f"""
        **الأسئلة المتبقية:** {remaining}/{limit}
        """)
        
        if remaining <= 3:
            st.sidebar.error(f"⚠️ بقي {remaining} أسئلة فقط!")
        
        st.sidebar.markdown("[💎 ترقية إلى Premium](/Pricing)", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# معالجة Success/Cancel URLs
# ════════════════════════════════════════════════════════════════

def handle_payment_callback():
    """
    معالجة العودة من صفحة الدفع
    """
    # التحقق من نجاح الدفع
    if 'success' in st.query_params:
        st.success("""
        🎉 **تم الاشتراك بنجاح!**
        
        مرحباً بك في SmartMoveAI Premium!
        
        ✅ أسئلة غير محدودة
        ✅ كل الدول (20+)
        ✅ تصدير PDF
        ✅ دعم أولوية
        
        ابدأ الآن بطرح أسئلتك! 🚀
        """)
        
        # مسح الـ query parameter
        if st.button("✅ فهمت - لنبدأ!"):
            st.query_params.clear()
            st.rerun()
    
    # التحقق من إلغاء الدفع
    elif 'canceled' in st.query_params:
        st.warning("""
        ⚠️ **تم إلغاء عملية الدفع**
        
        لا مشكلة! يمكنك المحاولة مرة أخرى متى شئت.
        
        💡 لا زال بإمكانك استخدام الخطة المجانية (10 أسئلة/شهر)
        """)
        
        if st.button("🔙 العودة للتطبيق"):
            st.query_params.clear()
            st.rerun()


# ════════════════════════════════════════════════════════════════
# Test Functions
# ════════════════════════════════════════════════════════════════

def test_stripe_connection():
    """
    اختبار الاتصال بـ Stripe
    """
    try:
        # محاولة استرجاع معلومات الحساب
        account = stripe.Account.retrieve()
        st.success(f"✅ متصل بـ Stripe: {account.business_profile.name}")
        return True
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال بـ Stripe: {e}")
        return False
