import streamlit as st
from openai import OpenAI

from retrieve import build_context
from prompting import build_prompt, SYSTEM_PROMPT


# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Egyptian & Greek Mythology AI",
    page_icon="🏛️"
)


# -------------------------
# OpenRouter Client
# -------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)


# -------------------------
# UI
# -------------------------
st.title("🏛️ Egyptian & Greek Mythology AI")

question = st.text_input(
    "Ask about ancient mythology:"
)


# -------------------------
# Generate Answer
# -------------------------
if question:

    with st.spinner("Searching mythology database..."):

        try:

            # Retrieve context
            context, sources = build_context(question)


            if not context:

                st.warning(
                    "I don't have enough information in the provided mythology database."
                )


            else:

                # Build RAG prompt
                prompt = build_prompt(
                    question,
                    context
                )


                # Call Qwen model
                response = client.chat.completions.create(

                    model="qwen/qwen-2.5-7b-instruct",

                    messages=[

                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },

                        {
                            "role": "user",
                            "content": prompt
                        }

                    ],

                    temperature=0,
                    top_p=0.1,
                )


                answer = response.choices[0].message.content


                # Display Answer
                st.subheader("Answer")

                st.markdown(answer)


                # Display Sources
                with st.expander("Retrieved Sources"):

                    for doc in sources:

                        st.markdown(
                            f"**{doc['title']}**"
                        )


        except Exception as e:

            st.error(
                f"Error: {e}"
            )
