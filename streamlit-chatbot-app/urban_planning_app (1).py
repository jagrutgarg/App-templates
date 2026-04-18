import streamlit as st
import anthropic
import datetime
import re
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Urban Planning Portal",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS + JS ───────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── root vars ── */
:root {
    --bg:        #0d1117;
    --surface:   #161b22;
    --surface2:  #1c2230;
    --accent:    #e8a045;
    --accent2:   #4fc3f7;
    --text:      #e6edf3;
    --muted:     #8b949e;
    --red:       #f85149;
    --yellow:    #f0c040;
    --green:     #3fb950;
    --border:    rgba(255,255,255,0.08);
}

/* ── global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* ── hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }

/* ══════════════════════════════════════════
   HERO BANNER
══════════════════════════════════════════ */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #0d1117 0%, #131a26 50%, #0d1117 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 2rem;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 60% 80% at 70% 50%, rgba(232,160,69,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-text h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: -1px;
    margin: 0;
    background: linear-gradient(90deg, var(--accent) 0%, #fff 60%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-text p {
    margin: .4rem 0 0;
    color: var(--muted);
    font-size: 1rem;
    font-weight: 400;
}

/* ── animated city skyline SVG ── */
.skyline-wrap {
    flex-shrink: 0;
    animation: skylineDrift 6s ease-in-out infinite alternate;
}
@keyframes skylineDrift {
    from { transform: translateY(0); }
    to   { transform: translateY(-6px); }
}

/* ══════════════════════════════════════════
   MAP CANVAS  (scrolling floor plans)
══════════════════════════════════════════ */
.map-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
    overflow: hidden;
    position: relative;
}
.map-section h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: var(--accent);
    margin: 0 0 .8rem;
    letter-spacing: .5px;
}
.map-track {
    display: flex;
    gap: 18px;
    width: max-content;
    animation: scrollPlans 28s linear infinite;
}
.map-track:hover { animation-play-state: paused; }
@keyframes scrollPlans {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.plan-card {
    width: 180px;
    height: 130px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: border-color .3s;
    position: relative;
    overflow: hidden;
}
.plan-card:hover { border-color: var(--accent); }
.plan-card svg { opacity: .85; }
.plan-label {
    position: absolute;
    bottom: 6px;
    left: 0; right: 0;
    text-align: center;
    font-size: .7rem;
    color: var(--muted);
    font-weight: 500;
    letter-spacing: .5px;
}

/* ══════════════════════════════════════════
   COMPLAINTS PANEL
══════════════════════════════════════════ */
.complaints-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1.5rem;
}
.complaints-panel h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: var(--accent2);
    margin: 0 0 1rem;
}
.complaint-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: .85rem 1rem;
    margin-bottom: .6rem;
    transition: border-color .25s;
    animation: fadeSlide .4s ease both;
}
.complaint-item:hover { border-color: rgba(255,255,255,0.2); }
@keyframes fadeSlide {
    from { opacity:0; transform: translateX(-12px); }
    to   { opacity:1; transform: translateX(0); }
}
.priority-dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 4px;
    box-shadow: 0 0 8px currentColor;
}
.dot-high   { background: var(--red);    color: var(--red); }
.dot-medium { background: var(--yellow); color: var(--yellow); }
.dot-low    { background: var(--green);  color: var(--green); }
.complaint-body { flex: 1; }
.complaint-text {
    font-size: .9rem;
    line-height: 1.5;
    margin: 0 0 .25rem;
}
.complaint-meta {
    font-size: .72rem;
    color: var(--muted);
    display: flex;
    gap: 12px;
    align-items: center;
}
.priority-badge {
    font-size: .65rem;
    font-weight: 600;
    padding: 2px 7px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: .5px;
}
.badge-high   { background: rgba(248,81,73,.18);  color: var(--red); }
.badge-medium { background: rgba(240,192,64,.18); color: var(--yellow); }
.badge-low    { background: rgba(63,185,80,.18);  color: var(--green); }

