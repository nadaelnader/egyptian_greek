import streamlit as st

from retrieve import build_context, is_comparison_question, find_characters
from model import ask_model

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="MythosAI",
    page_icon="🏛️",
    layout="wide",
)

# -------------------------
# Decorative Greek + Hieroglyph symbols (faint overlay)
# -------------------------
DECORATIVE_SYMBOLS = "𓆣 Ω 𓋹 Δ 𓅓 Θ 𓂀 Λ 𓊪 Σ 𓆓 Φ 𓏏 Ψ 𓎛 Ξ"

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            radial-gradient(circle at 15% 20%, rgba(184, 140, 60, 0.25), transparent 45%),
            radial-gradient(circle at 85% 30%, rgba(120, 150, 180, 0.20), transparent 45%),
            linear-gradient(135deg, #1a1410 0%, #241c14 30%, #1c2128 65%, #10151c 100%);
        background-attachment: fixed;
    }}

    .deco-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
        color: rgba(230, 210, 170, 0.10);
        font-size: 3.2rem;
        line-height: 4.5rem;
        letter-spacing: 1.2rem;
        word-spacing: 2rem;
        white-space: pre-wrap;
        padding: 40px;
        font-family: "Noto Sans", "Segoe UI Historic", sans-serif;
    }}

    .block-container {{
        position: relative;
        z-index: 1;
    }}

    h1 {{
        font-family: "Georgia", "Times New Roman", serif !important;
        color: #e8d5a8 !important;
        text-shadow: 0 0 14px rgba(0, 0, 0, 0.65);
        font-size: 3.4rem !important;
        font-weight: 800 !important;
        letter-spacing: 1px;
        text-align: center !important;
    }}

    .tagline {{
        text-align: center;
        color: #ffffff;
        font-family: "Georgia", "Times New Roman", serif;
        font-size: 1.15rem;
        font-style: italic;
        letter-spacing: 0.5px;
        margin-top: -10px;
        margin-bottom: 25px;
        text-shadow:
            0 0 8px rgba(255, 255, 255, 0.75),
            0 0 18px rgba(255, 255, 255, 0.45),
            0 0 30px rgba(212, 175, 90, 0.65),
            0 0 45px rgba(184, 140, 60, 0.45);
    }}

    h2, h3 {{
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
        text-align: center;
    }}

    .stTextInput label {{
        display: flex !important;
        justify-content: center !important;
        width: 100%;
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

    section[data-testid="stSidebar"] {{
        background: rgba(10, 10, 12, 0.85);
        border-right: 1px solid rgba(184, 140, 60, 0.3);
    }}

    section[data-testid="stSidebar"] h2 {{
        font-size: 1.3rem !important;
        text-align: left !important;
    }}
    </style>

    <div class="deco-overlay">{(DECORATIVE_SYMBOLS + "&nbsp;&nbsp;&nbsp;") * 20}</div>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Session state: question history
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of past questions (most recent first)

if "active_question" not in st.session_state:
    st.session_state.active_question = ""

# -------------------------
# Sidebar: question history
# -------------------------
with st.sidebar:
    st.header("🕘 Question History")

    if not st.session_state.history:
        st.caption("No questions asked yet.")
    else:
        for i, past_question in enumerate(st.session_state.history):
            if st.button(past_question, key=f"history_{i}"):
                st.session_state.active_question = past_question

        if st.button("🗑️ Clear history"):
            st.session_state.history = []
            st.session_state.active_question = ""
            st.rerun()

# -------------------------
# UI (العنوان وحقل الكتابة في المنتصف)
# -------------------------
left, center, right = st.columns([1, 2, 1])

with center:
    st.title("MythosAI")
    st.markdown(
        '<div class="tagline">Where Ancient Legends Meet Artificial Intelligence</div>',
        unsafe_allow_html=True,
    )
    question = st.text_input(
        "Ask me about what you need to know:",
        value=st.session_state.active_question,
    )

# -------------------------
# Generate Answer
# -------------------------
if question:

    if question not in st.session_state.history:
        st.session_state.history.insert(0, question)
        st.session_state.history = st.session_state.history[:50]  

    with st.spinner("Please wait..."):
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
