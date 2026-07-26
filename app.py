import streamlit as st

from retrieve import build_context
from model import ask_model

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Egyptian & Greek Mythology AI",
    page_icon="🏛️"
)

# -------------------------
# UI
# -------------------------
st.title("Egyptian & Greek Mythology AI")
question = st.text_input("Ask about ancient mythology:")

# -------------------------
# Generate Answer
# -------------------------
if question:
    with st.spinner("Searching mythology database..."):
        try:
            context, sources = build_context(question)

            if not context:
                st.warning(
                    "I don't have enough information in the provided mythology database."
                )
            else:
                answer, sources = ask_model(question)

                st.subheader("Answer")
                st.markdown(answer)

                with st.expander("Retrieved Sources"):
                    for doc in sources:
                        st.markdown(f"**{doc['title']}**")
        except Exception as e:
            st.error(f"Error: {e}")
