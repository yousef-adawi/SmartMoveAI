import streamlit as st
from openai import OpenAI
from typing import List, Dict
import os

# --- إعداد الصفحة ---
st.set_page_config(
    page_title="SmartMoveAI — Migration Advisor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- تصميم مخصص ---
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f1f8e9;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #4caf50;
    }
    /* إخفاء زر الـ form الافتراضي */
    .stForm {
        border: none;
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
        "🌍 تركيز البلد",
        [
            "Netherlands 🇳🇱",
            "Germany 🇩🇪",
            "Belgium 🇧🇪",
            "Sweden 🇸🇪",
            "Denmark 🇩🇰",
            "Global - متعدد الدول 🌐"
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
    """استدعاء OpenAI API بالطريقة الجديدة"""
    try:
        # بناء system prompt ديناميكي
        country_context = ""
        if "Netherlands" in country_focus:
            country_context = "Focus on Netherlands (هولندا) immigration procedures, IND requirements, and Dutch law."
        elif "Germany" in country_focus:
            country_context = "Focus on Germany immigration, Ausländerbehörde procedures, and German law."
        elif "Global" in country_focus:
            country_context = "Provide general immigration guidance applicable to multiple countries."
        
        language_context = ""
        if "العربية" in language:
            language_context = "Always respond in Arabic."
        elif "English" in language:
            language_context = "Always respond in English."
        else:
            language_context = "Respond in the same language as the user's question."
        
        system_message = {
            "role": "system",
            "content": f"""You are SmartMoveAI, an expert Migration Advisor providing PRACTICAL, ACTIONABLE guidance.

CRITICAL INSTRUCTIONS:
1. Give SPECIFIC, DETAILED step-by-step instructions
2. Include EXACT document names, forms, and requirements
3. Provide REALISTIC timelines and costs
4. Give PRACTICAL examples and scenarios
5. NEVER just give links - explain the full process

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
• [وثيقة محددة + كيفية الحصول عليها]

💰 **التكاليف المتوقعة:**
• [تكلفة محددة بالأرقام]

⏰ **المدة الزمنية:**
• [مدة محددة بالأيام/أسابيع/شهور]

⚠️ **نصائح مهمة:**
• [نصيحة عملية محددة]

🔗 **المصادر الرسمية:**
• [رابط + شرح مختصر لما يحتويه]
━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLES OF GOOD VS BAD ANSWERS:

❌ BAD: "يمكنك زيارة موقع IND للمزيد من المعلومات."
✅ GOOD: "قدّم طلب لم الشمل عبر تعبئة نموذج MVV (Machtiging tot Voorlopig Verblijf) من موقع IND. ستحتاج: جواز سفر ساري، شهادة زواج مترجمة ومصدّقة، إثبات دخل شهري لا يقل عن €1,900، وعقد إيجار. التكلفة: €350 للطلب + €80 رسوم بصمة. المدة: 3-6 أشهر."

❌ BAD: "هناك عدة أنواع من التأشيرات."
✅ GOOD: "للعمل في ألمانيا كمهندس برمجيات، تحتاج تأشيرة Blue Card EU. الشروط: شهادة جامعية معترف بها، عرض عمل براتب سنوي لا يقل عن €43,800 (€56,400 للمهن غير النقص). قدّم الطلب في السفارة الألمانية بعد تثبيت موعد عبر موقعهم. المستندات: شهادة الجامعة مصدقة، عقد العمل، CV، جواز سفر، صور شخصية. المدة: 4-12 أسبوع. التكلفة: €75."

ALWAYS be specific, practical, and helpful. Never be vague."""
        }
        
        # إرسال الطلب
        response = client.chat.completions.create(
            model=model_name,
            messages=[system_message] + messages,
            max_tokens=1200,
            temperature=0.3,
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
    # رسائل ترحيبية احترافية
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px;'>
        <h2 style='margin: 0; color: white;'>👋 مرحباً بك في SmartMoveAI</h2>
        <p style='margin: 15px 0 0 0; font-size: 1.1em; opacity: 0.95;'>
            مساعدك الذكي للحصول على معلومات دقيقة وعملية عن الهجرة والإقامة
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # أسئلة سريعة مع أزرار
    st.markdown("### 🚀 ابدأ بسؤال سريع:")
    
    col1, col2, col3 = st.columns(3)
    
    quick_questions = {
        "🏠 لم الشمل": "كيف أقدم طلب لم شمل عائلي في هولندا؟ اشرح لي الخطوات بالتفصيل مع المستندات والتكاليف",
        "💼 تأشيرة عمل": "ما هي خطوات الحصول على تأشيرة عمل في ألمانيا كمهندس برمجيات؟ أريد معلومات مفصلة",
        "🎓 فيزا دراسية": "كيف أحصل على تأشيرة دراسية في هولندا؟ ما المستندات المطلوبة والتكاليف؟",
        "⏱️ مدة المعالجة": "كم تستغرق معالجة طلب الفيزا في السفارة الهولندية؟",
        "💰 التكاليف": "ما هي التكاليف الكاملة لطلب لم الشمل في هولندا؟",
        "📄 المستندات": "ما المستندات المطلوبة للحصول على إقامة عمل في بلجيكا؟"
    }
    
    questions_list = list(quick_questions.items())
    
    with col1:
        if st.button(questions_list[0][0], use_container_width=True, key="q1"):
            st.session_state.selected_question = questions_list[0][1]
        if st.button(questions_list[3][0], use_container_width=True, key="q4"):
            st.session_state.selected_question = questions_list[3][1]
    
    with col2:
        if st.button(questions_list[1][0], use_container_width=True, key="q2"):
            st.session_state.selected_question = questions_list[1][1]
        if st.button(questions_list[4][0], use_container_width=True, key="q5"):
            st.session_state.selected_question = questions_list[4][1]
    
    with col3:
        if st.button(questions_list[2][0], use_container_width=True, key="q3"):
            st.session_state.selected_question = questions_list[2][1]
        if st.button(questions_list[5][0], use_container_width=True, key="q6"):
            st.session_state.selected_question = questions_list[5][1]
    
    # معالجة السؤال المختار
    if "selected_question" in st.session_state:
        st.session_state.history.append({
            "role": "user",
            "content": st.session_state.selected_question
        })
        with st.spinner("🤔 جاري التفكير..."):
            answer = call_openai(st.session_state.history, model)
            st.session_state.history.append({
                "role": "assistant",
                "content": answer
            })
        del st.session_state.selected_question
        st.rerun()
    
    st.markdown("---")
    
    # معلومات إضافية
    st.markdown("### 📊 ماذا يمكنني أن أساعدك؟")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🌍 معلومات عن الدول:**
        - هولندا 🇳🇱 | ألمانيا 🇩🇪
        - بلجيكا 🇧🇪 | السويد 🇸🇪
        - الدنمارك 🇩🇰
        
        **📋 أنواع التأشيرات:**
        - تأشيرات العمل والدراسة
        - لم الشمل العائلي
        - طلبات اللجوء
        """)
    
    with col2:
        st.markdown("""
        **💡 نقدم لك:**
        - ✅ خطوات مفصلة وعملية
        - ✅ قوائم المستندات المطلوبة
        - ✅ التكاليف والمدد الزمنية
        - ✅ نصائح من خبراء
        - ✅ روابط رسمية موثوقة
        """)
    
    st.markdown("---")

# --- نموذج الإدخال (دائماً في الأسفل) ---
st.markdown("### ✍️ أو اكتب سؤالك الخاص:")

# القيمة الافتراضية للنص
default_text = ""
if "prefill_question" in st.session_state:
    default_text = st.session_state.prefill_question
    del st.session_state.prefill_question

with st.form("user_input", clear_on_submit=True):
    user_text = st.text_area(
        "اكتب سؤالك هنا",
        height=100,
        value=default_text,
        placeholder="مثال: أريد معلومات مفصلة عن لم الشمل في هولندا - الخطوات، المستندات، التكاليف، والمدة الزمنية",
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