/* ══════════════════════════════════════════
   COMPLAINT INPUT
══════════════════════════════════════════ */
.input-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1.5rem;
}
.input-section h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: var(--accent);
    margin: 0 0 .8rem;
}
.stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .9rem !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(232,160,69,.15) !important;
}
div.stButton > button {
    background: linear-gradient(135deg, var(--accent), #c87d2a) !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: .55rem 1.8rem !important;
    font-size: .9rem !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: .3px !important;
    transition: opacity .2s !important;
}
div.stButton > button:hover { opacity: .85 !important; }

/* ══════════════════════════════════════════
   CHAT SECTION
══════════════════════════════════════════ */
.chat-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
}
.chat-section h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: var(--accent2);
    margin: 0 0 .8rem;
}
.chat-bubble {
    padding: .75rem 1rem;
    border-radius: 12px;
    margin-bottom: .6rem;
    max-width: 82%;
    font-size: .9rem;
    line-height: 1.55;
    animation: fadeSlide .3s ease both;
}
.bubble-user {
    background: rgba(232,160,69,.15);
    border: 1px solid rgba(232,160,69,.3);
    margin-left: auto;
    text-align: right;
}
.bubble-ai {
    background: var(--surface2);
    border: 1px solid var(--border);
}
.bubble-role {
    font-size: .68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .6px;
    color: var(--muted);
    margin-bottom: 4px;
}
.stChatInputContainer, .stChatInput {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
}
</style>

