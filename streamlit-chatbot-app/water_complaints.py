import streamlit as st
import datetime
import re
import math

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Water Complaints Portal",
    page_icon="💧",
    layout="wide",
)

# ── Session state ─────────────────────────────────────────────────────────────
if "complaints" not in st.session_state:
    st.session_state.complaints = []

# ── Priority classifier ───────────────────────────────────────────────────────
HIGH_WORDS = {
    "angry", "furious", "outraged", "disgusting", "pathetic", "useless",
    "terrible", "horrible", "awful", "unacceptable", "demand", "immediately",
    "urgent", "emergency", "intolerable", "worst", "disgrace", "shameful",
    "absurd", "ridiculous", "frustrated", "fed up", "sick", "hate",
    "never", "always", "enough", "serious", "dangerous", "death",
    "disease", "contaminated", "filthy", "dirty", "poison", "toxic",
    "!!!","!!", "no water", "days without",
}
MEDIUM_WORDS = {
    "problem", "issue", "concern", "complaint", "bad", "poor", "delay",
    "slow", "shortage", "supply", "low pressure", "not working", "broken",
    "leak", "request", "please fix", "fix", "repair", "help",
    "worried", "notice", "irregular", "inconvenient", "missing",
}


def classify_priority(text: str) -> str:
    lower = text.lower()
    exclamations = text.count("!")
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)

    # anger signals
    anger_score = 0
    for w in HIGH_WORDS:
        if w in lower:
            anger_score += 2
    anger_score += exclamations
    anger_score += int(caps_ratio > 0.4) * 3

    if anger_score >= 4:
        return "high"

    medium_score = sum(1 for w in MEDIUM_WORDS if w in lower)
    if medium_score >= 1 or exclamations >= 1:
        return "medium"

    return "low"


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
PRIORITY_COLOR = {"high": "#ef4444", "medium": "#f59e0b", "low": "#22c55e"}
PRIORITY_LABEL = {"high": "High", "medium": "Medium", "low": "Low"}

# ── Global CSS + animations ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;600&display=swap');

/* ---------- reset / base ---------- */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a1628 !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

/* ---------- animated water background ---------- */
body::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 120% 60% at 50% 110%,
            rgba(0,120,200,.35) 0%, transparent 70%),
        linear-gradient(170deg, #0a1628 0%, #0c2444 40%, #0e3060 100%);
    z-index: -2;
}

/* Ripple circles */
body::after {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(circle 1px at 20% 80%, rgba(100,200,255,.5) 0%, transparent 100%),
        radial-gradient(circle 1px at 75% 60%, rgba(100,200,255,.4) 0%, transparent 100%),
        radial-gradient(circle 1px at 50% 90%, rgba(100,200,255,.6) 0%, transparent 100%);
    z-index: -1;
    animation: pulse-bg 8s ease-in-out infinite alternate;
}

@keyframes pulse-bg {
    0%   { opacity:.6; transform: scaleX(1) scaleY(1); }
    100% { opacity:1;  transform: scaleX(1.02) scaleY(1.05); }
}

/* ---------- floating droplets ---------- */
.droplets-container {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.drop {
    position: absolute;
    bottom: -30px;
    width: 6px;
    height: 10px;
    border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
    background: rgba(120,210,255,.55);
    filter: blur(.5px);
    animation: float-drop linear infinite;
}

@keyframes float-drop {
    0%   { transform: translateY(0) scale(1);   opacity:.7; }
    80%  { opacity:.5; }
    100% { transform: translateY(-105vh) scale(.6); opacity:0; }
}

/* ---------- heading ---------- */
.water-heading {
    text-align: center;
    padding: 2.2rem 0 .4rem;
    position: relative;
    z-index: 2;
}
.water-heading h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 7vw, 5.5rem);
    font-weight: 700;
    letter-spacing: .08em;
    background: linear-gradient(135deg, #93e8ff 0%, #4fc3f7 40%, #81d4fa 80%, #ffffff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    filter: drop-shadow(0 0 24px rgba(79,195,247,.6));
    animation: shimmer-text 4s ease-in-out infinite alternate;
}
@keyframes shimmer-text {
    from { filter: drop-shadow(0 0 18px rgba(79,195,247,.5)); }
    to   { filter: drop-shadow(0 0 36px rgba(147,232,255,.9)); }
}
.water-heading p {
    font-family: 'Lato', sans-serif;
    font-weight: 300;
    font-size: 1rem;
    letter-spacing: .25em;
    text-transform: uppercase;
    color: rgba(147,232,255,.7);
    margin-top: .3rem;
}

