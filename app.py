import streamlit as st
import requests
import uuid

# ================= CONFIG =================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
# ==========================================

st.set_page_config(
    page_title="Understand Easily",
    page_icon="💡",
    layout="wide"
)

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = str(uuid.uuid4())  # unique chat ID

if st.session_state.current_chat not in st.session_state.messages:
    st.session_state.messages[st.session_state.current_chat] = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 💬 Chats")

    # Search chats
    search = st.text_input("Search chats")

    # New Chat button
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.current_chat = new_id
        st.session_state.messages[new_id] = []
        st.experimental_rerun()

    # Chat list
    for chat_id, msgs in st.session_state.messages.items():
        if msgs:
            title = msgs[0]["content"][:25] + "..."
        else:
            title = "Empty Chat"

        if search.lower() in title.lower():
            if st.button(title):
                st.session_state.current_chat = chat_id
                st.experimental_rerun()


# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', sans-serif !important;
    }

    header[data-testid="stHeader"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp { background-color: #0d0f16; }

    .chat-box {
        max-width: 900px;
        margin: auto;
        padding-top: 20px;
    }

    .bubble {
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 16px;
        line-height: 1.6;
        white-space: pre-wrap;
        font-size: 16px;
    }

    .user { background-color: #2b2f3a; }
    .assistant { background-color: #1c1f29; }

    textarea {
        background: #2b2f3a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #3a3f4d !important;
        font-size: 16px !important;
    }
    textarea:focus {
        border: 1px solid #6b7280 !important;
    }

    button[kind="primary"] {
        background-color: #bcdcff !important;
        color: #000 !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
    }

    .caption {
        text-align:center;
        margin-top: 30px;
        color:#9ca3af;
        font-size:14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.markdown(
    "<h2 style='text-align:center;'>💡 Understand Easily</h2>"
    "<p style='text-align:center; color:#b8b9c4;'>Learning made simple, one explanation at a time.</p>",
    unsafe_allow_html=True
)

# ---------- CHAT DISPLAY ----------
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

for msg in st.session_state.messages[st.session_state.current_chat]:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(f"<div class='bubble {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- INPUT ----------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "",
        placeholder="Ask a concept or follow-up question...",
        height=80
    )
    level = st.selectbox(
        "Level",
        ["Beginner", "School Student", "College Student", "Advanced"]
    )

    submitted = st.form_submit_button("Explain")

# ---------- ENTER KEY TO SUBMIT ----------
st.markdown(
    """
    <script>
    const textarea = parent.document.querySelector('textarea');
    textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const btn = parent.document.querySelector('button[kind="primary"]');
            if (btn) btn.click();
        }
    });
    </script>
    """,
    unsafe_allow_html=True
)

# ---------- BACKEND CALL ----------
if submitted and user_input.strip():
    chat_id = st.session_state.current_chat

    st.session_state.messages[chat_id].append({"role": "user", "content": user_input})

    with st.spinner("Explaining..."):
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"concept": user_input, "level": level},
            timeout=60
        )

        if response.status_code == 200:
            output = response.json().get("output", "")
        else:
            output = "Something went wrong."

    st.session_state.messages[chat_id].append({"role": "assistant", "content": output})
    st.experimental_rerun()

# ---------- FOOTER ----------
st.markdown("<p class='caption'>Learning made simple, one explanation at a time.</p>", unsafe_allow_html=True)