<!-- Whoosh sound (Web Audio API – auto plays once on load) -->
<script>
(function(){
    function whoosh(){
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const buf = ctx.createBuffer(1, ctx.sampleRate * 1.2, ctx.sampleRate);
            const data = buf.getChannelData(0);
            for(let i=0;i<data.length;i++){
                const t = i/ctx.sampleRate;
                const env = Math.exp(-3.5*t);
                data[i] = env*(Math.random()*2-1)*0.9;
            }
            const src = ctx.createBufferSource();
            src.buffer = buf;
            const filt = ctx.createBiquadFilter();
            filt.type = 'bandpass';
            filt.frequency.setValueAtTime(800,ctx.currentTime);
            filt.frequency.linearRampToValueAtTime(200,ctx.currentTime+1.2);
            filt.Q.value = 0.8;
            const gain = ctx.createGain();
            gain.gain.setValueAtTime(0.35,ctx.currentTime);
            gain.gain.linearRampToValueAtTime(0,ctx.currentTime+1.2);
            src.connect(filt); filt.connect(gain); gain.connect(ctx.destination);
            src.start();
        } catch(e){}
    }
    // play on first user interaction (browser policy)
    document.addEventListener('click', function once(){ whoosh(); document.removeEventListener('click',once); });
    // also try immediately (works in some browsers)
    window.addEventListener('load', function(){ setTimeout(whoosh,800); });
})();
</script>
""",
    unsafe_allow_html=True,
)

# ── Session state ──────────────────────────────────────────────────────────────
if "complaints" not in st.session_state:
    st.session_state.complaints = [
        {
            "text": "Water supply has been completely cut off in Sector 7 for 3 days. This is UNACCEPTABLE and OUTRAGEOUS!",
            "priority": "high",
            "date": (datetime.date.today() - datetime.timedelta(days=1)).strftime("%d %b %Y"),
        },
        {
            "text": "Pipe leakage on Main Street causing road damage and water wastage.",
            "priority": "medium",
            "date": (datetime.date.today() - datetime.timedelta(days=3)).strftime("%d %b %Y"),
        },
        {
            "text": "Tap water has a slight yellowish tint in Block C. Please check when convenient.",
            "priority": "low",
            "date": (datetime.date.today() - datetime.timedelta(days=5)).strftime("%d %b %Y"),
        },
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Priority classifier ────────────────────────────────────────────────────────
ANGER_WORDS = {
    "angry", "furious", "outraged", "disgusting", "unacceptable", "horrible",
    "terrible", "awful", "pathetic", "useless", "incompetent", "ridiculous",
    "absurd", "shameful", "disgusted", "fed up", "sick of", "enough",
    "!!", "!!!", "worst", "hate", "appalling", "infuriating",
}

def classify_priority(text: str) -> str:
    lower = text.lower()
    score = sum(1 for w in ANGER_WORDS if w in lower)
    exclamations = text.count("!")
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    total = score * 2 + exclamations + (caps_ratio * 10)
    if total >= 4:
        return "high"
    elif total >= 1.5:
        return "medium"
    return "low"

def sort_complaints(lst):
    order = {"high": 0, "medium": 1, "low": 2}
    return sorted(lst, key=lambda x: order[x["priority"]])

# ══════════════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
<div class="hero">
  <div class="hero-text">
    <h1>Urban Planning</h1>
    <p>Citizen portal · Water complaints · City infrastructure</p>
  </div>
  <div class="skyline-wrap">
    <svg width="260" height="110" viewBox="0 0 260 110" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- buildings -->
      <rect x="0"  y="60" width="30" height="50" fill="#1c2a3a" stroke="#e8a045" stroke-width="1"/>
      <rect x="5"  y="65" width="8"  height="8"  fill="#4fc3f7" opacity=".6"/>
      <rect x="17" y="65" width="8"  height="8"  fill="#4fc3f7" opacity=".4"/>
      <rect x="5"  y="78" width="8"  height="8"  fill="#4fc3f7" opacity=".3"/>
      <rect x="17" y="78" width="8"  height="8"  fill="#4fc3f7" opacity=".6"/>

      <rect x="35" y="30" width="40" height="80" fill="#162030" stroke="#e8a045" stroke-width="1"/>
      <rect x="52" y="20" width="6"  height="10" fill="#e8a045" opacity=".8"/>
      <rect x="40" y="38" width="10" height="10" fill="#4fc3f7" opacity=".5"/>
      <rect x="56" y="38" width="10" height="10" fill="#4fc3f7" opacity=".3"/>
      <rect x="40" y="54" width="10" height="10" fill="#4fc3f7" opacity=".6"/>
      <rect x="56" y="54" width="10" height="10" fill="#4fc3f7" opacity=".4"/>
      <rect x="40" y="70" width="10" height="10" fill="#4fc3f7" opacity=".2"/>
      <rect x="56" y="70" width="10" height="10" fill="#4fc3f7" opacity=".5"/>

      <rect x="80" y="50" width="25" height="60" fill="#1a2535" stroke="#e8a045" stroke-width="1"/>
      <rect x="85" y="55" width="7"  height="7"  fill="#4fc3f7" opacity=".5"/>
      <rect x="95" y="55" width="7"  height="7"  fill="#4fc3f7" opacity=".3"/>
      <rect x="85" y="68" width="7"  height="7"  fill="#4fc3f7" opacity=".6"/>

      <rect x="110" y="20" width="50" height="90" fill="#0f1c2e" stroke="#e8a045" stroke-width="1.5"/>
      <rect x="132" y="8"  width="6"  height="12" fill="#e8a045"/>
      <rect x="115" y="28" width="12" height="12" fill="#4fc3f7" opacity=".6"/>
      <rect x="133" y="28" width="12" height="12" fill="#4fc3f7" opacity=".4"/>
      <rect x="115" y="46" width="12" height="12" fill="#4fc3f7" opacity=".3"/>
      <rect x="133" y="46" width="12" height="12" fill="#4fc3f7" opacity=".7"/>
      <rect x="115" y="64" width="12" height="12" fill="#4fc3f7" opacity=".5"/>
      <rect x="133" y="64" width="12" height="12" fill="#4fc3f7" opacity=".2"/>

      <rect x="165" y="40" width="30" height="70" fill="#162030" stroke="#e8a045" stroke-width="1"/>
      <rect x="170" y="46" width="8"  height="8"  fill="#4fc3f7" opacity=".4"/>
      <rect x="182" y="46" width="8"  height="8"  fill="#4fc3f7" opacity=".6"/>
      <rect x="170" y="60" width="8"  height="8"  fill="#4fc3f7" opacity=".3"/>

      <rect x="200" y="55" width="35" height="55" fill="#1c2a3a" stroke="#e8a045" stroke-width="1"/>
      <rect x="206" y="62" width="9"  height="9"  fill="#4fc3f7" opacity=".5"/>
      <rect x="219" y="62" width="9"  height="9"  fill="#4fc3f7" opacity=".3"/>
      <rect x="206" y="76" width="9"  height="9"  fill="#4fc3f7" opacity=".6"/>
      <rect x="219" y="76" width="9"  height="9"  fill="#4fc3f7" opacity=".4"/>

      <rect x="240" y="70" width="20" height="40" fill="#1a2535" stroke="#e8a045" stroke-width="1"/>

      <!-- ground -->
      <line x1="0" y1="110" x2="260" y2="110" stroke="#e8a045" stroke-width="1.5"/>
    </svg>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
#  SCROLLING HOUSE PLANS
# ══════════════════════════════════════════════════════════════════════════════

def plan_svg(label, walls, doors):
    """Generate a tiny SVG floor plan."""
    lines = "\n".join(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e8a045" stroke-width="2"/>'
        for x1, y1, x2, y2 in walls
    )
    arcs = "\n".join(
        f'<path d="M {x} {y} a 10 10 0 0 1 {dx} {dy}" stroke="#4fc3f7" stroke-width="1.5" fill="none"/>'
        for x, y, dx, dy in doors
    )
    return f"""
