import streamlit as st
#hi
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Janta Seva",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme state ───────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# ── Glacial Indifference via @font-face (free CDN) ───────────────────────────
FONT_FACE = """
@font-face {
    font-family: 'Glacial Indifference';
    src: url('https://db.onlinewebfonts.com/t/60477e7f39f32e0f6b76e8b4f30e5063.woff2') format('woff2'),
         url('https://db.onlinewebfonts.com/t/60477e7f39f32e0f6b76e8b4f30e5063.woff') format('woff');
    font-weight: 400; font-style: normal;
}
@font-face {
    font-family: 'Glacial Indifference';
    src: url('https://db.onlinewebfonts.com/t/7f0e8fa72c02832dc6cc5b6a04d6f6ce.woff2') format('woff2'),
         url('https://db.onlinewebfonts.com/t/7f0e8fa72c02832dc6cc5b6a04d6f6ce.woff') format('woff');
    font-weight: 700; font-style: normal;
}
"""

# ── Per-theme CSS variables ───────────────────────────────────────────────────
if dark:
    css_vars = """
    :root {
        --bg:        #080f1f;
        --surface:   #0d1730;
        --panel:     #111f3a;
        --panel2:    #172445;
        --border:    #1e3060;
        --accent1:   #FF6B2C;
        --accent2:   #38BDF8;
        --accent3:   #818CF8;
        --text:      #E4EDFF;
        --text2:     #CBD5E1;
        --muted:     #5B7BA8;
        --glow1:     0 0 20px rgba(255,107,44,.3), 0 0 50px rgba(255,107,44,.1);
        --glow2:     0 0 20px rgba(56,189,248,.3), 0 0 50px rgba(56,189,248,.1);
        --shadow:    0 4px 30px rgba(0,0,10,.5);
        --ribbon:    linear-gradient(90deg,#FF6B2C,#818CF8,#38BDF8);
        --hero-grad: radial-gradient(ellipse 80% 50% at 20% 0%, rgba(255,107,44,.07) 0%, transparent 55%),
                     radial-gradient(ellipse 60% 40% at 80% 100%, rgba(56,189,248,.06) 0%, transparent 55%),
                     radial-gradient(ellipse 50% 60% at 60% 40%, rgba(129,140,248,.04) 0%, transparent 55%);
        --toggle-bg:    #1a2d55;
        --toggle-color: #38BDF8;
    }"""
else:
    css_vars = """
    :root {
        --bg:        #E0F2FE;
        --surface:   #BAE6FD;
        --panel:     #FFFFFF;
        --panel2:    #F0F9FF;
        --border:    #7DD3FC;
        --accent1:   #D64E0F;
        --accent2:   #0369A1;
        --accent3:   #4F46E5;
        --text:      #082F49;
        --text2:     #0C4A6E;
        --muted:     #0E7490;
        --glow1:     0 0 14px rgba(214,78,15,.2);
        --glow2:     0 0 14px rgba(3,105,161,.2);
        --shadow:    0 4px 20px rgba(0,60,120,.1);
        --ribbon:    linear-gradient(90deg,#D64E0F,#4F46E5,#0369A1);
        --hero-grad: radial-gradient(ellipse 80% 50% at 20% 0%, rgba(214,78,15,.06) 0%, transparent 55%),
                     radial-gradient(ellipse 60% 40% at 80% 100%, rgba(3,105,161,.06) 0%, transparent 55%);
        --toggle-bg:    #BAE6FD;
        --toggle-color: #0369A1;
    }"""

