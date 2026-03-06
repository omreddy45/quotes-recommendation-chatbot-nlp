"""
Modern Light Theme - Quotes Recommendation Chatbot
Connects to Rasa REST API backend
Favorites stored in SQLite database per user
"""

import streamlit as st
import requests
import sqlite3
import hashlib
from datetime import datetime
from typing import Optional, List

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Quote Bot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #f8f7f4 !important;
    font-family: 'DM Sans', sans-serif;
    color: #1a1a1a;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }
[data-testid="collapsedControl"] { display: none !important; }

/* ── Top bar ── */
.top-bar {
    display: flex;
    align-items: center;
    padding: 14px 20px 10px;
    border-bottom: 1px solid #e8e4dd;
    background: #ffffff;
}
.bot-identity { display: flex; align-items: center; gap: 10px; }
.bot-avatar {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #2d6a4f, #52b788);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
}
.bot-name { font-size: 15px; font-weight: 600; color: #1a1a1a; line-height: 1.1; }
.bot-tagline { font-size: 11px; color: #888; font-weight: 400; }
.online-dot {
    width: 8px; height: 8px;
    background: #52b788; border-radius: 50%;
    display: inline-block; margin-right: 4px;
}

/* ── Chat wrapper with border ── */
.chat-wrapper {
    border: 1.5px solid #e0dbd3;
    border-radius: 16px;
    background: #ffffff;
    margin: 16px 0 12px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

/* ── Chat scroll area ── */
.chat-scroll {
    max-height: 58vh;
    min-height: 200px;
    overflow-y: auto;
    padding: 20px 16px 12px;
    background: #f8f7f4;
}
.chat-scroll::-webkit-scrollbar { width: 4px; }
.chat-scroll::-webkit-scrollbar-thumb { background: #d4cfc8; border-radius: 4px; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #aaa;
}
.empty-icon { font-size: 44px; margin-bottom: 12px; }
.empty-title { font-size: 15px; font-weight: 500; color: #888; }
.empty-hint { font-size: 12px; color: #bbb; margin-top: 6px; }

/* ── Message rows ── */
.msg-row { display: flex; margin-bottom: 4px; align-items: flex-end; gap: 8px; }
.msg-row.user { justify-content: flex-end; }
.msg-row.bot  { justify-content: flex-start; }

/* ── Bot icon beside message ── */
.bot-icon {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #2d6a4f, #52b788);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
    margin-bottom: 2px;
}

/* ── Bubbles ── */
.bubble {
    max-width: 70%;
    padding: 11px 15px;
    border-radius: 18px;
    font-size: 14px;
    line-height: 1.55;
    word-break: break-word;
}
.bubble.user {
    background: #2d6a4f;
    color: #ffffff;
    border-bottom-right-radius: 4px;
}
.bubble.bot {
    background: #ffffff;
    color: #1a1a1a;
    border-bottom-left-radius: 4px;
    border: 1px solid #ece8e1;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

/* ── Quote card inside bot bubble ── */
.quote-card {
    background: #fdfaf6;
    border-left: 3px solid #52b788;
    border-radius: 0 10px 10px 0;
    padding: 12px 14px;
    margin-top: 6px;
    font-family: 'Lora', Georgia, serif;
    font-size: 14px;
    font-style: italic;
    color: #2c2c2c;
    line-height: 1.7;
}
.quote-author {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-style: normal;
    font-weight: 600;
    color: #888;
    margin-top: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Timestamp ── */
.ts {
    font-size: 10px;
    color: #bbb;
    text-align: center;
    margin: 6px 0 2px;
}

/* ── Typing indicator ── */
.typing-indicator {
    display: flex;
    align-items: flex-end;
    gap: 8px;
    margin-bottom: 8px;
    padding: 4px 0;
}
.typing-bubble {
    background: #ffffff;
    border: 1px solid #ece8e1;
    border-radius: 18px;
    border-bottom-left-radius: 4px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 5px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.typing-dot {
    width: 7px; height: 7px;
    background: #52b788;
    border-radius: 50%;
    animation: typingBounce 1.2s infinite ease-in-out;
}
.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-6px); opacity: 1; }
}

/* ── Input bar ── */
.input-bar-wrapper {
    background: #ffffff;
    border-top: 1px solid #e8e4dd;
    padding: 12px 16px;
    border-radius: 0 0 14px 14px;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input {
    border-radius: 24px !important;
    border: 1.5px solid #e0dbd3 !important;
    background: #fafaf8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 18px !important;
    color: #1a1a1a !important;
    box-shadow: none !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #52b788 !important;
    background: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(82,183,136,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: #b0aa9e !important; }

/* Send button */
.stButton > button {
    border-radius: 24px !important;
    background: #2d6a4f !important;
    color: #fff !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: background 0.2s, transform 0.1s !important;
    letter-spacing: 0.2px;
    width: 100%;
}
.stButton > button:hover {
    background: #1b4332 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Small action / category buttons */
.small-btn > button {
    border-radius: 20px !important;
    background: #f3f0eb !important;
    color: #444 !important;
    border: 1px solid #e0dbd3 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 6px 12px !important;
    height: auto !important;
    min-height: unset !important;
    width: auto !important;
}
.small-btn > button:hover {
    background: #e8e3db !important;
    border-color: #52b788 !important;
    color: #2d6a4f !important;
}

/* Favourites panel */
.fav-panel {
    background: #ffffff;
    border-radius: 14px;
    border: 1px solid #e8e4dd;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.fav-header {
    font-size: 14px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 12px;
}
.fav-item {
    background: #fdfaf6;
    border: 1px solid #ece8e1;
    border-left: 3px solid #52b788;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 8px;
    font-family: 'Lora', serif;
    font-size: 13px;
    font-style: italic;
    color: #333;
    line-height: 1.5;
}
.fav-empty {
    text-align: center;
    color: #bbb;
    font-size: 13px;
    padding: 20px 0;
}

.stSpinner > div { border-top-color: #52b788 !important; }
.block-container { padding: 0 !important; max-width: 720px !important; }
hr { border: none; border-top: 1px solid #e8e4dd; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONSTANTS
# ============================================================================
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
QUOTE_CATEGORIES = ["Motivation", "Inspiration", "Love", "Success", "Funny", "Life", "Happiness", "Wisdom"]

# ============================================================================
# SESSION STATE
# ============================================================================
for key, default in [
    ("chat_history", []),
    ("favorites", []),
    ("show_favorites", False),
    ("liked_idx", set()),
    ("input_key", 0),
    ("thinking", False),
    ("user_id", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ============================================================================
# DATABASE SETUP
# ============================================================================
DB_PATH = "quotes_app.db"

def init_db():
    """Initialize SQLite database for storing user favorites."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            quote TEXT NOT NULL UNIQUE,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_user_id() -> str:
    """Generate or retrieve persistent user ID from browser."""
    if st.session_state.user_id is None:
        # Create a deterministic user ID based on browser/session
        # In a real app, you'd use proper authentication
        user_hash = hashlib.md5(
            f"{st.session_state}_quotes_bot".encode()
        ).hexdigest()[:12]
        st.session_state.user_id = user_hash
    return st.session_state.user_id

def add_favorite(quote: str) -> bool:
    """Add a quote to user's favorites in database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        user_id = get_user_id()
        cursor.execute(
            "INSERT INTO user_favorites (user_id, quote) VALUES (?, ?)",
            (user_id, quote)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Quote already in favorites
        return False
    except Exception as e:
        st.error(f"Error saving favorite: {e}")
        return False

def remove_favorite(quote: str) -> bool:
    """Remove a quote from user's favorites."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        user_id = get_user_id()
        cursor.execute(
            "DELETE FROM user_favorites WHERE user_id = ? AND quote = ?",
            (user_id, quote)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error removing favorite: {e}")
        return False

def get_favorites() -> List[str]:
    """Retrieve all favorite quotes for the current user from database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        user_id = get_user_id()
        cursor.execute(
            "SELECT quote FROM user_favorites WHERE user_id = ? ORDER BY added_at DESC",
            (user_id,)
        )
        favorites = [row[0] for row in cursor.fetchall()]
        conn.close()
        return favorites
    except Exception as e:
        st.error(f"Error loading favorites: {e}")
        return []

def is_favorite(quote: str) -> bool:
    """Check if a quote is already in user's favorites."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        user_id = get_user_id()
        cursor.execute(
            "SELECT 1 FROM user_favorites WHERE user_id = ? AND quote = ?",
            (user_id, quote)
        )
        result = cursor.fetchone() is not None
        conn.close()
        return result
    except Exception as e:
        return False

# Initialize database on app startup
init_db()
st.session_state.favorites = get_favorites()

# ============================================================================
# HELPERS
# ============================================================================
def send_to_rasa(msg: str) -> Optional[str]:
    try:
        r = requests.post(RASA_API_URL, json={"sender": "user", "message": msg}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data:
                return data[0].get("text", "")
        return None
    except requests.exceptions.ConnectionError:
        return "❌ Can't reach the bot server. Is Rasa running?"
    except Exception as e:
        return f"❌ Error: {e}"

def is_quote(text: str) -> bool:
    """Only true if the message actually contains a quoted string."""
    return '"' in text and len(text) > 20

def push_user(msg: str):
    st.session_state.chat_history.append({
        "role": "user", "content": msg,
        "ts": datetime.now().strftime("%H:%M")
    })

def push_bot(msg: str, category: str = "", is_quote_msg: bool = False):
    st.session_state.chat_history.append({
        "role": "bot", "content": msg, "category": category,
        "is_quote": is_quote_msg,
        "ts": datetime.now().strftime("%H:%M")
    })

def handle_send(msg: str, category: str = ""):
    if not msg.strip():
        return
    push_user(msg)
    resp = send_to_rasa(msg)
    if resp:
        push_bot(resp, category, is_quote_msg=is_quote(resp))
    st.session_state.thinking = False
    st.session_state.input_key += 1   # resets text input to blank
    st.rerun()

# ============================================================================
# TOP BAR
# ============================================================================
col_left, col_right = st.columns([0.72, 0.28])
with col_left:
    st.markdown("""
    <div class="top-bar">
        <div class="bot-identity">
            <div class="bot-avatar">💬</div>
            <div>
                <div class="bot-name">Quote Bot</div>
                <div class="bot-tagline"><span class="online-dot"></span>AI-powered motivational chatbot</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    fav_label = f"{'★' if st.session_state.favorites else '☆'} Favourites ({len(st.session_state.favorites)})"
    if st.button(fav_label, key="fav_toggle"):
        st.session_state.show_favorites = not st.session_state.show_favorites
        st.rerun()

# ============================================================================
# FAVOURITES PANEL
# ============================================================================
if st.session_state.show_favorites:
    st.markdown('<div class="fav-panel">', unsafe_allow_html=True)
    st.markdown('<div class="fav-header">★ Favourite Quotes</div>', unsafe_allow_html=True)
    if st.session_state.favorites:
        for i, q in enumerate(st.session_state.favorites):
            fc1, fc2 = st.columns([0.9, 0.1])
            with fc1:
                st.markdown(f'<div class="fav-item">{q}</div>', unsafe_allow_html=True)
            with fc2:
                st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                if st.button("✕", key=f"delfav_{i}"):
                    if remove_favorite(q):
                        st.session_state.favorites = get_favorites()
                        st.toast("❌ Removed from favourites", icon="✅")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="fav-empty">No favourites yet — heart a quote to save it here!</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================================
# CHAT SECTION  (bordered wrapper contains scroll + input bar)
# ============================================================================
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="chat-scroll" id="chat-scroll">', unsafe_allow_html=True)

if not st.session_state.chat_history and not st.session_state.thinking:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">💭</div>
        <div class="empty-title">Start a conversation!</div>
        <div class="empty-hint">Type a message below or ask for a quote by category.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    prev_ts = None
    for idx, msg in enumerate(st.session_state.chat_history):
        if msg["ts"] != prev_ts:
            st.markdown(f'<div class="ts">{msg["ts"]}</div>', unsafe_allow_html=True)
            prev_ts = msg["ts"]

        if msg["role"] == "user":
            st.markdown(
                f'<div class="msg-row user"><div class="bubble user">{msg["content"]}</div></div>',
                unsafe_allow_html=True
            )
        else:
            content = msg["content"]

            # Parse quote vs plain text
            quote_part = ""
            text_part = content
            if '"' in content:
                start = content.find('"')
                end = content.rfind('"')
                if end > start:
                    quote_part = content[start:end+1]
                    text_part = content[:start].strip()
                    remainder = content[end+1:].strip()
                    if remainder:
                        text_part = (text_part + " " + remainder).strip()

            # Extract author
            author_line = ""
            if quote_part:
                for sep in ["—", " - "]:
                    if sep in quote_part:
                        parts = quote_part.split(sep)
                        if len(parts) >= 2:
                            author_line = parts[-1].strip().strip('"')
                            quote_part = sep.join(parts[:-1]).strip()
                            break

            bubble_inner = ""
            if text_part:
                bubble_inner += f'<div>{text_part}</div>'
            if quote_part:
                bubble_inner += f'<div class="quote-card">{quote_part}'
                if author_line:
                    bubble_inner += f'<div class="quote-author">— {author_line}</div>'
                bubble_inner += '</div>'

            st.markdown(
                f'<div class="msg-row bot">'
                f'<div class="bot-icon">🤖</div>'
                f'<div class="bubble bot">{bubble_inner}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            # ❤️ 👍 👎 only for actual quote messages
            if msg.get("is_quote", False):
                a1, a2, a3, _sp = st.columns([0.1, 0.1, 0.1, 0.7])
                with a1:
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("❤️", key=f"heart_{idx}", help="Save to favourites"):
                        if add_favorite(content):
                            st.session_state.favorites = get_favorites()
                            st.toast("❤️ Added to favourites!", icon="✅")
                            st.rerun()
                        else:
                            st.toast("Already in favourites!", icon="ℹ️")
                    st.markdown('</div>', unsafe_allow_html=True)
                with a2:
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("👍", key=f"like_{idx}", help="Liked this"):
                        if idx not in st.session_state.liked_idx:
                            st.session_state.liked_idx.add(idx)
                            push_bot("Glad you liked it! 😊\n\nWant a quote from another category?", is_quote_msg=False)
                            st.session_state.input_key += 1
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with a3:
                    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                    if st.button("👎", key=f"dislike_{idx}", help="Get another"):
                        cat = msg.get("category", "motivation")
                        handle_send(f"Give me another {cat.lower()} quote", cat)
                    st.markdown('</div>', unsafe_allow_html=True)

            # Category picker after 👍
            if "Want a quote from another category?" in content:
                st.markdown('<div style="margin-left:36px; margin-bottom:6px;">', unsafe_allow_html=True)
                cols = st.columns(4)
                for ci, cat in enumerate(QUOTE_CATEGORIES):
                    with cols[ci % 4]:
                        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                        if st.button(cat, key=f"catbtn_{idx}_{ci}"):
                            handle_send(f"Give me a {cat.lower()} quote", cat)
                        st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # Thinking / typing indicator
    if st.session_state.thinking:
        st.markdown("""
        <div class="typing-indicator">
            <div class="bot-icon">🤖</div>
            <div class="typing-bubble">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # end chat-scroll

# ── Input bar sits inside the bordered wrapper ──
st.markdown('<div class="input-bar-wrapper">', unsafe_allow_html=True)
in1, in2 = st.columns([0.83, 0.17])
with in1:
    user_input = st.text_input(
        "msg",
        placeholder="Type a message or ask for a quote…",
        label_visibility="collapsed",
        key=f"user_input_{st.session_state.input_key}",
    )
with in2:
    send_clicked = st.button("Send →", key="send_btn")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # end chat-wrapper

# ============================================================================
# SEND LOGIC — handles both button click AND Enter key
# ============================================================================
if (send_clicked or user_input.strip()) and user_input.strip():
    st.session_state.thinking = True
    handle_send(user_input.strip())

# Auto-scroll
st.markdown("""
<script>
setTimeout(function() {
    const el = document.getElementById('chat-scroll');
    if (el) el.scrollTop = el.scrollHeight;
}, 120);
</script>
""", unsafe_allow_html=True)