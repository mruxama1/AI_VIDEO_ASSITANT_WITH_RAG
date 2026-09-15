import streamlit as st
from main import run_pipeline
from core.rag_engine import ask_question

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="centered",
)

# ---------- Styling (clean chat-style look) ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAF9F6;
    }
    .main-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #ECEAE4;
    }
    .main-card h4 {
        margin-top: 0;
        color: #3D3929;
    }
    .stChatMessage {
        border-radius: 14px;
    }
    div.stButton > button {
        border-radius: 10px;
        padding: 0.5rem 1.25rem;
        background-color: #C15F3C;
        color: white;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #A94F30;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 AI Video Assistant")
st.caption("Paste a YouTube link or upload a file, and chat with your video.")

if "result" not in st.session_state:
    st.session_state.result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- Input ----------
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    source_type = st.radio("Source", ["YouTube URL", "Upload file"], horizontal=True)

    source = None
    if source_type == "YouTube URL":
        source = st.text_input("Paste YouTube URL")
    else:
        uploaded_file = st.file_uploader("Upload audio/video file")
        if uploaded_file is not None:
            temp_path = f"uploaded_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            source = temp_path

    run_clicked = st.button("Process")
    st.markdown("</div>", unsafe_allow_html=True)

if run_clicked and source:
    with st.spinner("Processing video — this can take a few minutes..."):
        st.session_state.result = run_pipeline(source)
        st.session_state.chat_history = []

# ---------- Results ----------
result = st.session_state.result

if result:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"#### 📌 {result['title']}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("#### 📋 Summary")
    st.write(result["summary"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("#### ✅ Action Items")
    st.write(result["action_items"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("#### 🔑 Key Decisions")
    st.write(result["key_decisions"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("#### ❓ Open Questions")
    st.write(result["open_questions"])
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("📄 Full Transcript"):
        st.write(result["transcript"])

    # ---------- Chat ----------
    st.markdown("#### 💬 Chat with your video")

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(msg)

    question = st.chat_input("Ask something about the video...")
    if question:
        st.session_state.chat_history.append(("user", question))
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_question(result["rag_chain"], question)
                st.write(answer)
        st.session_state.chat_history.append(("assistant", answer))
