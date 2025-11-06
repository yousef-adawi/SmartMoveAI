import streamlit as st
from openai import OpenAI
from typing import List, Dict
import os

# استيراد تكامل Stripe
try:
    from stripe_integration import (
        init_stripe, 
        check_question_limit, 
        display_subscription_status,
        handle_payment_callback
    )
    STRIPE_ENABLED = True
except:
    STRIPE_ENABLED = False

# --- إعداد الصفحة ---
st.set_page_config(
    page_title="SmartMoveAI — Migration Advisor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# معالجة callbacks من Stripe في بداية التطبيق
if STRIPE_ENABLED:
    handle_payment_callback()

# --- تصميم مخصص ---
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border-right: 5px solid #2196f3;
        font-size: 1.1em;
        color: #000;
        font-weight: 500;
    }
    .assistant-message {
        background-color: #f1f8e9;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border-right: 5px solid #4caf50;
        font-size: 1.05em;
        color: #000;
        line-height: 1.8;
    }
    /* جعل النص أكثر وضوحاً */
    .stTextArea textarea {
        font-size: 1.1em !important;
        color: #000 !important;
        font-weight: 500 !important;
    }
    /* تحسين الأزرار */
    .stButton button {
        font-weight: 600 !important;
        font-size: 1.05em !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>🌍 SmartMoveAI</h1><h3>مساعدك الذكي للهجرة والإقامة</h3><p style='margin-top: 10px; font-size: 0.9em; opacity: 0.9;'>احصل على معلومات دقيقة وعملية - خطوات مفصلة، مستندات، تكاليف، ومواعيد</p></div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 15px; background-color: #e8f4f8; border-radius: 10px; margin-bottom: 20px; border-right: 5px solid #2196f3;'>
    💼 <b>للشركات:</b> نقدم حلول API وتكامل مخصص | 
    📧 <b>تواصل:</b> <a href='mailto:yousef@smartmoveai.com' style='color: #2196f3; text-decoration: none;'>yousef@smartmoveai.com</a>
</div>
""", unsafe_allow_html=True)

# --- الإعدادات الجانبية ---
with st.sidebar:
    st.header("⚙️ الإعدادات")
    
    # معالجة callbacks من Stripe وعرض حالة الاشتراك
    if STRIPE_ENABLED:
        if 'user_email' in st.session_state:
            display_subscription_status(st.session_state.get('user_email'))
        else:
            # عرض معلومات Free plan
            st.info("🆓 **Free Plan**\n\n10 أسئلة/شهر")
            if st.button("💎 ترقية"):
                st.switch_page("pages/Pricing.py")
        st.markdown("---")
    
    # قراءة مفتاح OpenAI
    openai_api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        st.error("⚠️ لم يتم العثور على OpenAI API Key")
        st.info("أضف المفتاح في: **Settings → Secrets** في Streamlit Cloud")
        st.code('OPENAI_API_KEY = "sk-..."')
        st.stop()
    
    # إنشاء عميل OpenAI
    client = OpenAI(api_key=openai_api_key)
    
    # خيارات الموديل
    model = st.selectbox(
        "🤖 اختر الموديل",
        ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
        index=0,
        help="gpt-4o-mini: أسرع وأرخص | gpt-4o: أذكى وأدق"
    )
    
    # تركيز البلد
    country_focus = st.selectbox(
        "🌍 اختر الدولة",
        [
            "🌐 Global - جميع الدول",
            "🇳🇱 Netherlands - هولندا",
            "🇩🇪 Germany - ألمانيا",
            "🇧🇪 Belgium - بلجيكا",
            "🇸🇪 Sweden - السويد",
            "🇩🇰 Denmark - الدنمارك",
            "🇨🇦 Canada - كندا",
            "🇦🇺 Australia - أستراليا",
            "🇺🇸 USA - أمريكا",
            "🇬🇧 UK - بريطانيا",
            "🇫🇷 France - فرنسا",
            "🇮🇹 Italy - إيطاليا",
            "🇪🇸 Spain - إسبانيا",
            "🇦🇪 UAE - الإمارات",
            "🇸🇦 Saudi Arabia - السعودية",
            "🇶🇦 Qatar - قطر",
            "🇳🇿 New Zealand - نيوزيلندا",
            "🇸🇬 Singapore - سنغافورة",
            "🇯🇵 Japan - اليابان",
            "🇰🇷 South Korea - كوريا الجنوبية"
        ],
        index=0
    )
    
    # اللغة المفضلة
    language = st.selectbox(
        "🗣️ لغة الإجابة",
        ["العربية 🇸🇦", "English 🇬🇧", "تلقائي (حسب السؤال) 🔄"],
        index=2
    )
    
    st.divider()
    
    # إحصائيات
    if "history" in st.session_state:
        num_messages = len([m for m in st.session_state.history if m["role"] == "user"])
        st.metric("📊 عدد الأسئلة", num_messages)
    
    st.divider()
    
    # ملاحظات
    with st.expander("ℹ️ معلومات هامة"):
        st.warning("⚠️ هذه نسخة تجريبية")
        st.info("🔒 لا تشارك معلومات شخصية حساسة")
        st.success("✅ الإجابات إرشادية وليست استشارة قانونية")

# --- تهيئة المحادثة ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- دالة استدعاء OpenAI ---
def call_openai(messages: List[Dict[str, str]], model_name: str) -> str:
    """استدعاء OpenAI API مع قدرة التصحيح الذاتي"""
    try:
        # استخراج اسم الدولة من الاختيار
        country_name = country_focus.split(" - ")[1] if " - " in country_focus else "any country"
        country_emoji = country_focus.split(" ")[0] if country_focus else "🌐"
        
        # بناء system prompt ديناميكي مع التحقق الذاتي
        country_context = ""
        if "Netherlands" in country_focus or "هولندا" in country_focus:
            country_context = "Focus on Netherlands (هولندا) immigration procedures, IND requirements, and Dutch law."
        elif "Germany" in country_focus or "ألمانيا" in country_focus:
            country_context = "Focus on Germany immigration, Ausländerbehörde procedures, and German law."
        elif "Canada" in country_focus or "كندا" in country_focus:
            country_context = "Focus on Canada immigration, Express Entry, PNP programs, and IRCC procedures."
        elif "Australia" in country_focus or "أستراليا" in country_focus:
            country_context = "Focus on Australia immigration, SkillSelect, visa subclasses, and Department of Home Affairs."
        elif "USA" in country_focus or "أمريكا" in country_focus:
            country_context = "Focus on USA immigration, USCIS procedures, green card, and visa categories."
        elif "UK" in country_focus or "بريطانيا" in country_focus:
            country_context = "Focus on UK immigration, Home Office procedures, and UK visa routes."
        elif "UAE" in country_focus or "الإمارات" in country_focus:
            country_context = "Focus on UAE immigration, residence visa, work permits, and GDRFA procedures."
        elif "Global" in country_focus or "جميع" in country_focus:
            country_context = f"Provide general immigration guidance. If the user asks about a specific country, focus on that country's procedures."
        else:
            # أي دولة أخرى - ديناميكي
            country_context = f"Focus on {country_name} immigration procedures, official requirements, and local laws. Provide accurate information specific to this country."
        
        language_context = ""
        if "العربية" in language:
            language_context = "Always respond in Arabic."
        elif "English" in language:
            language_context = "Always respond in English."
        else:
            language_context = "Respond in the same language as the user's question."
        
        system_message = {
            "role": "system",
            "content": f"""You are SmartMoveAI, an expert Migration Advisor providing PRACTICAL, ACTIONABLE guidance for immigration worldwide.

⚠️ CRITICAL - ACCURACY & SELF-CORRECTION:
1. If you're NOT 100% certain about any specific number, cost, or timeline - SAY SO
2. Use phrases like: "تقريباً" (approximately), "عادةً" (usually), "قد يختلف" (may vary)
3. ALWAYS mention: "تحقق من الموقع الرسمي للمعلومات المحدثة"
4. If immigration laws changed recently (2024-2025), acknowledge this
5. NEVER invent specific numbers - if unsure, give a range
6. If you made an error in previous messages, CORRECT IT immediately

VERIFICATION PHRASES (use these):
• "وفقاً للمعلومات الأخيرة المتاحة..." (According to latest available information)
• "اعتباراً من 2024..." (As of 2024...)
• "قد تختلف الأرقام حسب الحالة الفردية" (Numbers may vary by individual case)
• "⚠️ تنبيه: تحقق من الموقع الرسمي قبل التقديم" (Warning: verify with official website)

{country_context}
{language_context}

RESPONSE FORMAT (ALWAYS follow this):
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 **الخطوات العملية:**
1. [خطوة محددة مع تفاصيل دقيقة]
2. [خطوة محددة مع تفاصيل دقيقة]
...

📄 **المستندات المطلوبة:**
• [وثيقة محددة + كيفية الحصول عليها]

💰 **التكاليف المتوقعة:** (تقريبية - قد تتغير)
• [تكلفة مع التاريخ: "اعتباراً من 2024"]

⏰ **المدة الزمنية:** (قد تختلف)
• [مدة متوسطة مع نطاق]

⚠️ **تحذير مهم:**
• ⚠️ المعلومات أعلاه إرشادية - تحقق من الموقع الرسمي قبل التقديم
• القوانين قد تتغير - استشر محامي هجرة للحالات المعقدة

🔗 **المصادر الرسمية للتحقق:**
• [رابط رسمي + "تحقق من هنا للمعلومات المحدثة"]
━━━━━━━━━━━━━━━━━━━━━━━━━━

QUALITY CHECKS BEFORE RESPONDING:
✓ Are all numbers accurate or clearly marked as approximate?
✓ Did I provide official source links?
✓ Did I warn about verifying information?
✓ Did I avoid inventing specific details?
✓ If unsure, did I say "approximately" or give a range?

EXAMPLES OF GOOD SELF-AWARE ANSWERS:

✅ GOOD: "رسوم الطلب تقريباً €350 (اعتباراً من 2024، قد تتغير). تحقق من موقع IND للرسوم المحدثة."
❌ BAD: "رسوم الطلب €350 بالضبط."

✅ GOOD: "المدة عادةً 3-6 أشهر، لكن قد تستغرق أطول حسب تعقيد الحالة."
❌ BAD: "المدة بالضبط 4 أشهر."

✅ GOOD: "وفقاً للمعلومات المتاحة حتى 2024، الحد الأدنى للدخل €1,900/شهر. ⚠️ تحقق من IND للمتطلبات الحالية."
❌ BAD: "الحد الأدنى للدخل €1,900 دائماً."

ALWAYS be specific but honest about uncertainty. Better to say "I'm not 100% sure" than give wrong information."""
        }
        
        # إرسال الطلب
        response = client.chat.completions.create(
            model=model_name,
            messages=[system_message] + messages,
            max_tokens=1500,
            temperature=0.2,  # أقل للحصول على إجابات أكثر دقة
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ حدث خطأ: {str(e)}\n\nتأكد من صحة مفتاح API في الإعدادات."

# --- عرض المحادثة في الأعلى ---
if st.session_state.history:
    st.markdown("---")
    st.subheader("💬 سجل المحادثة")
    
    # عرض المحادثات (الأحدث في الأسفل)
    for i, msg in enumerate(st.session_state.history):
        if msg["role"] == "user":
            st.markdown(f"""
            <div class='user-message'>
                <b>👤 أنت:</b><br>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='assistant-message'>
                <b>🤖 SmartMoveAI:</b><br>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
else:
    # واجهة بسيطة وواضحة
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 40px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px;'>
        <h2 style='margin: 0; color: white; font-size: 2em;'>👋 مرحباً بك في SmartMoveAI</h2>
        <p style='margin: 20px 0 0 0; font-size: 1.3em; font-weight: 500;'>
            احصل على معلومات دقيقة ومفصلة عن الهجرة والإقامة
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # معلومات واضحة بدون تعقيد
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #667eea; margin-top: 0;'>🌍 دول مدعومة</h3>
            <p style='font-size: 1em; line-height: 1.6; color: #333;'>
                🇳🇱 هولندا | 🇩🇪 ألمانيا | 🇧🇪 بلجيكا<br>
                🇸🇪 السويد | 🇩🇰 الدنمارك<br>
                🇨🇦 كندا | 🇦🇺 أستراليا | 🇺🇸 أمريكا<br>
                🇬🇧 بريطانيا | 🇫🇷 فرنسا | 🇮🇹 إيطاليا<br>
                🇦🇪 الإمارات | 🇸🇦 السعودية | 🇶🇦 قطر<br>
                <b style='color: #667eea;'>+ أي دولة أخرى!</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #667eea; margin-top: 0;'>💼 ما نقدمه</h3>
            <p style='font-size: 1.1em; line-height: 1.8; color: #333;'>
                ✅ خطوات مفصلة وعملية<br>
                ✅ المستندات المطلوبة<br>
                ✅ التكاليف الدقيقة<br>
                ✅ المدد الزمنية<br>
                ✅ روابط رسمية
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

# --- نموذج الإدخال (دائماً في الأسفل) ---
st.markdown("### ✍️ اكتب سؤالك:")

with st.form("user_input", clear_on_submit=True):
    user_text = st.text_area(
        "سؤالك",
        height=120,
        placeholder="إلى أين تريد الهجرة؟ اسألني عن أي دولة...",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        submitted = st.form_submit_button("📤 إرسال", use_container_width=True, type="primary")
    with col2:
        clear_btn = st.form_submit_button("🗑️ مسح المحادثة", use_container_width=True)

# --- معالجة زر المسح ---
if clear_btn:
    st.session_state.history = []
    st.rerun()

# --- معالجة الإرسال ---
if submitted and user_text.strip():
    # التحقق من حد الأسئلة
    if STRIPE_ENABLED:
        is_allowed, remaining, limit, is_premium = check_question_limit(
            st.session_state.get('user_email', None)
        )
        
        if not is_allowed:
            st.error(f"""
            ⚠️ **وصلت للحد الأقصى من الأسئلة!**
            
            لقد استخدمت {limit} أسئلة من أصل {limit} في الخطة المجانية.
            """)
            
            st.info("""
            💎 **اشترك في Premium للحصول على:**
            - ✅ أسئلة غير محدودة
            - ✅ كل الدول (20+)
            - ✅ تصدير PDF
            - ✅ دعم أولوية 24/7
            
            **السعر: €19.99/شهر فقط**
            """)
            
            if st.button("💎 اشترك الآن", type="primary"):
                st.switch_page("pages/Pricing.py")
            
            st.stop()
    
    # إضافة سؤال المستخدم
    st.session_state.history.append({
        "role": "user",
        "content": user_text.strip()
    })
    
    # عرض مؤشر التحميل
    with st.spinner("🤔 جاري التفكير..."):
        # استدعاء OpenAI
        answer = call_openai(st.session_state.history, model)
        
        # إضافة الإجابة
        st.session_state.history.append({
            "role": "assistant",
            "content": answer
        })
    
    # إعادة تحميل لعرض الإجابة الجديدة
    st.rerun()

# --- Footer ---
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>
            💻 تطوير: <b>Yousef Adawi</b><br>
            📧 للاستفسارات والتخصيص: yousef@smartmoveai.com<br>
            🔗 <a href='https://github.com/yousef-adawi/SmartMoveAI' target='_blank'>GitHub</a> | 
            <a href='https://smartmoveai.streamlit.app' target='_blank'>Demo</a>
        </p>
        <p style='font-size: 12px; margin-top: 10px;'>
            ⚠️ نسخة تجريبية Beta v1.0 | الإجابات إرشادية فقط
        </p>
    </div>
    """, unsafe_allow_html=True)
