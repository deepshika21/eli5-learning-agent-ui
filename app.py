import streamlit as st
import requests

# ================= CONFIG =================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
# ==========================================


st.set_page_config(page_title="Understand Easily", layout="centered")

# ---------------------- CSS STYLING ----------------------
st.markdown("""
<style>
/* Page background */
body, .stApp {
    background-color: #0E0E0E !important;
    color: white !important;
}

/* Input container styling */
.big-box {
    background-color: #1A1A1A;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
}

/* Titles */
h3 {
    color: white !important;
}

/* Explain Button Styling */
.stButton > button {
    width: 100%;
    background-color: #4A8BFF;
    color: white;
    padding: 12px;
    border-radius: 12px;
    border: none;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #1A6DFF;
}

/* Disable typing in Selectbox */
div[data-baseweb="select"] input {
    pointer-events: none !important;
    caret-color: transparent !important;
}

/* Dropdown background dark */
div[data-baseweb="select"] {
    background-color: #1A1A1A !important;
    color: white !important;
}

/* Dropdown text color */
div[data-baseweb="select"] * {
    color: white !important;
}

/* Dropdown options menu */
ul[role="listbox"] {
    background-color: #1A1A1A !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- UI LAYOUT ----------------------
st.markdown("<h1 style='text-align:center; color:white;'>Concept Explainer</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

# ---------------------- Left Column (Concept Box) ----------------------
with col1:
    st.markdown("<div class='big-box'>", unsafe_allow_html=True)
    st.markdown("### Concept:")
    
    concept = st.text_area(
        "",
        placeholder="Eg: BFS, DFS, Unification.",
        height=200
    )

    # --------------- ENTER KEY FUNCTION ---------------
    st.markdown("""
    <script>
    document.addEventListener("keydown", function(e) {
        const ta = document.querySelector("textarea");
        if (document.activeElement === ta) {

            // Shift + Enter = allow newline
            if (e.key === "Enter" && e.shiftKey) {
                return;
            }

            // Enter = click Explain button
            if (e.key === "Enter") {
                e.preventDefault();
                const btn = window.parent.document.querySelector('button[kind="primary"]');
                if (btn) btn.click();
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- Right Column (Level Dropdown) ----------------------
with col2:
    st.markdown("<div class='big-box'>", unsafe_allow_html=True)
    st.markdown("### Your Level:")

    level = st.selectbox(
        "",
        ["School Student", "College Student", "Advanced"]
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- Explain Button ----------------------
if st.button("Explain", type="primary"):
    if concept.strip() == "":
        st.warning("Please enter a concept first!")
    else:
        st.success(f"Explaining *{concept}* for *{level}*...")
