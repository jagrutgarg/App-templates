import streamlit as st
import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Electricity Complaints Portal",
    page_icon="⚡",
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
    "fire", "electrocuted", "shock", "sparks", "burning", "smoke",
    "explosion", "blast", "short circuit", "no power", "days without",
    "!!!","!!", "dark", "blackout", "outrage",
}
MEDIUM_WORDS = {
    "problem", "issue", "concern", "complaint", "bad", "poor", "delay",
    "slow", "fluctuation", "voltage", "low voltage", "not working", "broken",
    "tripping", "fuse", "transformer", "request", "please fix", "fix",
    "repair", "help", "worried", "notice", "irregular", "inconvenient",
    "missing", "outage", "power cut", "load shedding", "meter",
}

def classify_priority(text: str) -> str:
    lower = text.lower()
    exclamations = text.count("!")
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
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

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d0d !important;
}
[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

/* === DARK STORMY BACKGROUND === */
body::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 160% 50% at 50% 0%,
            rgba(60,60,80,.85) 0%, transparent 65%),
        linear-gradient(180deg, #111118 0%, #0a0a10 50%, #080808 100%);
    z-index: -3;
}

/* === LIGHTNING FLASH OVERLAY === */
.lightning-flash {
    position: fixed;
    inset: 0;
    background: rgba(255,240,100,0);
    z-index: 1;
    pointer-events: none;
    animation: flash 7s ease-in-out infinite;
}
@keyframes flash {
    0%,88%,92%,96%,100% { background: rgba(255,240,100,0); }
    89%   { background: rgba(255,240,100,.12); }
    90%   { background: rgba(255,240,100,.04); }
    91%   { background: rgba(255,240,100,.18); }
    94%   { background: rgba(255,240,100,.08); }
    95%   { background: rgba(255,240,100,.0); }
}

/* === CLOUDS === */
.clouds-layer {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 220px;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}
.cloud {
    position: absolute;
    top: 0;
    border-radius: 50%;
    background: radial-gradient(ellipse, rgba(90,90,105,.65) 0%, rgba(60,60,75,.3) 60%, transparent 100%);
    filter: blur(18px);
    animation: drift linear infinite;
}
.cloud-1  { width:340px;height:100px;top:-20px;left:-60px;animation-duration:40s;animation-delay:0s;opacity:.9; }
.cloud-2  { width:260px;height:80px; top:10px; left:20%;  animation-duration:55s;animation-delay:-12s;opacity:.75;}
.cloud-3  { width:400px;height:120px;top:-30px;left:38%;  animation-duration:48s;animation-delay:-8s; opacity:.85;}
.cloud-4  { width:280px;height:90px; top:15px; left:62%;  animation-duration:62s;animation-delay:-20s;opacity:.7; }
.cloud-5  { width:350px;height:110px;top:-10px;left:80%;  animation-duration:45s;animation-delay:-5s; opacity:.8; }
.cloud-6  { width:200px;height:70px; top:40px; left:50%;  animation-duration:70s;animation-delay:-30s;opacity:.6; }
@keyframes drift {
    from { transform: translateX(0);   }
    to   { transform: translateX(120px); }
}

