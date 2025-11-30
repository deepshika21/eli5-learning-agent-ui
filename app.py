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
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "active_chat" not in st.session_state:
    cid = str(uuid.uuid4())
    st.session_state.chats[cid] = []
    st.session_state.active_chat = cid

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("Chats 🗪")

    search = st.text_input("Search chats")

    st.divider()

    level = st.selectbox(
        "Level 🎯",
        ["Beginner", "School Student", "College Student", "Advanced"]
    )

    st.divider()

    if st.button("New Chat ✚"):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = []
        st.session_state.active_chat = new_id
        st.rerun()

    for cid, msgs in st.session_state.chats.items():
        title = msgs[0]["content"][:28] + "…" if msgs else "Empty Chat"
        if search.lower() in title.lower():
            if st.button(title, key=cid):
                st.session_state.active_chat = cid
                st.rerun()

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, sans-serif !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background-color: #0d0f16;
    }

    .container {
        max-width: 900px;
        margin: auto;
    }

    .bubble {
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 14px;
        line-height: 1.6;
        white-space: pre-wrap;
        font-size: 15.5px;
    }

    .user {
        background-color: #2b2f3a;
    }

    .assistant {
        background-color: #1c1f29;
    }

    /* Inputs unified shape */
    input, textarea, select {
        border-radius: 8px !important;
    }

    div[data-baseweb="input"] input {
        background-color: #2b2f3a !important;
        color: #ffffff !important;
        border: 1px solid #3a3f4d !important;
    }

    div[data-baseweb="input"] input:focus {
        border: 1px solid #6b7280 !important;
        outline: none !important;
        box-shadow: none !important;
    }

    button[kind="primary"] {
        background-color: #c7ddff !important;
        color: #000 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 10px 22px !important;
        border: none !important;
    }

    button[kind="primary"]:hover {
        opacity: 0.85;
    }

    .caption {
        text-align:center;
        margin-top: 20px;
        color:#9ca3af;
        font-size:14px;
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
            Learning made simple, one explanation at a time.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- CHAT DISPLAY ----------
st.markdown("<div class='container'>", unsafe_allow_html=True)

chat = st.session_state.chats[st.session_state.active_chat]
for msg in chat:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(
        f"<div class='bubble {role_class}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# ---------- CHAT INPUT (ENTER SUBMITS, SHIFT+ENTER = NEW LINE) ----------
user_input = st.chat_input("Ask a concept or follow-up question…")

# ---------- BACKEND CALL ----------
if user_input:
    chat.append({"role": "user", "content": user_input})

    with st.spinner("Explaining..."):
        try:
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={
                    "concept": user_input,
                    "level": level
                },
                timeout=60
            )

            if response.status_code == 200:
                output = response.json().get("output", "")
            else:
                output = "Something went wrong while generating the explanation."

        except Exception as e:
            output = f"Request failed: {e}"

    chat.append({"role": "assistant", "content": output})
    st.rerun()

# ---------- FOOTER ----------
st.markdown(
    "<p class='caption'>Built to understand, not memorise.</p>",
    unsafe_allow_html=True
)