/* ---------- cards / panels ---------- */
.glass-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(147,232,255,.15);
    border-radius: 16px;
    backdrop-filter: blur(12px);
    padding: 1.6rem;
    position: relative;
    z-index: 2;
    box-shadow: 0 4px 32px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.06);
}

.section-title {
    font-family: 'Lato', sans-serif;
    font-weight: 600;
    font-size: .75rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: rgba(147,232,255,.55);
    margin-bottom: 1rem;
}

/* ---------- complaint cards ---------- */
.complaint-card {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.07);
    border-left: 3px solid;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: .85rem;
    transition: transform .2s, box-shadow .2s;
    position: relative;
}
.complaint-card:hover {
    transform: translateX(3px);
    box-shadow: 0 4px 20px rgba(0,0,0,.3);
}

.complaint-header {
    display: flex;
    align-items: center;
    gap: .6rem;
    margin-bottom: .5rem;
}
.priority-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 0 8px currentColor;
    animation: dot-pulse 2s ease-in-out infinite;
}
@keyframes dot-pulse {
    0%,100% { transform: scale(1);   opacity:1; }
    50%      { transform: scale(1.3); opacity:.7; }
}
.priority-badge {
    font-family: 'Lato', sans-serif;
    font-size: .65rem;
    font-weight: 600;
    letter-spacing: .15em;
    text-transform: uppercase;
    padding: .18rem .55rem;
    border-radius: 99px;
    border: 1px solid;
}
.complaint-date {
    font-family: 'Lato', sans-serif;
    font-size: .72rem;
    color: rgba(200,230,255,.4);
    margin-left: auto;
}
.complaint-text {
    font-family: 'Lato', sans-serif;
    font-size: .92rem;
    color: rgba(220,240,255,.82);
    line-height: 1.55;
}

/* ---------- empty state ---------- */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    font-family: 'Lato', sans-serif;
    color: rgba(147,232,255,.3);
    font-size: .9rem;
    letter-spacing: .05em;
}

/* ---------- Streamlit widget overrides ---------- */
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,.05) !important;
    border: 1px solid rgba(147,232,255,.25) !important;
    border-radius: 10px !important;
    color: rgba(220,240,255,.9) !important;
    font-family: 'Lato', sans-serif !important;
    font-size: .95rem !important;
    resize: vertical;
}
[data-testid="stTextArea"] textarea::placeholder {
    color: rgba(147,232,255,.35) !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(79,195,247,.6) !important;
    box-shadow: 0 0 0 2px rgba(79,195,247,.15) !important;
}

/* submit button */
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #1565c0, #0d47a1) !important;
    border: 1px solid rgba(79,195,247,.4) !important;
    color: #e3f2fd !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 600 !important;
    font-size: .9rem !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: .65rem !important;
    transition: all .25s !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #1976d2, #1565c0) !important;
    box-shadow: 0 0 20px rgba(79,195,247,.35) !important;
    transform: translateY(-1px) !important;
}

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Floating droplets (HTML) ──────────────────────────────────────────────────
drops_html = '<div class="droplets-container">'
configs = [
    (8,  6,  "8px","12px","12s","0s"),
    (18, 40, "5px","8px", "15s","3s"),
    (30, 70, "7px","11px","10s","1s"),
    (45, 20, "4px","7px", "18s","6s"),
    (55, 85, "6px","10px","13s","2s"),
    (68, 50, "5px","9px", "16s","4s"),
    (78, 10, "8px","13px","11s","7s"),
    (88, 65, "4px","6px", "20s","5s"),
    (25, 90, "6px","10px","14s","9s"),
    (60, 35, "5px","8px", "17s","8s"),
    (12, 55, "7px","11px","12s","1.5s"),
    (92, 78, "4px","7px", "19s","3.5s"),
]
for lft, bot_off, w, h, dur, delay in configs:
    drops_html += (
        f'<div class="drop" style="left:{lft}%;bottom:{bot_off}px;'
        f'width:{w};height:{h};animation-duration:{dur};animation-delay:{delay};'
        f'opacity:{0.3+lft/200:.2f}"></div>'
    )
drops_html += "</div>"
st.markdown(drops_html, unsafe_allow_html=True)

# ── Drop sound (Web Audio API) ────────────────────────────────────────────────
st.markdown("""
<script>
(function(){
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  function playDrop() {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain); gain.connect(ctx.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(880, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(220, ctx.currentTime + .18);
    gain.gain.setValueAtTime(.08, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(.0001, ctx.currentTime + .25);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + .25);
    const next = 2.5 + Math.random() * 4;
    setTimeout(playDrop, next * 1000);
  }
  document.addEventListener('click', function resume(){
    if(ctx.state==='suspended') ctx.resume();
    setTimeout(playDrop, 500);
    document.removeEventListener('click', resume);
  }, {once:true});
  // also try auto-start
  setTimeout(()=>{ if(ctx.state!=='suspended') playDrop(); }, 1000);
})();
</script>
""", unsafe_allow_html=True)