/* === SVG LIGHTNING BOLTS === */
.bolts-layer {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 260px;
    z-index: 1;
    pointer-events: none;
}
.bolt {
    position: absolute;
    top: 0;
    animation: bolt-flicker ease-in-out infinite;
    filter: drop-shadow(0 0 8px rgba(255,220,50,.9)) drop-shadow(0 0 20px rgba(255,200,0,.6));
}
.bolt svg path { stroke: #ffe033; stroke-width: 2.5; fill: #fff176; }
.bolt-1 { left:12%; animation-duration:6s;  animation-delay:0s;   }
.bolt-2 { left:28%; animation-duration:9s;  animation-delay:-3s;  }
.bolt-3 { left:48%; animation-duration:7s;  animation-delay:-1.5s;}
.bolt-4 { left:66%; animation-duration:11s; animation-delay:-5s;  }
.bolt-5 { left:82%; animation-duration:8s;  animation-delay:-2s;  }
@keyframes bolt-flicker {
    0%,100% { opacity:0; transform:scaleY(1); }
    2%      { opacity:1; transform:scaleY(1.05); }
    4%      { opacity:.3; }
    5%      { opacity:.95; }
    7%      { opacity:0; }
    50%     { opacity:0; }
    52%     { opacity:.8; }
    54%     { opacity:0; }
}

/* === HEADING === */
.elec-heading {
    text-align: center;
    padding: 2.8rem 0 .5rem;
    position: relative;
    z-index: 3;
}
.elec-heading h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem,8vw,6.5rem);
    letter-spacing: .18em;
    color: #ffe033;
    text-shadow:
        0 0 10px rgba(255,224,51,1),
        0 0 30px rgba(255,200,0,.8),
        0 0 70px rgba(255,180,0,.5),
        0 0 120px rgba(255,150,0,.3);
    animation: heading-pulse 3s ease-in-out infinite alternate;
}
@keyframes heading-pulse {
    from { text-shadow: 0 0 10px rgba(255,224,51,1), 0 0 30px rgba(255,200,0,.8), 0 0 70px rgba(255,180,0,.5); }
    to   { text-shadow: 0 0 18px rgba(255,240,100,1), 0 0 50px rgba(255,220,50,1), 0 0 110px rgba(255,200,0,.7), 0 0 200px rgba(255,150,0,.3); }
}
.elec-heading p {
    font-family: 'Barlow', sans-serif;
    font-weight: 300;
    font-size: .9rem;
    letter-spacing: .3em;
    text-transform: uppercase;
    color: rgba(255,224,51,.5);
    margin-top: .3rem;
}

/* === GLASS CARDS === */
.glass-card {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,224,51,.12);
    border-radius: 14px;
    backdrop-filter: blur(10px);
    padding: 1.6rem;
    position: relative;
    z-index: 3;
    box-shadow: 0 4px 40px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.04);
}
.section-title {
    font-family: 'Barlow', sans-serif;
    font-weight: 600;
    font-size: .72rem;
    letter-spacing: .22em;
    text-transform: uppercase;
    color: rgba(255,224,51,.45);
    margin-bottom: 1rem;
}

/* === COMPLAINT CARDS === */
.complaint-card {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    border-left: 3px solid;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: .85rem;
    transition: transform .2s, box-shadow .2s;
}
.complaint-card:hover {
    transform: translateX(3px);
    box-shadow: 0 4px 20px rgba(0,0,0,.4);
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
    animation: dot-pulse 2s ease-in-out infinite;
}
@keyframes dot-pulse {
    0%,100% { transform:scale(1);   opacity:1; }
    50%      { transform:scale(1.4); opacity:.65; }
}
.priority-badge {
    font-family: 'Barlow', sans-serif;
    font-size: .63rem;
    font-weight: 600;
    letter-spacing: .14em;
    text-transform: uppercase;
    padding: .16rem .5rem;
    border-radius: 99px;
    border: 1px solid;
}
.complaint-date {
    font-family: 'Barlow', sans-serif;
    font-size: .7rem;
    color: rgba(255,200,50,.3);
    margin-left: auto;
}
.complaint-text {
    font-family: 'Barlow', sans-serif;
    font-size: .92rem;
    color: rgba(230,220,200,.8);
    line-height: 1.55;
}
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    font-family: 'Barlow', sans-serif;
    color: rgba(255,224,51,.2);
    font-size: .9rem;
    letter-spacing: .06em;
}

/* === STREAMLIT OVERRIDES === */
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,224,51,.2) !important;
    border-radius: 10px !important;
    color: rgba(230,220,190,.9) !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: .95rem !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: rgba(255,224,51,.3) !important; }
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(255,224,51,.55) !important;
    box-shadow: 0 0 0 2px rgba(255,224,51,.1) !important;
}
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #7a5e00, #5a4400) !important;
    border: 1px solid rgba(255,224,51,.35) !important;
    color: #ffe033 !important;
    font-family: 'Barlow', sans-serif !important;
    font-weight: 600 !important;
    font-size: .88rem !important;
    letter-spacing: .14em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: .65rem !important;
    transition: all .25s !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #a07800, #7a5e00) !important;
    box-shadow: 0 0 22px rgba(255,224,51,.3) !important;
    transform: translateY(-1px) !important;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Animated layers ───────────────────────────────────────────────────────────
