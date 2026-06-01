import streamlit as st
from openai import OpenAI
import os

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="🤖 Data Analysis AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS STYLING
# ============================================
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #E3F2FD;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #1E88E5;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR - API KEY & SETTINGS
# ============================================
with st.sidebar:
    st.title("⚙️ Settings")
    
    st.markdown("### 🔑 API Key")
    api_key = st.text_input(
        "Enter your Groq API Key:",
        type="password",
        help="Get free API key from https://console.groq.com"
    )
    
    if not api_key:
        st.warning("⚠️ Please enter your API key to continue")
        st.stop()
    
    os.environ["GROQ_API_KEY"] = api_key
    
    st.markdown("---")
    st.markdown("### 📚 Assistant Features")
    st.markdown("""
    <div class="feature-box">
    ✅ SQL Query Help<br>
    ✅ Python/Pandas Code<br>
    ✅ Data Analysis Questions<br>
    ✅ EDA Guidance<br>
    ✅ Project Ideas<br>
    ✅ Internship Tips
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("""
    This AI assistant helps you with:
    - SQL queries and practice
    - Python data analysis code
    - Exploratory Data Analysis (EDA)
    - Portfolio project ideas
    - Internship preparation
    
    Built with Streamlit & Groq AI
    """)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# ============================================
# MAIN HEADER
# ============================================
st.markdown('<div class="main-header">🤖 Data Analysis AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your personal AI tutor for SQL, Python, and Data Analysis</div>', unsafe_allow_html=True)

# ============================================
# QUICK QUESTIONS BUTTONS
# ============================================
st.markdown("### ⚡ Quick Questions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 SQL Help"):
        if "quick_question" not in st.session_state:
            st.session_state.quick_question = ""
        st.session_state.quick_question = "Can you help me write a SQL query?"
with col2:
    if st.button("🐍 Python Code"):
        st.session_state.quick_question = "Can you help me with Python/Pandas code?"
with col3:
    if st.button("📈 EDA Tips"):
        st.session_state.quick_question = "Can you give me EDA tips for my project?"
with col4:
    if st.button("💼 Internship"):
        st.session_state.quick_question = "Can you give me internship tips for data analyst?"

# Handle quick question
if st.session_state.get('quick_question'):
    user_input = st.session_state.quick_question
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.quick_question = None
    st.rerun()

# ============================================
# INITIALIZE CHAT HISTORY
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================
# DISPLAY CHAT MESSAGES
# ============================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# CHAT INPUT
# ============================================
if prompt := st.chat_input("Ask me anything about SQL, Python, Data Analysis..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 Thinking...")
        
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert Data Analysis AI Assistant. Help students learn data analysis skills.

TOPICS: SQL, Python/Pandas, Data Visualization, EDA, Portfolio Projects, Internships

STYLE: Friendly, simple language, code examples, step-by-step guidance, practical

FORMAT: Bullet points, code blocks, bold text for important points"""
                    },
                    *st.session_state.messages
                ],
                temperature=0.7,
                max_tokens=1024
            )
            
            answer = response.choices[0].message.content
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            message_placeholder.error(f"❌ Error: {str(e)}\nPlease check your API key.")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🤖 Built with ❤️ for Data Analysis Students</p>
    <p>Powered by Groq AI & Streamlit | Free Tier Available</p>
</div>
""", unsafe_allow_html=True)