<svg width="160" height="110" viewBox="0 0 160 110" xmlns="http://www.w3.org/2000/svg">
  <rect width="160" height="110" fill="#0f1c2e"/>
  {lines}
  {arcs}
  <text x="80" y="104" fill="#8b949e" font-size="9" text-anchor="middle" font-family="DM Sans,sans-serif">{label}</text>
</svg>"""


plans = [
    plan_svg(
        "Studio Flat",
        [(10,10,150,10),(10,10,10,100),(150,10,150,100),(10,100,150,100),
         (10,55,80,55),(80,10,80,55)],
        [(10,45,10,-10),(80,10,10,10)],
    ),
    plan_svg(
        "2BHK Layout",
        [(10,10,150,10),(10,10,10,100),(150,10,150,100),(10,100,150,100),
         (80,10,80,60),(10,60,150,60),(80,60,80,100)],
        [(10,30,10,-10),(10,75,10,-10),(80,35,10,10)],
    ),
    plan_svg(
        "Duplex – GF",
        [(10,10,150,10),(10,10,10,100),(150,10,150,100),(10,100,150,100),
         (10,50,100,50),(100,10,100,100),(100,70,150,70)],
        [(10,30,10,-10),(100,35,-10,10),(100,85,-10,10)],
    ),
    plan_svg(
        "Villa Plan",
        [(10,10,150,10),(10,10,10,100),(150,10,150,100),(10,100,150,100),
         (10,40,90,40),(90,10,90,100),(10,70,90,70),(90,60,150,60)],
        [(10,25,10,-10),(90,25,-10,10),(90,75,-10,10),(10,55,10,-10)],
    ),
    plan_svg(
        "Office Space",
        [(10,10,150,10),(10,10,10,100),(150,10,150,100),(10,100,150,100),
         (10,35,150,35),(60,35,60,100),(60,70,150,70)],
        [(10,22,10,-10),(60,52,-10,10)],
    ),
    plan_svg(
        "Row House",
        [(10,10,150,10),(10,10,10,100),(150,10,150,100),(10,100,150,100),
         (80,10,80,100),(10,55,80,55),(80,45,150,45),(80,75,150,75)],
        [(10,35,10,-10),(80,75,-10,10),(80,25,-10,10)],
    ),
]

# Duplicate for seamless loop
cards_html = ""
for p in plans * 2:
    cards_html += f'<div class="plan-card">{p}</div>'

st.markdown(
    f"""
