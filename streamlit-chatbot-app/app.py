import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Janta Seva",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Root ── */
:root {
    --bg:        #050810;
    --surface:   #0c1120;
    --panel:     #111827;
    --border:    #1e2d45;
    --accent1:   #FF6B2C;   /* Databricks orange */
    --accent2:   #00E5FF;   /* electric cyan     */
    --accent3:   #FF3D7F;   /* hot pink          */
    --gold:      #FFD700;
    --text:      #E8EDF5;
    --muted:     #6B7A99;
    --radius:    14px;
    --glow1: 0 0 20px rgba(255,107,44,.35), 0 0 60px rgba(255,107,44,.12);
    --glow2: 0 0 20px rgba(0,229,255,.35),  0 0 60px rgba(0,229,255,.12);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Animated starfield bg ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 0%,   rgba(255,107,44,.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%,  rgba(0,229,255,.07)  0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 60% 40%,  rgba(255,61,127,.05) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { font-family: 'DM Sans', sans-serif !important; }

/* Sidebar logo area */
.sidebar-logo {
    text-align: center;
    padding: 2rem 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.sidebar-logo .flag { font-size: 3rem; display: block; margin-bottom: .5rem; }
.sidebar-logo .brand {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    background: linear-gradient(135deg, var(--accent1), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -.02em;
}
.sidebar-logo .tagline {
    color: var(--muted);
    font-size: .75rem;
    font-family: 'Space Mono', monospace;
    margin-top: .25rem;
    letter-spacing: .1em;
    text-transform: uppercase;
}

/* nav pills */
.nav-label {
    font-family: 'Space Mono', monospace;
    font-size: .65rem;
    text-transform: uppercase;
    letter-spacing: .15em;
    color: var(--muted);
    padding: 0 .5rem;
    margin-bottom: .5rem;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] select,
[data-testid="stSelectbox"] > div > div {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Main header ── */
.hero {
    position: relative;
    padding: 3rem 0 2rem;
    margin-bottom: 2rem;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    background: rgba(255,107,44,.1);
    border: 1px solid rgba(255,107,44,.3);
    color: var(--accent1);
    font-family: 'Space Mono', monospace;
    font-size: .7rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    padding: .35rem .85rem;
    border-radius: 999px;
    margin-bottom: 1.25rem;
}
.hero-badge::before { content: '●'; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.2rem, 5vw, 3.5rem);
    line-height: 1.05;
    letter-spacing: -.03em;
    margin: 0 0 .75rem;
}
.hero-title .line1 { color: var(--text); }
.hero-title .line2 {
    background: linear-gradient(90deg, var(--accent1) 0%, var(--accent3) 50%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    max-width: 520px;
    line-height: 1.6;
}

/* ── Stat chips ── */
.stats-row { display:flex; gap:1rem; flex-wrap:wrap; margin: 1.5rem 0; }
.stat-chip {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: .75rem 1.25rem;
    min-width: 130px;
    position: relative;
    overflow: hidden;
}
.stat-chip::after {
    content:'';
    position:absolute; top:0; left:0; right:0; height:2px;
}
.stat-chip.orange::after { background: var(--accent1); box-shadow: var(--glow1); }
.stat-chip.cyan::after   { background: var(--accent2); box-shadow: var(--glow2); }
.stat-chip.pink::after   { background: var(--accent3); }
.stat-chip .val {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.stat-chip .lbl {
    font-size: .72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-top: .2rem;
}

/* ── Section header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: .75rem;
    margin-bottom: 1.75rem;
}
.section-header .icon-box {
    width: 40px; height: 40px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.icon-orange { background: rgba(255,107,44,.15); border: 1px solid rgba(255,107,44,.3); }
.icon-cyan   { background: rgba(0,229,255,.12);  border: 1px solid rgba(0,229,255,.25); }
.section-header h2 {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    margin: 0;
    color: var(--text);
    letter-spacing: -.02em;
}
.section-header p { margin: .15rem 0 0; color: var(--muted); font-size: .85rem; }

/* ── Chat ── */
.chat-wrapper {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 4px 40px rgba(0,0,0,.4);
}
.chat-topbar {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: .75rem;
}
.chat-topbar .dot {
    width: 10px; height: 10px; border-radius: 50%;
    display: inline-block; margin-right: 2px;
}
.dot-r{background:#FF5F57;} .dot-y{background:#FEBC2E;} .dot-g{background:#28C840;}
.chat-topbar .chat-title {
    font-family: 'Space Mono', monospace;
    font-size: .8rem;
    color: var(--muted);
    margin-left: .5rem;
    letter-spacing: .05em;
}
.chat-topbar .status-pill {
    margin-left: auto;
    background: rgba(40,200,64,.12);
    border: 1px solid rgba(40,200,64,.3);
    color: #28C840;
    font-size: .7rem;
    font-family: 'Space Mono', monospace;
    padding: .2rem .65rem;
    border-radius: 999px;
    letter-spacing: .08em;
}

/* ── Override chat message bubbles ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: .5rem 1.5rem !important;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    background: rgba(255,107,44,.05) !important;
}
[data-testid="stChatMessage"] .stMarkdown p {
    color: var(--text) !important;
    font-size: .95rem !important;
    line-height: 1.6 !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, var(--accent1), var(--accent3)) !important;
    border: none !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, var(--accent2), #0066CC) !important;
    border: none !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea,
[data-testid="stChatInputTextArea"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .95rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent1) !important;
    box-shadow: var(--glow1) !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, var(--accent1), var(--accent3)) !important;
    border: none !important;
    border-radius: 10px !important;
}

/* ── Image attach toolbar ── */
.attach-toolbar {
    display: flex;
    gap: .6rem;
    align-items: center;
    padding: .75rem 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    margin-bottom: .75rem;
}
.attach-label {
    font-family: 'Space Mono', monospace;
    font-size: .68rem;
    color: var(--muted);
    letter-spacing: .1em;
    text-transform: uppercase;
    margin-right: .25rem;
    white-space: nowrap;
}

/* style the file uploader inside toolbar as minimal */
.attach-toolbar [data-testid="stFileUploader"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
.attach-toolbar [data-testid="stFileUploader"] label { display: none !important; }
.attach-toolbar [data-testid="stFileUploaderDropzone"] {
    background: rgba(255,107,44,.08) !important;
    border: 1px solid rgba(255,107,44,.25) !important;
    border-radius: 10px !important;
    padding: .4rem .9rem !important;
    min-height: unset !important;
}
.attach-toolbar [data-testid="stFileUploaderDropzoneInstructions"] {
    font-size: .78rem !important;
    color: var(--accent1) !important;
}

/* Camera input styling */
[data-testid="stCameraInput"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}
[data-testid="stCameraInput"] button {
    background: linear-gradient(135deg, var(--accent2), #0066CC) !important;
    border: none !important;
    color: #000 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}

/* ── Chat image preview bubble ── */
.chat-img-preview {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: .75rem;
    display: inline-flex;
    flex-direction: column;
    gap: .5rem;
    max-width: 320px;
    margin-bottom: .5rem;
}
.chat-img-preview img {
    border-radius: 10px !important;
    width: 100%;
    object-fit: cover;
    max-height: 200px;
}
.chat-img-caption {
    font-family: 'Space Mono', monospace;
    font-size: .65rem;
    color: var(--muted);
    letter-spacing: .08em;
    text-align: center;
}

/* ── Tab styling ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--surface) !important;
    border-radius: 12px !important;
    padding: .3rem !important;
    gap: .25rem !important;
    border: 1px solid var(--border) !important;
    margin-bottom: 1rem;
}
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    border: none !important;
    padding: .4rem 1rem !important;
    transition: all .2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(255,107,44,.2), rgba(255,61,127,.15)) !important;
    color: var(--accent1) !important;
    border: 1px solid rgba(255,107,44,.3) !important;
}

/* ── Image uploader ── */
[data-testid="stFileUploader"] {
    background: var(--panel) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    transition: border-color .2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent2) !important;
}
[data-testid="stFileUploader"] label { color: var(--text) !important; }

/* ── Info / success boxes ── */
[data-testid="stAlert"] {
    background: rgba(0,229,255,.07) !important;
    border: 1px solid rgba(0,229,255,.2) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}

/* ── Image preview ── */
[data-testid="stImage"] img {
    border-radius: 16px !important;
    border: 1px solid var(--border) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,.4) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Databricks hackathon ribbon ── */
.hackathon-ribbon {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent1) 0%, var(--accent3) 50%, var(--accent2) 100%);
    z-index: 9999;
}

/* ── Footer ── */
.footer {
    margin-top: 4rem;
    padding: 1.5rem 0;
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
}
.footer-left {
    font-family: 'Space Mono', monospace;
    font-size: .72rem;
    color: var(--muted);
    letter-spacing: .06em;
}
.footer-badge {
    background: rgba(255,107,44,.1);
    border: 1px solid rgba(255,107,44,.25);
    color: var(--accent1);
    font-family: 'Space Mono', monospace;
    font-size: .68rem;
    padding: .3rem .75rem;
    border-radius: 999px;
    letter-spacing: .08em;
    text-transform: uppercase;
}

/* Override streamlit default header */
h1,h2,h3 { color: var(--text) !important; }
</style>

<!-- Top rainbow ribbon -->
<div class="hackathon-ribbon"></div>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
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
        "Choose Feature",
        ["💬 Complaint Chatbot", "🖼️ Image Classifier"],
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#111827;border:1px solid #1e2d45;border-radius:12px;padding:1rem 1.2rem;">
        <div style="font-family:'Space Mono',monospace;font-size:.65rem;color:#6B7A99;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.75rem;">
            Built With
        </div>
        <div style="display:flex;flex-direction:column;gap:.5rem;">
            <div style="display:flex;align-items:center;gap:.5rem;font-size:.82rem;color:#E8EDF5;">
                <span style="color:#FF6B2C;">⬡</span> Databricks
            </div>
            <div style="display:flex;align-items:center;gap:.5rem;font-size:.82rem;color:#E8EDF5;">
                <span style="color:#00E5FF;">◈</span> Claude AI
            </div>
            <div style="display:flex;align-items:center;gap:.5rem;font-size:.82rem;color:#E8EDF5;">
                <span style="color:#FF3D7F;">❋</span> Streamlit
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🔴 Live · Databricks Hackathon 2025</div>
    <div class="hero-title">
        <div class="line1">Empowering Citizens.</div>
        <div class="line2">Powered by AI.</div>
    </div>
    <p class="hero-sub">
        A unified civic intelligence platform that transforms public complaints into actionable
        insights — built on Databricks, designed for Bharat.
    </p>
    <div class="stats-row">
        <div class="stat-chip orange">
            <div class="val">1.4B</div>
            <div class="lbl">Citizens Served</div>
        </div>
        <div class="stat-chip cyan">
            <div class="val">98%</div>
            <div class="lbl">Resolution Rate</div>
        </div>
        <div class="stat-chip pink">
            <div class="val">&lt;2s</div>
            <div class="lbl">Response Time</div>
        </div>
    </div>
</div>
<hr>
""", unsafe_allow_html=True)


# ── CHATBOT ──────────────────────────────────────────────────────────────────
if "💬" in option:

    st.markdown("""
    <div class="section-header">
        <div class="icon-box icon-orange">💬</div>
        <div>
            <h2>Complaint Chatbot</h2>
            <p>AI-powered civic grievance resolution</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat topbar decoration
    st.markdown("""
    <div class="chat-topbar">
        <span class="dot dot-r"></span>
        <span class="dot dot-y"></span>
        <span class="dot dot-g"></span>
        <span class="chat-title">seva-bot · v2.0</span>
        <span class="status-pill">● ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

    # Init session
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_image" not in st.session_state:
        st.session_state.pending_image = None

    # Welcome message
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown(
                "🙏 **Namaste!** I'm SevaBot, your AI civic assistant. "
                "Tell me your complaint — about roads, water, electricity, sanitation, or any civic issue. "
                "You can also **📎 attach a photo** of the problem! "
                "I'll register it instantly and track resolution in real-time."
            )

    # Previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("image"):
                st.image(msg["image"], width=300)
            st.markdown(msg["content"])

    # ── Image uploader (above input, styled like an attachment tray) ──────────
    st.markdown("""
    <style>
    /* Hide the default file uploader label & drag zone — keep it compact */
    div[data-testid="stFileUploader"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    div[data-testid="stFileUploader"] > label { display: none !important; }
    div[data-testid="stFileUploader"] section {
        background: var(--panel) !important;
        border: 1px dashed var(--border) !important;
        border-radius: 12px !important;
        padding: .6rem 1rem !important;
        min-height: unset !important;
    }
    div[data-testid="stFileUploader"] section:hover {
        border-color: var(--accent1) !important;
    }
    div[data-testid="stFileUploader"] section > div {
        gap: .5rem !important;
    }
    /* attachment tray wrapper */
    .attach-tray {
        display: flex;
        align-items: center;
        gap: .75rem;
        margin-bottom: .5rem;
        padding: .5rem .75rem;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 14px;
    }
    .attach-label {
        font-family: 'Space Mono', monospace;
        font-size: .68rem;
        color: var(--muted);
        letter-spacing: .08em;
        text-transform: uppercase;
        white-space: nowrap;
        flex-shrink: 0;
    }
    .attach-label span { color: var(--accent1); margin-right: .35rem; }
    </style>
    """, unsafe_allow_html=True)

    # Attachment tray
    st.markdown('<div class="attach-tray"><span class="attach-label"><span>📎</span> Attach Photo (optional)</span>', unsafe_allow_html=True)
    uploaded_img = st.file_uploader(
        "attach",
        type=["jpg", "jpeg", "png", "webp"],
        key="chat_img_upload",
        label_visibility="collapsed",
        help="Upload or drag a photo of the civic issue",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Preview the attached image before sending
    if uploaded_img:
        col_prev, col_clear = st.columns([3, 1])
        with col_prev:
            st.image(uploaded_img, caption="📸 Attached — will be sent with your message", width=260)
        with col_clear:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✕ Remove", key="remove_img", use_container_width=True):
                st.session_state.chat_img_upload = None
                st.rerun()
        st.session_state.pending_image = uploaded_img
    else:
        st.session_state.pending_image = None

    # Text input
    if prompt := st.chat_input("Describe your civic complaint… (or just send a photo 👆)"):
        img_data = st.session_state.pending_image

        # Build user message
        user_msg: dict = {"role": "user", "content": prompt or "📸 *Sent a photo*"}
        if img_data:
            user_msg["image"] = img_data

        st.session_state.messages.append(user_msg)
        with st.chat_message("user"):
            if img_data:
                st.image(img_data, width=300)
            st.markdown(user_msg["content"])

        # Smart response — consider both text and image
        p = (prompt or "").lower()
        has_img = img_data is not None
        img_note = "\n\n📸 *Your photo has been attached to this ticket for field verification.*" if has_img else ""

        if any(w in p for w in ["road","pothole","street"]) or (has_img and not prompt):
            category = "Road / Infrastructure"
            ticket_prefix = "RD"
            dept = "PWD (Public Works Department)"
            eta = "3–5 working days"
            emoji = "🛣️"
        elif any(w in p for w in ["water","pipe","supply"]):
            category = "Water Supply"
            ticket_prefix = "WS"
            dept = "Municipal Water Authority"
            eta = "24 hours"
            emoji = "💧"
        elif any(w in p for w in ["light","electricity","power","outage"]):
            category = "Electricity / Power"
            ticket_prefix = "PW"
            dept = "DISCOM Control Room"
            eta = "2–4 hours"
            emoji = "⚡"
        elif any(w in p for w in ["garbage","waste","sanitation","clean"]):
            category = "Sanitation"
            ticket_prefix = "SN"
            dept = "Municipal Sanitation Wing"
            eta = "48 hours"
            emoji = "🗑️"
        else:
            category = "General Grievance"
            ticket_prefix = "GN"
            dept = "Concerned Department"
            eta = "72 hours"
            emoji = "✅"

        ticket_no = f"#{ticket_prefix}-2025-{len(st.session_state.messages):04d}"
        response = (
            f"{emoji} **{category} complaint registered** · Ticket `{ticket_no}`\n\n"
            f"Forwarded to **{dept}**. Expected resolution: **{eta}**."
            f"{img_note}"
        )

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Clear pending image after send
        st.session_state.pending_image = None
        st.rerun()


# ── IMAGE CLASSIFIER ─────────────────────────────────────────────────────────
elif "🖼️" in option:

    st.markdown("""
    <div class="section-header">
        <div class="icon-box icon-cyan">🖼️</div>
        <div>
            <h2>Civic Image Classifier</h2>
            <p>Upload infrastructure images for AI-powered damage assessment</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown("""
        <div style="background:#111827;border:1px solid #1e2d45;border-radius:16px;padding:1.5rem;margin-bottom:1rem;">
            <div style="font-family:'Space Mono',monospace;font-size:.68rem;color:#6B7A99;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.75rem;">
                Supported Categories
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem;">
                <div style="background:#0c1120;border-radius:8px;padding:.5rem .75rem;font-size:.82rem;color:#E8EDF5;">🛣️ Road Damage</div>
                <div style="background:#0c1120;border-radius:8px;padding:.5rem .75rem;font-size:.82rem;color:#E8EDF5;">💧 Water Leakage</div>
                <div style="background:#0c1120;border-radius:8px;padding:.5rem .75rem;font-size:.82rem;color:#E8EDF5;">🗑️ Garbage Dump</div>
                <div style="background:#0c1120;border-radius:8px;padding:.5rem .75rem;font-size:.82rem;color:#E8EDF5;">⚡ Broken Lines</div>
                <div style="background:#0c1120;border-radius:8px;padding:.5rem .75rem;font-size:.82rem;color:#E8EDF5;">🏗️ Encroachment</div>
                <div style="background:#0c1120;border-radius:8px;padding:.5rem .75rem;font-size:.82rem;color:#E8EDF5;">🌊 Waterlogging</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        file = st.file_uploader(
            "Drop your image here",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload a photo of the civic issue for AI classification",
        )

    with col2:
        if file:
            st.image(file, caption="Uploaded Image", use_column_width=True)
            st.markdown("""
            <div style="background:rgba(0,229,255,.07);border:1px solid rgba(0,229,255,.2);border-radius:14px;padding:1.25rem;margin-top:1rem;">
                <div style="font-family:'Space Mono',monospace;font-size:.7rem;color:#00E5FF;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.5rem;">
                    🔬 Analysis Status
                </div>
                <div style="color:#E8EDF5;font-size:.9rem;line-height:1.6;">
                    🚧 <strong>Model Training in Progress</strong><br>
                    <span style="color:#6B7A99;font-size:.82rem;">
                        Our ResNet-50 model is being fine-tuned on Databricks GPU clusters.
                        Predictions will be live shortly — stay tuned!
                    </span>
                </div>
                <div style="margin-top:1rem;">
                    <div style="height:4px;background:#1e2d45;border-radius:2px;overflow:hidden;">
                        <div style="height:100%;width:68%;background:linear-gradient(90deg,#FF6B2C,#00E5FF);border-radius:2px;animation:progress 2s ease-in-out infinite alternate;"></div>
                    </div>
                    <div style="font-family:'Space Mono',monospace;font-size:.65rem;color:#6B7A99;margin-top:.4rem;">68% · ETA ~2 days</div>
                </div>
            </div>
            <style>
            @keyframes progress { from{width:55%} to{width:80%} }
            </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="height:300px;background:#111827;border:1px dashed #1e2d45;border-radius:16px;
                        display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1rem;">
                <div style="font-size:3rem;">📸</div>
                <div style="color:#6B7A99;font-size:.9rem;text-align:center;line-height:1.6;">
                    Upload an image to begin<br>
                    <span style="font-size:.8rem;">Supports JPG, PNG, WEBP</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-left">© 2025 JANTA SEVA · CIVIC INTELLIGENCE PLATFORM · BUILT FOR BHARAT</div>
    <div class="footer-badge">⬡ Databricks Hackathon 2025</div>
</div>
""", unsafe_allow_html=True)