# ── Heading ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="water-heading">
  <h1>💧 Water</h1>
  <p>Complaints &amp; Grievance Portal</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Layout: two columns ───────────────────────────────────────────────────────
col_form, col_list = st.columns([1, 1.6], gap="large")

# ── LEFT: complaint form ──────────────────────────────────────────────────────
with col_form:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📝 Submit a Complaint</p>', unsafe_allow_html=True)

    complaint_text = st.text_area(
        label="",
        placeholder="Describe your water-related issue here…\n\nTip: The system auto-detects priority based on urgency and tone.",
        height=180,
        key="complaint_input",
        label_visibility="collapsed",
    )

    submitted = st.button("Submit Complaint", use_container_width=True)

    if submitted:
        text = complaint_text.strip()
        if text:
            priority = classify_priority(text)
            entry = {
                "text": text,
                "priority": priority,
                "date": datetime.datetime.now(),
            }
            st.session_state.complaints.append(entry)
            st.success("✅ Complaint submitted successfully!")
            st.rerun()
        else:
            st.warning("⚠️ Please enter your complaint before submitting.")

    # legend
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Lato',sans-serif;font-size:.78rem;color:rgba(147,232,255,.5);">
      <p style="margin-bottom:.4rem;letter-spacing:.1em;text-transform:uppercase;font-size:.68rem;">Priority Guide</p>
      <div style="display:flex;flex-direction:column;gap:.35rem;">
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#ef4444;box-shadow:0 0 6px #ef4444;flex-shrink:0;"></span>
          <span><b style="color:rgba(239,68,68,.9);">High</b> — Angry, urgent, health-risk language</span>
        </div>
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#f59e0b;box-shadow:0 0 6px #f59e0b;flex-shrink:0;"></span>
          <span><b style="color:rgba(245,158,11,.9);">Medium</b> — Problems, leaks, supply issues</span>
        </div>
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#22c55e;box-shadow:0 0 6px #22c55e;flex-shrink:0;"></span>
          <span><b style="color:rgba(34,197,94,.9);">Low</b> — General feedback or suggestions</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT: complaints list ────────────────────────────────────────────────────
with col_list:
    st.markdown('<div class="glass-card" style="min-height:420px">', unsafe_allow_html=True)

    sorted_complaints = sorted(
        st.session_state.complaints,
        key=lambda x: (PRIORITY_ORDER[x["priority"]], x["date"]),
    )

    total = len(sorted_complaints)
    counts = {p: sum(1 for c in sorted_complaints if c["priority"] == p) for p in ["high","medium","low"]}

    header_html = f"""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.2rem;flex-wrap:wrap;gap:.5rem;">
      <p class="section-title" style="margin-bottom:0;">📋 Complaints Log</p>
      <div style="display:flex;gap:.6rem;font-family:'Lato',sans-serif;font-size:.72rem;">
        <span style="color:rgba(239,68,68,.85);">● {counts['high']} High</span>
        <span style="color:rgba(245,158,11,.85);">● {counts['medium']} Medium</span>
        <span style="color:rgba(34,197,94,.85);">● {counts['low']} Low</span>
        <span style="color:rgba(147,232,255,.4);">| {total} Total</span>
      </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    if not sorted_complaints:
        st.markdown("""
        <div class="empty-state">
          <div style="font-size:2.5rem;margin-bottom:.8rem;">💧</div>
          <div>No complaints yet.<br>Be the first to raise an issue.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for c in sorted_complaints:
            p = c["priority"]
            color = PRIORITY_COLOR[p]
            label = PRIORITY_LABEL[p]
            date_str = c["date"].strftime("%d %b %Y · %I:%M %p")
            safe_text = c["text"].replace("<","&lt;").replace(">","&gt;")

            card_html = f"""
            <div class="complaint-card" style="border-left-color:{color};">
              <div class="complaint-header">
                <span class="priority-dot" style="background:{color};color:{color};"></span>
                <span class="priority-badge" style="color:{color};border-color:{color};background:{'rgba(239,68,68,.08)' if p=='high' else 'rgba(245,158,11,.08)' if p=='medium' else 'rgba(34,197,94,.08)'};">{label} Priority</span>
                <span class="complaint-date">{date_str}</span>
              </div>
              <p class="complaint-text">{safe_text}</p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer tip ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2rem;font-family:'Lato',sans-serif;
            font-size:.72rem;color:rgba(147,232,255,.25);letter-spacing:.1em;">
  💧 Click anywhere to enable ambient water drop sounds
</div>
""", unsafe_allow_html=True)
