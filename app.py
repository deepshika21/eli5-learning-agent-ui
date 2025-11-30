import streamlit as st
import requests

# ================= CONFIG =================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
# ==========================================

st.set_page_config(
    page_title="Friend for Exam",
    page_icon="📘",
    layout="centered"
)

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- CSS (CHATGPT-STYLE, DARK, CALM) ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d0f16;
        color: #ffffff;
    }

    .chat-container {
        max-width: 900px;
        margin: auto;
        padding-top: 40px;
    }

    .message {
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 16px;
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
        color: #ffffff !important;
        border: 1px solid #3a3f4d !important;
        border-radius: 8px !important;
        font-size: 16px !important;
    }

    textarea:focus {
        outline: none !important;
        border: 1px solid #6b7280 !important;
    }

    button {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        margin-top: 6px !important;
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        margin-top: 30px;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.markdown(
    "<h2 style='text-align:center;'>📘 Friend for Exam</h2>"
    "<p style='text-align:center; color:#b8b9c4;'>Ask. Understand. Remember.</p>",
    unsafe_allow_html=True
)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# ---------- CHAT HISTORY ----------
for m in st.session_state.messages:
    role_class = "user" if m["role"] == "user" else "assistant"
    st.markdown(
        f"<div class='message {role_class}'>{m['content']}</div>",
        unsafe_allow_html=True
    )

# ---------- INPUT ----------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "",
        placeholder="Ask a concept or follow-up question...",
        height=80
    )
    level = st.selectbox(
        "Level",
        ["School Student", "College Student", "Beginner", "Advanced"]
    )
    send = st.form_submit_button("Explain")

# ---------- ACTION ----------
if send and user_input.strip():
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Thinking like a good teacher…"):
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={
                "concept": user_input,
                "level": level,
                "previous_context": (
                    st.session_state.messages[-2]["content"]
                    if len(st.session_state.messages) > 1 else ""
                )
            },
            timeout=60
        )

        if response.status_code == 200:
            explanation = response.json().get("output", "")
        else:
            explanation = "Something went wrong."

    # Add assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": explanation}
    )

    st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div class='footer'>Built to understand, not memorise.</div>",
    unsafe_allow_html=True
)
