"""
app.py
------
Streamlit main entry point.
Handles routing between all 8 pages with session-based auth.
Run with: streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv
load_dotenv()  # Load .env before any agent imports

from database.db import init_db

# Initialise database on first run
init_db()

# ── PAGE CONFIG ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎙️ PodcastAI Platform",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── SESSION INIT ──────────────────────────────────────────────────────
if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
if "token"         not in st.session_state: st.session_state["token"]         = ""
if "user_id"       not in st.session_state: st.session_state["user_id"]       = ""
if "username"      not in st.session_state: st.session_state["username"]      = ""
if "page"          not in st.session_state: st.session_state["page"]          = "login"

# ── AUTH CHECK ────────────────────────────────────────────────────────
from auth.middleware import require_auth

if st.session_state["authenticated"]:
    if not require_auth(st.session_state):
        st.session_state["authenticated"] = False
        st.session_state["page"]          = "login"
        st.rerun()

# ── ROUTING ───────────────────────────────────────────────────────────
page    = st.session_state["page"]
user_id = st.session_state.get("user_id", "")
uname   = st.session_state.get("username", "")

# Public pages
if not st.session_state["authenticated"]:
    if page == "register":
        from pages.register import show; show()
    else:
        from pages.login import show; show()
    st.stop()

# ── AUTHENTICATED SIDEBAR ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/microphone.png", width=50)
    st.markdown(f"**{uname}** 👤")
    st.divider()

    pages = {
        "🏠 Dashboard":    "dashboard",
        "📹 Episodes":     "episodes",
        "✍️ Preferences":  "preferences",
        "🔁 Templates":    "templates",
        "📤 Export Hub":   "export_hub",
        "📊 Analytics":    "analytics",
        "🎯 Demo":         "demo",
    }

    for label, key in pages.items():
        if st.button(label, use_container_width=True,
                     type="primary" if page == key else "secondary"):
            st.session_state["page"] = key
            st.rerun()

    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        for k in ["authenticated","token","user_id","username"]:
            st.session_state[k] = "" if k != "authenticated" else False
        st.session_state["page"] = "login"
        st.rerun()

# ── PAGE DISPATCH ─────────────────────────────────────────────────────
if   page == "dashboard":   from pages.dashboard   import show; show(user_id, uname)
elif page == "episodes":    from pages.episodes    import show; show(user_id)
elif page == "preferences": from pages.preferences import show; show(user_id)
elif page == "templates":   from pages.templates   import show; show(user_id)
elif page == "export_hub":  from pages.export_hub  import show; show(user_id)
elif page == "analytics":   from pages.analytics   import show; show(user_id)
elif page == "demo":        from pages.demo        import show; show(user_id)
else:
    from pages.dashboard import show; show(user_id, uname)
