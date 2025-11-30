import streamlit as st
import requests

# ================= CONFIG =================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
# ==========================================

st.set_page_config(
    page_title="Understand Easily",
    page_icon="📘",
    layout="wide"
)

# ---------- CUSTOM CSS (FROM YOUR HTML) ----------
st.markdown(
    """
    <style>
    body {
        margin: 0;
        background-color: #0d0f16;
        font-family: Arial, sans-serif;
        color: #ffffff;
    }

    .stApp {
        background-color: #0d0f16;
    }

    h1 {
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 10px;
        text-align: center;
    }

    .subtitle {
        font-size: 18px;
        color: #b8b9c4;
        margin-bottom: 60px;
        text-align: center;
    }

    /* Layout container */
    .container {
        max-width: 1200px;
        margin: auto;
        padding-top: 60px;
    }

    /* Textarea */
    textarea {
        background: #2b2f3a !important;
        border: 1px solid #3a3f4d !important;
        color: #ffffff !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        height: 80px !important;
    }

    textarea:focus {
        outline: none !important;
        border: 1px solid #6b7280 !important;
    }

    /* Select box */
    div[data-baseweb="select"] > div {
        background: #2b2f3a !important;
        border: 1px solid #3a3f4d !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-size: 16px !important;
    }

    /* Button */
    button[kind="primary"] {
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        padding: 12px 30px !important;
        border: none !important;
        margin-top: 20px !important;
    }

    button[kind="primary"]:hover {
        opacity: 0.8 !important;
    }

    footer {
        margin-top: 80px;
        color: #a5a6b1;
        font-size: 14px;
        text-align: center;
        margin-bottom: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- CONTENT ----------
st.markdown('<div class="container">', unsafe_allow_html=True)

st.markdown("<h1>Understand Easily</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Clear explanations — from child-level intuition to exam-ready understanding</p>",
    unsafe_allow_html=True
)

# ---------- INPUT ROW ----------
col1, col2 = st.columns([3, 1])

with col1:
    concept = st.text_area(
        "",
        placeholder="e.g. Probability, Deadlock, Ohm's Law"
    )

with col2:
    level = st.selectbox(
        "",
        ["School Student", "College Student", "Beginner", "Advanced"]
    )

# ---------- ACTION ----------
if st.button("Explain"):
    if concept.strip() == "":
        st.warning("Please enter a concept.")
    else:
        with st.spinner("Explaining clearly..."):
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={
                    "concept": concept,
                    "level": level
                },
                timeout=60
            )

        if response.status_code == 200:
            data = response.json()
            explanation = data.get("output", "")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(explanation)
        else:
            st.error(f"Error {response.status_code}")

# ---------- FOOTER ----------
st.markdown("<footer>Built to understand, not memorise.</footer>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