st.markdown('<div class="lightning-flash"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="clouds-layer">
  <div class="cloud cloud-1"></div>
  <div class="cloud cloud-2"></div>
  <div class="cloud cloud-3"></div>
  <div class="cloud cloud-4"></div>
  <div class="cloud cloud-5"></div>
  <div class="cloud cloud-6"></div>
</div>
""", unsafe_allow_html=True)

BOLT_SVG = """<svg width="28" height="110" viewBox="0 0 28 110" xmlns="http://www.w3.org/2000/svg">
  <path d="M18 0 L4 55 L14 55 L8 110 L26 42 L15 42 Z"
        fill="#fff176" stroke="#ffe033" stroke-width="1.5"
        style="filter:drop-shadow(0 0 6px #ffe033)"/>
</svg>"""

bolts_html = '<div class="bolts-layer">'
bolt_positions = [
    ("bolt-1","12%"), ("bolt-2","28%"), ("bolt-3","48%"),
    ("bolt-4","66%"), ("bolt-5","83%"),
]
for cls, left in bolt_positions:
    bolts_html += f'<div class="bolt {cls}" style="left:{left}">{BOLT_SVG}</div>'
bolts_html += "</div>"
st.markdown(bolts_html, unsafe_allow_html=True)

# ── Thunder sound (Web Audio API) ─────────────────────────────────────────────
st.markdown("""
<script>
(function(){
  const ctx = new (window.AudioContext || window.webkitAudioContext)();

  function thunder() {
    const buf = ctx.createBuffer(1, ctx.sampleRate * 3, ctx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < data.length; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (ctx.sampleRate * .9));
    }
    const src = ctx.createBufferSource();
    src.buffer = buf;

    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 180;

    const gain = ctx.createGain();
    gain.gain.setValueAtTime(.0001, ctx.currentTime);
    gain.gain.linearRampToValueAtTime(.55, ctx.currentTime + .08);
    gain.gain.exponentialRampToValueAtTime(.0001, ctx.currentTime + 2.8);

    src.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);
    src.start();

    // crackle
    for(let k=0;k<3;k++){
      setTimeout(()=>{
        const c = ctx.createOscillator();
        const cg = ctx.createGain();
        c.connect(cg); cg.connect(ctx.destination);
        c.type='sawtooth';
        c.frequency.value = 60 + Math.random()*40;
        cg.gain.setValueAtTime(.18, ctx.currentTime);
        cg.gain.exponentialRampToValueAtTime(.0001, ctx.currentTime+.12);
        c.start(); c.stop(ctx.currentTime+.12);
      }, k*180 + Math.random()*120);
    }

    const next = 6000 + Math.random() * 9000;
    setTimeout(thunder, next);
  }

  function start(){
    if(ctx.state==='suspended') ctx.resume();
    setTimeout(thunder, 800);
    document.removeEventListener('click', start);
  }
  document.addEventListener('click', start, {once:true});
  setTimeout(()=>{ if(ctx.state!=='suspended') thunder(); }, 1200);
})();
</script>
""", unsafe_allow_html=True)

# ── Heading ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="elec-heading">
  <h1>⚡ ELECTRICITY</h1>
  <p>Complaints &amp; Grievance Portal</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
col_form, col_list = st.columns([1, 1.6], gap="large")

# ── LEFT: form ────────────────────────────────────────────────────────────────
with col_form:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📝 Submit a Complaint</p>', unsafe_allow_html=True)

    complaint_text = st.text_area(
        label="",
        placeholder="Describe your electricity-related issue here…\n\nE.g. power cut, voltage fluctuation, sparks, meter issue, etc.\nThe system auto-detects severity from your message.",
        height=185,
        key="complaint_input",
        label_visibility="collapsed",
    )

    submitted = st.button("⚡ Submit Complaint", use_container_width=True)

    if submitted:
        text = complaint_text.strip()
        if text:
            priority = classify_priority(text)
            st.session_state.complaints.append({
                "text": text,
                "priority": priority,
                "date": datetime.datetime.now(),
            })
            st.success("✅ Complaint submitted successfully!")
            st.rerun()
        else:
            st.warning("⚠️ Please enter your complaint before submitting.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Barlow',sans-serif;font-size:.78rem;color:rgba(255,224,51,.4);">
      <p style="margin-bottom:.5rem;letter-spacing:.12em;text-transform:uppercase;font-size:.66rem;">Priority Guide</p>
      <div style="display:flex;flex-direction:column;gap:.38rem;">
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#ef4444;box-shadow:0 0 7px #ef4444;flex-shrink:0;"></span>
          <span><b style="color:rgba(239,68,68,.9);">High</b> — Angry, urgent, hazardous keywords</span>
        </div>
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#f59e0b;box-shadow:0 0 7px #f59e0b;flex-shrink:0;"></span>
          <span><b style="color:rgba(245,158,11,.9);">Medium</b> — Outage, fluctuation, meter issues</span>
        </div>
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#22c55e;box-shadow:0 0 7px #22c55e;flex-shrink:0;"></span>
          <span><b style="color:rgba(34,197,94,.9);">Low</b> — General queries or suggestions</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT: complaints list ────────────────────────────────────────────────────
with col_list:
    st.markdown('<div class="glass-card" style="min-height:430px">', unsafe_allow_html=True)

    sorted_complaints = sorted(
        st.session_state.complaints,
        key=lambda x: (PRIORITY_ORDER[x["priority"]], x["date"]),
    )
    total  = len(sorted_complaints)
    counts = {p: sum(1 for c in sorted_complaints if c["priority"] == p) for p in ["high","medium","low"]}

    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
                margin-bottom:1.2rem;flex-wrap:wrap;gap:.5rem;">
      <p class="section-title" style="margin-bottom:0;">📋 Complaints Log</p>
      <div style="display:flex;gap:.6rem;font-family:'Barlow',sans-serif;font-size:.72rem;">
        <span style="color:rgba(239,68,68,.85);">● {counts['high']} High</span>
        <span style="color:rgba(245,158,11,.85);">● {counts['medium']} Medium</span>
        <span style="color:rgba(34,197,94,.85);">● {counts['low']} Low</span>
        <span style="color:rgba(255,224,51,.3);">| {total} Total</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not sorted_complaints:
        st.markdown("""
        <div class="empty-state">
          <div style="font-size:2.5rem;margin-bottom:.8rem;">⚡</div>
          <div>No complaints yet.<br>Raise an electricity issue above.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for c in sorted_complaints:
            p     = c["priority"]
            color = PRIORITY_COLOR[p]
            label = PRIORITY_LABEL[p]
            date_str  = c["date"].strftime("%d %b %Y · %I:%M %p")
            safe_text = c["text"].replace("<","&lt;").replace(">","&gt;")

            bg = {
                "high":   "rgba(239,68,68,.07)",
                "medium": "rgba(245,158,11,.07)",
                "low":    "rgba(34,197,94,.07)",
            }[p]

            st.markdown(f"""
            <div class="complaint-card" style="border-left-color:{color};">
              <div class="complaint-header">
                <span class="priority-dot"
                      style="background:{color};box-shadow:0 0 8px {color};"></span>
                <span class="priority-badge"
                      style="color:{color};border-color:{color};background:{bg};">
                  {label} Priority
                </span>
                <span class="complaint-date">{date_str}</span>
              </div>
              <p class="complaint-text">{safe_text}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2rem;font-family:'Barlow',sans-serif;
            font-size:.72rem;color:rgba(255,224,51,.2);letter-spacing:.1em;">
  ⚡ Click anywhere to enable ambient thunder sounds
</div>
""", unsafe_allow_html=True)