<div class="map-section">
  <h3>🗺️ Floor Plan Gallery</h3>
  <div style="overflow:hidden; border-radius:8px;">
    <div class="map-track">{cards_html}</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
#  TWO-COLUMN LAYOUT: Complaints + Input
# ══════════════════════════════════════════════════════════════════════════════
col_left, col_right = st.columns([1.1, 0.9], gap="large")

# ── LEFT: Complaints board ──────────────────────────────────────────────────
with col_left:
    sorted_complaints = sort_complaints(st.session_state.complaints)
    items_html = ""
    for c in sorted_complaints:
        dot_cls = f"dot-{c['priority']}"
        badge_cls = f"badge-{c['priority']}"
        items_html += f"""
<div class="complaint-item">
  <div class="priority-dot {dot_cls}"></div>
  <div class="complaint-body">
    <div class="complaint-text">{c['text']}</div>
    <div class="complaint-meta">
      <span>📅 {c['date']}</span>
      <span class="priority-badge {badge_cls}">{c['priority']} priority</span>
    </div>
  </div>
</div>"""

    st.markdown(
        f"""
<div class="complaints-panel">
  <h3>💧 Water Complaints Board</h3>
  {items_html}
</div>
""",
        unsafe_allow_html=True,
    )

# ── RIGHT: Submit complaint ─────────────────────────────────────────────────
with col_right:
    st.markdown(
        '<div class="input-section"><h3>📝 Submit a Water Complaint</h3></div>',
        unsafe_allow_html=True,
    )

    new_complaint = st.text_area(
        "Describe your water issue",
        placeholder="e.g. No water supply since morning! This is totally unacceptable!",
        height=130,
        label_visibility="collapsed",
    )

    if st.button("Submit Complaint →"):
        text = new_complaint.strip()
        if text:
            priority = classify_priority(text)
            st.session_state.complaints.append(
                {
                    "text": text,
                    "priority": priority,
                    "date": datetime.date.today().strftime("%d %b %Y"),
                }
            )
            colour = {"high": "🔴", "medium": "🟡", "low": "🟢"}[priority]
            st.success(f"{colour} Complaint submitted as **{priority.upper()} priority**!")
            time.sleep(0.8)
            st.rerun()
        else:
            st.warning("Please write your complaint before submitting.")

# ══════════════════════════════════════════════════════════════════════════════
#  CHAT ASSISTANT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="chat-section"><h3>🤖 Urban Planning Assistant</h3></div>',
    unsafe_allow_html=True,
)

# render history
for msg in st.session_state.chat_history:
    cls = "bubble-user" if msg["role"] == "user" else "bubble-ai"
    role_label = "You" if msg["role"] == "user" else "Assistant"
    st.markdown(
        f'<div class="chat-bubble {cls}"><div class="bubble-role">{role_label}</div>{msg["content"]}</div>',
        unsafe_allow_html=True,
    )

user_input = st.chat_input("Ask about urban planning, water issues, permits…")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.markdown(
        f'<div class="chat-bubble bubble-user"><div class="bubble-role">You</div>{user_input}</div>',
        unsafe_allow_html=True,
    )

    with st.spinner("Thinking…"):
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=(
                "You are an expert Urban Planning Assistant embedded in a city citizen portal. "
                "You help citizens with water supply complaints, urban infrastructure queries, "
                "building permits, zoning questions, and city services. "
                "Be concise, helpful, and empathetic. Use short paragraphs."
            ),
            messages=st.session_state.chat_history,
        )
        reply = response.content[0].text

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.markdown(
        f'<div class="chat-bubble bubble-ai"><div class="bubble-role">Assistant</div>{reply}</div>',
        unsafe_allow_html=True,
    )