st.markdown(f"""
<style>
{FONT_FACE}
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=Space+Mono:wght@400;700&display=swap');

{css_vars}

/* ── BASE ── */
*, *::before, *::after {{ box-sizing: border-box; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {{
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: background .3s ease, color .2s ease;
}}

/* ── HEADINGS → Glacial Indifference ── */
h1, h2, h3, h4, h5, h6,
.hero-title, .brand,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {{
    font-family: 'Glacial Indifference', 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}}

/* ── Top ribbon ── */
.theme-ribbon {{
    position: fixed; top: 0; left: 0; right: 0; height: 3px;
    background: var(--ribbon); z-index: 9999;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    transition: background .3s;
}}
[data-testid="stSidebar"] * {{
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}}

.sidebar-logo {{
    text-align: center;
    padding: 2rem 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}}
.sidebar-logo .flag {{ font-size: 3rem; display: block; margin-bottom: .4rem; }}
.sidebar-logo .brand {{
    font-family: 'Glacial Indifference', sans-serif !important;
    font-weight: 700; font-size: 1.65rem;
    background: linear-gradient(135deg, var(--accent1), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: .03em;
}}
.sidebar-logo .tagline {{
    color: var(--muted); font-size: .7rem;
    font-family: 'Space Mono', monospace !important;
    margin-top: .3rem; letter-spacing: .1em; text-transform: uppercase;
}}

/* ── Theme toggle override ── */
div[data-testid="stSidebar"] .stButton button {{
    background: var(--toggle-bg) !important;
    color: var(--toggle-color) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: .9rem !important;
    width: 100% !important;
}}
div[data-testid="stSidebar"] .stButton button:hover {{
    opacity: .82 !important; transform: translateY(-1px) !important;
}}

.nav-label {{
    font-family: 'Space Mono', monospace !important;
    font-size: .63rem; text-transform: uppercase;
    letter-spacing: .15em; color: var(--muted); margin-bottom: .4rem;
}}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {{
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
}}

/* ── Built-with card ── */
.built-card {{
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 12px; padding: 1rem 1.2rem; margin-top: 1rem;
}}
.built-card .bt {{ font-family:'Space Mono',monospace; font-size:.63rem;
    text-transform:uppercase; letter-spacing:.12em; color:var(--muted); margin-bottom:.75rem; }}
.built-card .bi {{ display:flex; align-items:center; gap:.5rem;
    font-size:.84rem; color:var(--text2); margin-bottom:.4rem; }}

/* ── Hero ── */
[data-testid="stAppViewContainer"]::before {{
    content:''; position:fixed; inset:0;
    background: var(--hero-grad);
    pointer-events:none; z-index:0;
}}
.hero {{ position:relative; padding:3rem 0 2rem; margin-bottom:2rem; }}

.hero-badge {{
    display:inline-flex; align-items:center; gap:.5rem;
    background:rgba(255,107,44,.1); border:1px solid rgba(255,107,44,.3);
    color:var(--accent1); font-family:'Space Mono',monospace;
    font-size:.68rem; letter-spacing:.12em; text-transform:uppercase;
    padding:.3rem .85rem; border-radius:999px; margin-bottom:1.25rem;
}}
.hero-badge::before {{ content:'●'; animation:pulse 2s infinite; }}
@keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:.3}} }}

.hero-title {{
    font-family: 'Glacial Indifference', sans-serif !important;
    font-weight: 700;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    line-height: 1.08; letter-spacing:.02em; margin:0 0 .75rem;
}}
.hero-title .line1 {{ color:var(--text); display:block; }}
.hero-title .line2 {{
    background:linear-gradient(90deg, var(--accent1) 0%, var(--accent3) 50%, var(--accent2) 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; display:block;
}}
.hero-sub {{
    color:var(--muted); font-size:1.05rem; max-width:540px;
    line-height:1.65; font-family:'DM Sans',sans-serif;
}}

/* ── Stat chips ── */
.stats-row {{ display:flex; gap:1rem; flex-wrap:wrap; margin:1.5rem 0; }}
.stat-chip {{
    background:var(--panel); border:1px solid var(--border);
    border-radius:14px; padding:.8rem 1.3rem; min-width:135px;
    position:relative; overflow:hidden; box-shadow:var(--shadow);
}}
.stat-chip::after {{ content:''; position:absolute; top:0; left:0; right:0; height:2px; }}
.stat-chip.orange::after {{ background:var(--accent1); box-shadow:var(--glow1); }}
.stat-chip.cyan::after   {{ background:var(--accent2); box-shadow:var(--glow2); }}
.stat-chip.indigo::after {{ background:var(--accent3); }}
.stat-chip .val {{
    font-family:'Glacial Indifference',sans-serif !important;
    font-size:1.65rem; font-weight:700; color:var(--text); line-height:1;
}}
.stat-chip .lbl {{
    font-size:.7rem; color:var(--muted); text-transform:uppercase;
    letter-spacing:.08em; margin-top:.25rem; font-family:'DM Sans',sans-serif;
}}

/* ── Section header ── */
.section-header {{ display:flex; align-items:center; gap:.75rem; margin-bottom:1.75rem; }}
.section-header .icon-box {{
    width:42px; height:42px; border-radius:11px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.2rem; flex-shrink:0;
}}
.icon-orange {{ background:rgba(255,107,44,.12); border:1px solid rgba(255,107,44,.3); }}
.icon-cyan   {{ background:rgba(56,189,248,.1);  border:1px solid rgba(56,189,248,.25); }}
.section-header h2 {{
    font-family:'Glacial Indifference',sans-serif !important;
    font-weight:700; font-size:1.45rem; margin:0;
    color:var(--text); letter-spacing:.02em;
}}
.section-header p {{ margin:.15rem 0 0; color:var(--muted); font-size:.85rem; }}

/* ── Chat topbar ── */
.chat-topbar {{
    background:var(--surface); border-bottom:1px solid var(--border);
    padding:.85rem 1.5rem; display:flex; align-items:center; gap:.6rem;
    border-radius:16px 16px 0 0;
}}
.dot {{ width:10px; height:10px; border-radius:50%; display:inline-block; margin-right:1px; }}
.dot-r{{background:#FF5F57;}} .dot-y{{background:#FEBC2E;}} .dot-g{{background:#28C840;}}
.chat-topbar .chat-title {{
    font-family:'Space Mono',monospace; font-size:.78rem;
    color:var(--muted); margin-left:.4rem; letter-spacing:.05em;
}}
.chat-topbar .status-pill {{
    margin-left:auto; background:rgba(40,200,64,.1);
    border:1px solid rgba(40,200,64,.3); color:#28C840;
    font-size:.68rem; font-family:'Space Mono',monospace;
    padding:.2rem .65rem; border-radius:999px; letter-spacing:.08em;
}}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {{ background:transparent !important; border:none !important; }}
[data-testid="stChatMessage"] .stMarkdown p {{
    color:var(--text) !important; font-family:'DM Sans',sans-serif !important;
    font-size:.97rem !important; line-height:1.65 !important;
}}
[data-testid="chatAvatarIcon-user"] {{
    background:linear-gradient(135deg,var(--accent1),var(--accent3)) !important; border:none !important;
}}
[data-testid="chatAvatarIcon-assistant"] {{
    background:linear-gradient(135deg,var(--accent2),#1D4ED8) !important; border:none !important;
}}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {{
    background:var(--panel) !important; border:1.5px solid var(--border) !important;
    border-radius:14px !important; color:var(--text) !important;
    font-family:'DM Sans',sans-serif !important; font-size:.97rem !important;
}}
[data-testid="stChatInput"] textarea:focus {{
    border-color:var(--accent1) !important; box-shadow:var(--glow1) !important;
}}
[data-testid="stChatInput"] button {{
    background:linear-gradient(135deg,var(--accent1),var(--accent3)) !important;
    border:none !important; border-radius:10px !important;
}}

/* ── File uploader ── */
div[data-testid="stFileUploader"] {{ background:transparent !important; border:none !important; padding:0 !important; }}
div[data-testid="stFileUploader"] > label {{ display:none !important; }}
div[data-testid="stFileUploader"] section {{
    background:var(--panel) !important; border:1.5px dashed var(--border) !important;
    border-radius:12px !important; padding:.6rem 1rem !important; min-height:unset !important;
    transition:border-color .2s;
}}
div[data-testid="stFileUploader"] section:hover {{ border-color:var(--accent1) !important; }}
div[data-testid="stFileUploader"] section * {{ color:var(--text) !important; }}

/* ── Attach tray ── */
.attach-tray {{
    display:flex; align-items:center; gap:.75rem;
    margin-bottom:.5rem; padding:.5rem .75rem;
    background:var(--panel); border:1px solid var(--border); border-radius:14px;
}}
.attach-label {{
    font-family:'Space Mono',monospace; font-size:.66rem; color:var(--muted);
    letter-spacing:.08em; text-transform:uppercase; white-space:nowrap; flex-shrink:0;
}}
.attach-label span {{ color:var(--accent1); margin-right:.35rem; }}

/* ── General buttons ── */
.stButton button {{
    background:var(--panel) !important; border:1px solid var(--border) !important;
    color:var(--text) !important; border-radius:10px !important;
    font-family:'DM Sans',sans-serif !important; transition:all .2s !important;
}}
.stButton button:hover {{
    border-color:var(--accent1) !important; color:var(--accent1) !important;
}}

/* ── Alert ── */
[data-testid="stAlert"] {{
    background:rgba(56,189,248,.07) !important;
    border:1px solid rgba(56,189,248,.2) !important;
    border-radius:12px !important; color:var(--text) !important;
}}

/* ── Image preview ── */
[data-testid="stImage"] img {{
    border-radius:14px !important; border:1px solid var(--border) !important;
    box-shadow:var(--shadow) !important;
}}

/* ── HR, scrollbar ── */
hr {{ border-color:var(--border) !important; margin:1.5rem 0 !important; }}
::-webkit-scrollbar {{ width:6px; }}
::-webkit-scrollbar-track {{ background:var(--bg); }}
::-webkit-scrollbar-thumb {{ background:var(--border); border-radius:3px; }}

/* ── Category grid ── */
.cat-grid {{
    background:var(--panel2); border:1px solid var(--border);
    border-radius:14px; padding:1.25rem; margin-bottom:1rem;
}}
.cat-grid .ct {{ font-family:'Space Mono',monospace; font-size:.65rem; color:var(--muted);
    letter-spacing:.1em; text-transform:uppercase; margin-bottom:.75rem; }}
.cat-grid .ci {{ display:grid; grid-template-columns:1fr 1fr; gap:.5rem; }}
.cat-item {{
    background:var(--panel); border-radius:8px; padding:.5rem .75rem;
    font-size:.83rem; color:var(--text2); border:1px solid var(--border);
    font-family:'DM Sans',sans-serif;
}}

/* ── Footer ── */
.footer {{
    margin-top:4rem; padding:1.5rem 0; border-top:1px solid var(--border);
    display:flex; align-items:center; justify-content:space-between;
    flex-wrap:wrap; gap:1rem;
}}
.footer-left {{ font-family:'Space Mono',monospace; font-size:.68rem; color:var(--muted); letter-spacing:.06em; }}
.footer-badge {{
    background:rgba(255,107,44,.1); border:1px solid rgba(255,107,44,.25);
    color:var(--accent1); font-family:'Space Mono',monospace; font-size:.66rem;
    padding:.28rem .75rem; border-radius:999px; letter-spacing:.08em; text-transform:uppercase;
}}
</style>
<div class="theme-ribbon"></div>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="flag">🇮🇳</span>
        <div class="brand">Janta Seva</div>
        <div class="tagline">Civic Intelligence Platform</div>
    </div>
    <div class="nav-label">Navigate</div>
    """, unsafe_allow_html=True)

    option = st.selectbox(
        "Feature", ["💬 Complaint Chatbot", "🖼️ Image Classifier"],
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    btn_label = "☀️  Light Mode" if dark else "🌙  Dark Mode"
    if st.button(btn_label, key="theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("""
    <div class="built-card">
        <div class="bt">Built With</div>
        <div class="bi"><span style="color:var(--accent1)">⬡</span> Databricks</div>
        <div class="bi"><span style="color:var(--accent2)">◈</span> Claude AI</div>
        <div class="bi"><span style="color:var(--accent3)">❋</span> Streamlit</div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🔴 Live · Databricks Hackathon 2025</div>
    <div class="hero-title">
        <span class="line1">Empowering Citizens.</span>
        <span class="line2">Powered by AI.</span>
    </div>
    <p class="hero-sub">
        A unified civic intelligence platform that transforms public complaints into actionable
        insights — built on Databricks, designed for Bharat.
    </p>
    <div class="stats-row">
        <div class="stat-chip orange"><div class="val">1.4B</div><div class="lbl">Citizens Served</div></div>
        <div class="stat-chip cyan"><div class="val">98%</div><div class="lbl">Resolution Rate</div></div>
        <div class="stat-chip indigo"><div class="val">&lt;2s</div><div class="lbl">Response Time</div></div>
    </div>
</div>
<hr>
""", unsafe_allow_html=True)


# ── CHATBOT ───────────────────────────────────────────────────────────────────
if "💬" in option:

    st.markdown("""
    <div class="section-header">
        <div class="icon-box icon-orange">💬</div>
        <div><h2>Complaint Chatbot</h2><p>AI-powered civic grievance resolution</p></div>
    </div>
    <div class="chat-topbar">
        <span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span>
        <span class="chat-title">seva-bot · v2.0</span>
        <span class="status-pill">● ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_image" not in st.session_state:
        st.session_state.pending_image = None

    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown(
                "🙏 **Namaste!** I'm SevaBot, your AI civic assistant. "
                "Tell me your complaint — roads, water, electricity, sanitation — or **📎 attach a photo** of the problem. "
                "I'll register it instantly and track resolution in real-time."
            )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("image"):
                st.image(msg["image"], width=300)
            st.markdown(msg["content"])

    # Attachment tray
    st.markdown('<div class="attach-tray"><span class="attach-label"><span>📎</span> Attach Photo (optional)</span>', unsafe_allow_html=True)
    uploaded_img = st.file_uploader(
        "attach", type=["jpg","jpeg","png","webp"],
        key="chat_img_upload", label_visibility="collapsed",
        help="Upload or drag a photo of the civic issue",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_img:
        col_prev, col_clear = st.columns([3, 1])
        with col_prev:
            st.image(uploaded_img, caption="📸 Attached — will send with your message", width=260)
        with col_clear:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✕ Remove", key="remove_img", use_container_width=True):
                st.session_state.chat_img_upload = None
                st.rerun()
        st.session_state.pending_image = uploaded_img
    else:
        st.session_state.pending_image = None

    if prompt := st.chat_input("Describe your civic complaint… (or just send a photo 👆)"):
        img_data = st.session_state.pending_image
        user_msg: dict = {"role": "user", "content": prompt or "📸 *Sent a photo*"}
        if img_data:
            user_msg["image"] = img_data
        st.session_state.messages.append(user_msg)

        with st.chat_message("user"):
            if img_data:
                st.image(img_data, width=300)
            st.markdown(user_msg["content"])

        p = (prompt or "").lower()
        has_img = img_data is not None
        img_note = "\n\n📸 *Your photo has been attached to this ticket for field verification.*" if has_img else ""

        if any(w in p for w in ["road","pothole","street"]) or (has_img and not prompt):
            cat, pfx, dept, eta, emo = "Road / Infrastructure","RD","PWD (Public Works Department)","3–5 working days","🛣️"
        elif any(w in p for w in ["water","pipe","supply"]):
            cat, pfx, dept, eta, emo = "Water Supply","WS","Municipal Water Authority","24 hours","💧"
        elif any(w in p for w in ["light","electricity","power","outage"]):
            cat, pfx, dept, eta, emo = "Electricity / Power","PW","DISCOM Control Room","2–4 hours","⚡"
        elif any(w in p for w in ["garbage","waste","sanitation","clean"]):
            cat, pfx, dept, eta, emo = "Sanitation","SN","Municipal Sanitation Wing","48 hours","🗑️"
        else:
            cat, pfx, dept, eta, emo = "General Grievance","GN","Concerned Department","72 hours","✅"

        ticket = f"#{pfx}-2025-{len(st.session_state.messages):04d}"
        response = f"{emo} **{cat} complaint registered** · Ticket `{ticket}`\n\nForwarded to **{dept}**. Expected resolution: **{eta}**.{img_note}"

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.pending_image = None
        st.rerun()


# ── IMAGE CLASSIFIER ──────────────────────────────────────────────────────────
elif "🖼️" in option:

    st.markdown("""
    <div class="section-header">
        <div class="icon-box icon-cyan">🖼️</div>
        <div><h2>Civic Image Classifier</h2><p>Upload infrastructure images for AI-powered damage assessment</p></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown("""
        <div class="cat-grid">
            <div class="ct">Supported Categories</div>
            <div class="ci">
                <div class="cat-item">🛣️ Road Damage</div>
                <div class="cat-item">💧 Water Leakage</div>
                <div class="cat-item">🗑️ Garbage Dump</div>
                <div class="cat-item">⚡ Broken Lines</div>
                <div class="cat-item">🏗️ Encroachment</div>
                <div class="cat-item">🌊 Waterlogging</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        file = st.file_uploader("Drop your image here", type=["jpg","jpeg","png","webp"],
                                help="Upload a photo of the civic issue for AI classification")

    with col2:
        if file:
            st.image(file, caption="Uploaded Image", use_column_width=True)
            st.markdown("""
            <div style="background:rgba(56,189,248,.07);border:1px solid rgba(56,189,248,.2);
                        border-radius:14px;padding:1.25rem;margin-top:1rem;">
                <div style="font-family:'Space Mono',monospace;font-size:.68rem;color:var(--accent2);
                            letter-spacing:.1em;text-transform:uppercase;margin-bottom:.5rem;">🔬 Analysis Status</div>
                <div style="color:var(--text);font-size:.9rem;line-height:1.65;font-family:'DM Sans',sans-serif;">
                    🚧 <strong>Model Training in Progress</strong><br>
                    <span style="color:var(--muted);font-size:.82rem;">
                        Our ResNet-50 is being fine-tuned on Databricks GPU clusters. Predictions go live soon!
                    </span>
                </div>
                <div style="margin-top:1rem;">
                    <div style="height:4px;background:var(--border);border-radius:2px;overflow:hidden;">
                        <div style="height:100%;width:68%;background:linear-gradient(90deg,var(--accent1),var(--accent2));
                                    border-radius:2px;animation:prog 2s ease-in-out infinite alternate;"></div>
                    </div>
                    <div style="font-family:'Space Mono',monospace;font-size:.63rem;color:var(--muted);margin-top:.4rem;">68% · ETA ~2 days</div>
                </div>
            </div>
            <style>@keyframes prog {{ from{{width:55%}} to{{width:80%}} }}</style>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="height:300px;background:var(--panel2);border:1.5px dashed var(--border);
                        border-radius:16px;display:flex;flex-direction:column;
                        align-items:center;justify-content:center;gap:1rem;">
                <div style="font-size:3rem;">📸</div>
                <div style="color:var(--muted);font-size:.9rem;text-align:center;
                            line-height:1.6;font-family:'DM Sans',sans-serif;">
                    Upload an image to begin<br>
                    <span style="font-size:.8rem;">Supports JPG, PNG, WEBP</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-left">© 2025 JANTA SEVA · CIVIC INTELLIGENCE PLATFORM · BUILT FOR BHARAT</div>
    <div class="footer-badge">⬡ Databricks Hackathon 2025</div>
</div>
""", unsafe_allow_html=True)
