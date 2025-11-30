import streamlit as st
import requests

# =============== CONFIG ===================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
# =========================================

st.set_page_config(
    page_title="Understand Easily",
    page_icon="🧠",
    layout="centered"
)

# ---------- SESSION STATE ----------
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}
    st.session_state.current_chat = "Chat 1"

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 1

# ---------- CSS ----------
st.markdown(
    """
    <style>
    * {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }

    .stApp {
        background-color: #0d0f16;
        color: #ffffff;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 600;
        margin-top: 20px;
    }

    .caption {
        text-align: center;
        color: #b8b9c4;
        font-size: 17px;
        margin-bottom: 40px;
    }

    .chat-container {
        max-width: 900px;
        margin: auto;
        padding-top: 10px;
    }

    .message {
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 14px;
        line-height: 1.6;
        font-size: 16px;
        white-space: pre-wrap;
    }

    .user {
        background-color: #2b2f3a;
    }

    .assistant {
        background-color: #1c1f29;
    }

    textarea {
        background: #2b2f3a !important;
        border: 1px solid #3a3f4d !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-size: 16px !important;
    }

    textarea:focus {
        outline: none !important;
        border: 1px solid #6b7280 !important;
    }

    div[data-baseweb="select"] > div {
        background: #2b2f3a !important;
        border: 1px solid #3a3f4d !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }

    button {
        background: #dbeafe !important;   /* soft light blue */
        color: #000000 !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        padding: 10px 22px !important;
        margin-top: 6px !important;
    }

    .sidebar-title {
        font-weight: 600;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- SIDEBAR: CHATS ----------
st.sidebar.markdown("<div class='sidebar-title'>Chats</div>", unsafe_allow_html=True)
search = st.sidebar.text_input("Search chats")

for chat_name in st.session_state.chats:
    if search.lower() in chat_name.lower():
        if st.sidebar.button(chat_name):
            st.session_state.current_chat = chat_name

if st.sidebar.button("+ New Chat"):
    st.session_state.chat_count += 1
    new_name = f"Chat {st.session_state.chat_count}"
    st.session_state.chats[new_name] = []
    st.session_state.current_chat = new_name

# ---------- HEADER ----------
st.markdown("<div class='title'>🧠 Understand Easily</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='caption'>A calm space to ask questions, understand concepts, and remember them for exams.</div>",
    unsafe_allow_html=True
)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

chat = st.session_state.chats[st.session_state.current_chat]

# ---------- SHOW CHAT HISTORY ----------
for msg in chat:
    cls = "user" if msg["role"] == "user" else "assistant"
    st.markdown(
        f"<div class='message {cls}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------- INPUT AREA (NO FORM) ----------
user_input = st.text_area(
    "",
    placeholder="Ask a concept or follow-up question…",
    height=80,
    key="chat_input"
)

level = st.selectbox(
    "Level",
    ["School Student", "College Student", "Beginner", "Advanced"],
    key="level_select"
)

explain_clicked = st.button("Explain")

# ---------- HANDLE SEND ----------
if explain_clicked and user_input.strip():
    # Append user message
    chat.append({"role": "user", "content": user_input})

    with st.spinner("Explaining carefully…"):
        try:
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={
                    "concept": user_input,
                    "level": level,
                    "previous_context": chat[-2]["content"] if len(chat) > 1 else ""
                },
                timeout=60
            )
            if response.status_code == 200:
                reply = response.json().get("output", "")
            else:
                reply = f"Something went wrong (status {response.status_code})."
        except Exception as e:
            reply = f"Request failed: {e}"

    chat.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ---------- JS: ENTER = EXPLAIN, SHIFT+ENTER = NEW LINE ----------
st.markdown(
    """
    <script>
    const textareas = parent.document.querySelectorAll("textarea");
    if (textareas.length > 0) {
        const ta = textareas[textareas.length - 1];  // last textarea (chat input)
        ta.addEventListener("keydown", function(e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                const buttons = parent.document.querySelectorAll("button");
                buttons.forEach(btn => {
                    if (btn.innerText.trim() === "Explain") {
                        btn.click();
                    }
                });
            }
        });
    }
    </script>
    """,
    unsafe_allow_html=True
)
