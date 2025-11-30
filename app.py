import streamlit as st
import requests

# ================= CONFIG =================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
# ==========================================

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Explain It Like I'm 5",
    page_icon="🧠",
    layout="wide"
)

# ---------- GLOBAL UI STYLES (GREY ONLY) ----------
st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background-color: #0f172a;
        color: #e5e7eb;
    }

    /* General text */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #e5e7eb !important;
    }

    /* Textarea + input */
    textarea, input {
        background-color: #1f2933 !important;
        color: #e5e7eb !important;
        border-radius: 8px !important;
        border: 1px solid #6b7280 !important;
    }

    textarea:focus, input:focus {
        outline: none !important;
        border: 1px solid #9ca3af !important;
        box-shadow: 0 0 4px rgba(156, 163, 175, 0.4) !important;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #1f2933 !important;
        border-radius: 8px !important;
        border: 1px solid #6b7280 !important;
        color: #e5e7eb !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border: 1px solid #9ca3af !important;
        box-shadow: 0 0 4px rgba(156, 163, 175, 0.4) !important;
    }

    /* Dropdown menu */
    ul[role="listbox"] {
        background-color: #111827 !important;
        border: 1px solid #374151 !important;
    }

    li {
        color: #e5e7eb !important;
    }

    li:hover {
        background-color: #1f2933 !important;
    }

    /* Button */
    button[kind="primary"] {
        background-color: #1f2933 !important;
        color: #e5e7eb !important;
        border: 1px solid #6b7280 !important;
        border-radius: 8px !important;
    }

    button[kind="primary"]:hover {
        background-color: #374151 !important;
        border: 1px solid #9ca3af !important;
    }

    /* Expander */
    details {
        background-color: #111827 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        padding: 4px !important;
    }

    summary {
        font-size: 1rem !important;
        color: #e5e7eb !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.markdown(
    """
    <h1 style="text-align:center;">Explain It Like I'm 5</h1>
    <p style="text-align:center; color:#9ca3af;">
    Clear explanations — from child-level intuition to exam-ready understanding
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------- INPUT SECTION ----------
col1, col2 = st.columns([2, 1])

with col1:
    concept = st.text_area(
        "Concept",
        placeholder="e.g. Probability, Deadlock, Ohm's Law",
        height=120
    )

with col2:
    level = st.selectbox(
        "Your level",
        ["School Student", "College Student", "Exam Preparation"]
    )

st.markdown("")

# ---------- ACTION ----------
if st.button("Explain"):
    if concept.strip() == "":
        st.warning("Please enter a concept.")
    else:
        with st.spinner("Thinking clearly..."):
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

            st.divider()
            st.subheader("Explanation")

            # Section-aware display
            if "Explain Like I'm 5" in explanation:
                with st.expander("Explain Like I'm 5"):
                    st.markdown(explanation)
            else:
                # fallback if agent returns plain text
                st.markdown(explanation)

        else:
            st.error(f"Error {response.status_code}")

# ---------- FOOTER ----------
st.divider()
st.markdown(
    "<p style='text-align:center; color:#6b7280;'>Built to understand, not memorise.</p>",
    unsafe_allow_html=True
)
