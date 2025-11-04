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
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>🌍 SmartMoveAI</h1><h3>مساعدك الذكي للهجرة</h3></div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 10px; background-color: #fff3cd; border-radius: 5px; margin-bottom: 20px;'>
    💡 <b>واجهة تجريبية</b> — اسأل عن الهجرة، التأشيرات، لمّ الشمل، أو أي استفسار قانوني
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

# --- نموذج الإدخال ---
with st.form("user_input", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_text = st.text_area(
            "💬 اكتب سؤالك:",
            height=120,
            placeholder="مثال: كيف أقدم طلب لم شمل في هولندا؟\nمثال: ما هي شروط تأشيرة العمل في ألمانيا؟",
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")  # مسافة
        submitted = st.form_submit_button("📤 إرسال", use_container_width=True, type="primary")
        
        # أمثلة سريعة
        if st.form_submit_button("💡 مثال", use_container_width=True):
            user_text = "كيف أقدم طلب لم شمل في هولندا؟"

# --- دالة استدعاء OpenAI (محدثة) ---
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
            "content": f"""You are SmartMoveAI, an expert Migration Advisor AI assistant.

Your role:
- Provide accurate, practical, and up-to-date immigration guidance
- Give step-by-step instructions with required documents
- Mention official sources (e.g., IND.nl for Netherlands)
- Clearly state when professional legal advice is needed
- Be empathetic and supportive

{country_context}
{language_context}

Important:
- Use bullet points for clarity
- Include timelines when relevant
- Mention costs if applicable
- Always recommend consulting official sources or lawyers for complex cases"""
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
    
    # إعادة تحميل الصفحة لعرض الرد
    st.rerun()

# --- عرض المحادثة ---
if st.session_state.history:
    st.markdown("---")
    st.subheader("💬 سجل المحادثة")
    
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
    
    # زر مسح المحادثة
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🗑️ مسح المحادثة", use_container_width=True):
            st.session_state.history = []
            st.rerun()
else:
    # رسائل ترحيبية
    st.info("👋 مرحباً! اسألني أي سؤال عن الهجرة، التأشيرات، أو الإجراءات القانونية")
    
    # أمثلة مقترحة
    st.markdown("### 💡 أمثلة على الأسئلة:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - 🏠 كيف أقدم طلب لم شمل في هولندا؟
        - 💼 ما هي شروط تأشيرة العمل؟
        - 📄 ما المستندات المطلوبة للإقامة؟
        """)
    
    with col2:
        st.markdown("""
        - ⏱️ كم يستغرق معالجة طلب الفيزا؟
        - 💰 ما هي تكاليف طلب اللجوء؟
        - 🎓 كيف أحصل على فيزا دراسية؟
        """)

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
