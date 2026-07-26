import streamlit as st

api_key = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(
    page_title="Egyptian & Greek Mythology AI",
    page_icon="🏛️"
)

st.title("🏛️ Egyptian & Greek Mythology AI")

question = st.text_input("Ask about ancient mythology:")

if question:
    st.write("Your answer will appear here...")
