from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MERN Dev Assistant",
    page_icon="🟢",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;700;800&display=swap');

/* Root theme */
:root {
    --bg: #0d1117;
    --surface: #161b22;
    --border: #21262d;
    --green: #3fb950;
    --green-dim: #1a3a22;
    --blue: #58a6ff;
    --text: #e6edf3;
    --muted: #8b949e;
    --user-bg: #1c2128;
    --ai-bg: #0f1e14;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* App wrapper */
[data-testid="stAppViewContainer"] > .main {
    padding-top: 0 !important;
}

/* ── Header ── */
.header {
    background: linear-gradient(135deg, #0f1e14 0%, #0d1117 60%);
    border-bottom: 1px solid var(--border);
    padding: 1.4rem 2rem 1.2rem;
    margin: -1rem -1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.header-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.header-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.02em;
}
.header-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--green);
    margin-top: 1px;
}
.header-badge {
    margin-left: auto;
    background: var(--green-dim);
    border: 1px solid var(--green);
    color: var(--green);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.05em;
}

/* ── Chat messages ── */
.msg-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1.1rem;
    animation: fadeUp 0.25s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 34px; height: 34px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-top: 2px;
}
.avatar.ai  { background: var(--green-dim); border: 1px solid var(--green); color: var(--green); }
.avatar.usr { background: #1c2a3a; border: 1px solid var(--blue); color: var(--blue); }

.bubble {
    max-width: 78%;
    padding: 0.75rem 1rem;
    border-radius: 12px;
    font-size: 0.88rem;
    line-height: 1.65;
    white-space: pre-wrap;
    word-break: break-word;
}
.bubble.ai  {
    background: var(--ai-bg);
    border: 1px solid #1a3a22;
    color: var(--text);
    border-top-left-radius: 2px;
}
.bubble.usr {
    background: var(--user-bg);
    border: 1px solid #1c2a3a;
    color: var(--text);
    border-top-right-radius: 2px;
    text-align: left;
}
.bubble code {
    background: #0d1117;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 5px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8em;
    color: var(--green);
}

/* ── Divider / timestamp ── */
.ts {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: var(--muted);
    margin: 0.5rem 0 1rem;
}

/* ── Input area ── */
[data-testid="stChatInput"] {
    border-top: 1px solid var(--border) !important;
    background: var(--surface) !important;
    border-radius: 12px !important;
    padding: 0.4rem !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    border: none !important;
    outline: none !important;
}
[data-testid="stChatInput"] button {
    background: var(--green) !important;
    border-radius: 8px !important;
}

/* Streamlit sidebar/columns */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* Button */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    border-radius: 6px !important;
    padding: 0.3rem 0.8rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: var(--green) !important;
    color: var(--green) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
  <div class="header-dot"></div>
  <div>
    <div class="header-title">MERN Dev Assistant</div>
    <div class="header-sub">mistral-small-2506 · Senior Engineer Mode</div>
  </div>
  <div class="header-badge">ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=(
            "You are a senior MERN Stack Developer with 10+ years of experience. "
            "You provide expert guidance on MongoDB, Express.js, React, and Node.js. "
            "Give practical, production-ready code examples. Be concise but thorough. "
            "Format code blocks properly and explain your reasoning."
        ))
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # list of {"role": "user"|"ai", "content": str}

# ── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506")

model = get_model()

# ── Render existing chat ───────────────────────────────────────────────────────
if not st.session_state.chat_history:
    st.markdown('<div class="ts">Start chatting — ask anything about MongoDB, Express, React, or Node.js</div>', unsafe_allow_html=True)

for entry in st.session_state.chat_history:
    if entry["role"] == "user":
        st.markdown(f"""
        <div class="msg-row user">
          <div class="avatar usr">you</div>
          <div class="bubble usr">{entry["content"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-row">
          <div class="avatar ai">M</div>
          <div class="bubble ai">{entry["content"]}</div>
        </div>""", unsafe_allow_html=True)

# ── Clear button ──────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([4, 1, 1])
with col3:
    if st.button("clear chat"):
        st.session_state.chat_history = []
        st.session_state.messages = [st.session_state.messages[0]]  # keep system msg
        st.rerun()

# ── Chat input ────────────────────────────────────────────────────────────────
prompt = st.chat_input("Ask about MongoDB, Express, React, Node.js…")

if prompt:
    # Show user message
    st.markdown(f"""
    <div class="msg-row user">
      <div class="avatar usr">you</div>
      <div class="bubble usr">{prompt}</div>
    </div>""", unsafe_allow_html=True)

    # Append to LangChain message list
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Stream response
    with st.spinner(""):
        response = model.invoke(st.session_state.messages)
        reply = response.content

    # Fix: use actual content, not string literal
    st.session_state.messages.append(AIMessage(content=reply))
    st.session_state.chat_history.append({"role": "ai", "content": reply})

    # Show AI message
    st.markdown(f"""
    <div class="msg-row">
      <div class="avatar ai">M</div>
      <div class="bubble ai">{reply}</div>
    </div>""", unsafe_allow_html=True)