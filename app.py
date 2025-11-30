import streamlit as st
import requests

# ===== CONFIG =====
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
# ==================

st.set_page_config(page_title="Explain It Like I'm 5", layout="centered")

st.title("🧠 Explain It Like I'm 5")
st.write("An AI agent that explains concepts clearly at different levels.")

concept = st.text_area(
    "Enter a concept:",
    placeholder="e.g. Deadlock in operating systems",
    height=120
)

if st.button("Explain"):
    if concept.strip() == "":
        st.warning("Please enter a concept.")
    else:
        with st.spinner("Thinking..."):
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={"concept": concept},
                timeout=60
            )

        if response.status_code == 200:
            st.markdown("### 📘 Explanation")
            st.markdown(response.text)
        else:
            st.error("Something went wrong. Please try again later.")
