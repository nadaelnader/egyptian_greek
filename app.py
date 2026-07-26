import base64
from pathlib import Path

import streamlit as st

from retrieve import build_context, is_comparison_question, find_characters
from model import ask_model

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Egyptian & Greek Mythology AI",
    page_icon="🏛️",
    layout="wide",
)

# -------------------------
# Background image (base64)
# -------------------------
BACKGROUND_FILE = "background.jpg"  # غيّر الاسم هنا لو رفعت الصورة باسم مختلف (مثلاً background.png)


@st.cache_data
def get_base64_image(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    return base64.b64encode(file_path.read_bytes()).decode()


bg_base64 = get_base64_image(BACKGROUND_FILE)

if bg_base64:
    ext = BACKGROUND_FILE.split(".")[-1]
    background_css = f"""
    .stApp {{
        background-image:
            linear-gradient(135deg, rgba(20, 15, 10, 0.82), rgba(15, 20, 28, 0.85)),
            url("data:image/{ext};base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    """
else:
    # fallback: لو الصورة مش موجودة، استخدم نفس الجراديانت القديم
    background_css = """
    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(184, 140, 60, 0.25), transparent 45%),
            radial-gradient(circle at 85% 30%, rgba(120, 150, 180, 0.20), transparent 45%),
            linear-gradient(135deg, #1a1410 0%, #241c14 30%, #1c2128 65%, #10151c 100%);
        background-attachment: fixed;
    }
    """

st.markdown(
    f"""
    <style>
    {background_css}

    h1, h2, h3 {{
        font-family: "Georgia", "Times New Roman", serif !important;
        color: #e8d5a8 !important;
        text-shadow: 0 0 12px rgba(0, 0, 0, 0.6);
    }}

    p, label, .stMarkdown {{
        color: #f0ece0 !important;
    }}

    .stTextInput > div > div > input {{
        background-color: rgba(15, 13, 10, 0.8) !important;
        color: #f0e6cf !important;
        border: 1px solid #8a6d3a !important;
        border-radius: 8px !important;
    }}

    .answer-box {{
        background: rgba(10, 10, 12, 0.78);
        border: 1px solid rgba(184, 140, 60, 0.55);
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.4);
        margin-top: 10px;
        margin-bottom: 20px;
    }}

    .character-box {{
        background: rgba(10, 10, 12, 0.8);
        border: 1px solid rgba(150, 170, 190, 0.4);
        border-radius: 12px;
        padding: 18px 20px;
        height: 100%;
    }}

    .character-box h4 {{
        color: #d8c48a !important;
        border-bottom: 1px solid rgba(184, 140, 60, 0.4);
        padding-bottom: 6px;
        margin-bottom: 10px;
    }}

    div[data-testid="stExpander"] {{
        background: rgba(10, 10, 12, 0.65);
        border: 1px solid rgba(150, 170, 190, 0.3);
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
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
                comparison_mode = (
                    is_comparison_question(question)
                    and len(find_characters(question)) >= 2
                )

                if comparison_mode:
                    characters = find_characters(question)[:2]
                    cols = st.columns(len(characters))

                    for col, doc in zip(cols, characters):
                        with col:
                            with st.spinner(f"Looking up {doc['title']}..."):
                                per_char_answer, _ = ask_model(
                                    f"Tell me about {doc['title']}"
                                )
                            st.markdown(
                                f"""<div class="character-box">
                                <h4>{doc['title']}</h4>
                                {per_char_answer}
                                </div>""",
                                unsafe_allow_html=True,
                            )
                else:
                    answer, sources = ask_model(question)
                    st.subheader("Answer")
                    st.markdown(
                        f'<div class="answer-box">{answer}</div>',
                        unsafe_allow_html=True,
                    )

                with st.expander("Retrieved Sources"):
                    for doc in sources:
                        st.markdown(f"**{doc['title']}**")

        except Exception as e:
            st.error(f"Error: {e}")
