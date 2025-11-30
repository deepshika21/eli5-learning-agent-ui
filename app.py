import streamlit as st
import requests
import uuid
import json
import os

# ================= CONFIG =================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
DATA_FILE = "chats.json"
# ==========================================

st.set_page_config(
    page_title="Understand Easily",
    page_icon="💡",
    layout="wide"
)

# ---------- PERSISTENCE ----------
def load_chats():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chats(chats):
    with open(DATA_FILE, "w") as f:
        json.dump(chats, f, indent=2)

# ---------- SESSION STATE ----------
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

if "active_chat" not in st.session_state or not st.session_state.chats:
    cid = str(uuid.uuid4())
    st.session_state.chats = {
        cid: {
            "title": "New Chat",
            "messages": []
        }
    }
    st.session_state.active_chat = cid
    save_chats(st.session_state.chats)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 💬 Chats")

    search = st.text_input("Search chats", placeholder="Search…")

    level = st.selectbox(
        "Explanation Level",
        ["Beginner", "School Student", "College Student", "Advanced"]
    )

    exam_mode = st.selectbox(
        "📘 Exam Mode",
        ["Normal", "2-mark answer", "5-mark answer"]
    )

    if st.button("➕ New Chat", use_container_width=True):
        cid = str(uuid.uuid4())
        st.session_state.chats[cid] = {"title": "New Chat", "messages": []}
        st.session_state.active_chat = cid
        save_chats(st.session_state.chats)
        st.rerun()

    if st.button("🧹 Clear All Chats", use_container_width=True):
        cid = str(uuid.uuid4())
        st.session_state.chats = {cid: {"title": "New Chat", "messages": []}}
        st.session_state.active_chat = cid
        save_chats(st.session_state.chats)
        st.rerun()

    st.divider()

    for cid, chat in st.session_state.chats.items():
        if search.lower() in chat["title"].lower():
            if st.button(chat["title"], key=cid, use_container_width=True):
                st.session_state.active_chat = cid
                st.rerun()

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, sans-serif !important;
    }

    #MainMenu, footer { visibility: hidden; }

    .stApp { background-color: #0d0f16; }

    .container { max-width: 1000px; margin: auto; }

    /* Chat bubbles – BROADER */
    .bubble {
        padding: 12px 16px;
        border-radius: 8px;
        margin: 0 auto 12px auto;
        line-height: 1.45;
        white-space: pre-wrap;
        font-size: 15px;
    }

    .user {
        background-color: #2b2f3a;
        max-width: 800px;
    }

    .assistant {
        background-color: #1c1f29;
        max-width: 720px;
    }

    /* Sidebar inputs – soft borders */
    section[data-testid="stSidebar"] div[data-baseweb="input"] > div {
        border-radius: 6px !important;
        background-color: #2b2f3a !important;
        border: 1px solid #444857 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"] input {
        background-color: #2b2f3a !important;
        color: #ffffff !important;
        border: none !important;
        padding: 10px 12px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"]:hover > div,
    section[data-testid="stSidebar"] div[data-baseweb="input"]:has(input:focus) > div {
        border: 1px solid #6b7280 !important;
    }

    section[data-testid="stSidebar"] button {
        border-radius: 6px !important;
        padding: 10px 12px !important;
        font-weight: 600 !important;
    }

    button[kind="primary"] {
        background-color: #c7ddff !important;
        color: #000 !important;
        border: none !important;
    }

    .caption {
        text-align: center;
        margin-top: 20px;
        color: #9ca3af;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.markdown(
    """
    <div class="container">
        <h2 style="text-align:center;">💡 Understand Easily</h2>
        <p style="text-align:center; color:#b8b9c4;">
            Learn concepts clearly. Answer exams confidently.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- CHAT DISPLAY ----------
st.markdown("<div class='container'>", unsafe_allow_html=True)

chat = st.session_state.chats[st.session_state.active_chat]

for msg in chat["messages"]:
    cls = "user" if msg["role"] == "user" else "assistant"
    st.markdown(f"<div class='bubble {cls}'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- INPUT ----------
user_input = st.chat_input("Ask a concept or exam question…")

# ---------- BACKEND ----------
if user_input:
    if chat["title"] == "New Chat":
        chat["title"] = user_input[:32] + ("…" if len(user_input) > 32 else "")

    chat["messages"].append({"role": "user", "content": user_input})

    with st.spinner("Explaining…"):
        try:
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={
                    "concept": user_input,
                    "level": level,
                    "exam_mode": exam_mode
                },
                timeout=60
            )
            output = response.json().get("output", "")
        except Exception as e:
            output = f"Request failed: {e}"

    chat["messages"].append({"role": "assistant", "content": output})
    save_chats(st.session_state.chats)
    st.rerun()

# ---------- FOOTER ----------
st.markdown("<p class='caption'>Built to understand, not memorise.</p>", unsafe_allow_html=True)
