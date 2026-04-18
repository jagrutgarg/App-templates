import streamlit as st
import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Roads Complaints Portal",
    page_icon="🛣️",
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
    "accident", "injured", "death", "killed", "dangerous", "fatal",
    "broken axle", "tire burst", "fell", "collapsed", "flood", "sinking",
    "!!!", "!!", "no road", "impossible", "disaster", "catastrophe", "helpless",
    "months", "years", "nobody", "nothing done", "ignored",
}
MEDIUM_WORDS = {
    "pothole", "crater", "hole", "bump", "broken", "damaged", "cracked",
    "repair", "fix", "problem", "issue", "concern", "complaint", "bad",
    "poor", "delay", "waterlogging", "flooding", "uneven", "rough",
    "no signal", "streetlight", "divider", "footpath", "drainage",
    "speed breaker", "marking", "missing", "encroachment", "garbage",
    "dust", "mud", "slippery", "narrow", "blocked",
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

# ── Full CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Nunito:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #1a1a0a !important;
}
[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

/* ── sky background ── */
body::before {
    content: "";
    position: fixed; inset: 0;
    background: linear-gradient(180deg,
        #0f1a05 0%, #1c2e08 30%, #2a3d0a 55%,
        #1a1a0a 75%, #111108 100%);
    z-index: -3;
}

/* ── stars ── */
body::after {
    content: "";
    position: fixed; inset: 0;
    background-image:
        radial-gradient(1px 1px at 10% 15%, rgba(255,255,220,.7), transparent),
        radial-gradient(1px 1px at 25% 8%,  rgba(255,255,220,.5), transparent),
        radial-gradient(1px 1px at 42% 20%, rgba(255,255,220,.6), transparent),
        radial-gradient(1px 1px at 60% 5%,  rgba(255,255,220,.4), transparent),
        radial-gradient(1px 1px at 75% 18%, rgba(255,255,220,.7), transparent),
        radial-gradient(1px 1px at 88% 10%, rgba(255,255,220,.5), transparent),
        radial-gradient(1px 1px at 5%  30%, rgba(255,255,220,.3), transparent),
        radial-gradient(1px 1px at 92% 25%, rgba(255,255,220,.6), transparent);
    z-index: -2;
}

/* ── HEADING ── */
.roads-heading {
    text-align: center;
    padding: 1.6rem 0 .3rem;
    position: relative; z-index: 3;
}
.roads-heading h1 {
    font-family: 'Black Han Sans', sans-serif;
    font-size: clamp(3rem, 7vw, 5.8rem);
    letter-spacing: .12em;
    color: #f5c842;
    text-shadow:
        0 2px 0 #a07800,
        0 0 18px rgba(245,200,66,.6),
        0 0 50px rgba(245,180,50,.3);
    animation: sign-sway 5s ease-in-out infinite alternate;
    display: inline-block;
}
@keyframes sign-sway {
    from { transform: rotate(-1deg); text-shadow: 0 2px 0 #a07800, 0 0 14px rgba(245,200,66,.5); }
    to   { transform: rotate(1deg);  text-shadow: 0 2px 0 #a07800, 0 0 28px rgba(245,200,66,.9); }
}
.roads-heading p {
    font-family: 'Nunito', sans-serif;
    font-weight: 300;
    font-size: .88rem;
    letter-spacing: .28em;
    text-transform: uppercase;
    color: rgba(245,200,66,.45);
    margin-top: .3rem;
}

/* ── ANIMATION SCENE ── */
.scene-wrapper {
    position: relative; z-index: 2;
    margin: .5rem auto 1.2rem;
    max-width: 860px;
    height: 140px;
    overflow: hidden;
    border-radius: 12px;
    background: linear-gradient(180deg, #1e2d06 0%, #141f04 40%, #0d1302 100%);
    border: 1px solid rgba(245,200,66,.1);
    box-shadow: 0 4px 30px rgba(0,0,0,.6);
}

/* road surface */
.road {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 58px;
    background: #2a2a2a;
    border-top: 3px solid #444;
}
/* road texture */
.road::before {
    content: "";
    position: absolute; inset: 0;
    background: repeating-linear-gradient(
        90deg,
        transparent 0px, transparent 38px,
        rgba(255,255,255,.06) 38px, rgba(255,255,255,.06) 40px
    );
}
/* dashed centre line */
.road::after {
    content: "";
    position: absolute;
    top: 50%; left: 0; right: 0;
    height: 3px;
    background: repeating-linear-gradient(
        90deg,
        #f5c842 0px, #f5c842 28px,
        transparent 28px, transparent 54px
    );
    transform: translateY(-50%);
    animation: dash-scroll 1.2s linear infinite;
}
@keyframes dash-scroll {
    from { background-position: 0 0; }
    to   { background-position: -54px 0; }
}

/* grass strip */
.grass {
    position: absolute;
    bottom: 58px; left: 0; right: 0;
    height: 14px;
    background: linear-gradient(180deg, #2d4a08 0%, #1e3305 100%);
    border-top: 2px solid #3a5c0a;
}

/* kerb */
.kerb {
    position: absolute;
    bottom: 55px; left: 0; right: 0;
    height: 5px;
    background: repeating-linear-gradient(
        90deg,
        #e0e0e0 0px, #e0e0e0 14px,
        #c00 14px, #c00 28px
    );
    opacity: .6;
}

/* potholes */
.pothole {
    position: absolute;
    bottom: 60px;
    border-radius: 50%;
    background: radial-gradient(ellipse, #111 30%, #1e1e1e 70%, transparent 100%);
    border: 2px solid #333;
    box-shadow: inset 0 3px 8px rgba(0,0,0,.8), 0 1px 2px rgba(0,0,0,.5);
}
.ph1 { width:36px; height:18px; left:18%;  animation: ph-appear 8s  linear infinite; }
.ph2 { width:28px; height:14px; left:42%;  animation: ph-appear 8s  linear infinite; animation-delay:-2.5s; }
.ph3 { width:44px; height:20px; left:68%;  animation: ph-appear 8s  linear infinite; animation-delay:-5s; }
.ph4 { width:24px; height:12px; left:83%;  animation: ph-appear 10s linear infinite; animation-delay:-1s; }

@keyframes ph-appear {
    0%   { transform: scaleX(0); opacity:0; }
    8%   { transform: scaleX(1); opacity:1; }
    85%  { opacity:1; }
    100% { opacity:0; }
}

/* debris around holes */
.debris {
    position: absolute;
    bottom: 72px;
    width: 60px; height: 8px;
    background: radial-gradient(ellipse, #5a4a2a 0%, transparent 70%);
    border-radius: 50%;
    opacity: .5;
}
.db1 { left:16%; animation: ph-appear 8s linear infinite; animation-delay:.3s; }
.db2 { left:40%; animation: ph-appear 8s linear infinite; animation-delay:-2.2s; }
.db3 { left:65%; animation: ph-appear 8s linear infinite; animation-delay:-4.7s; }

/* ── CAR ── */
.car-wrap {
    position: absolute;
    bottom: 58px;
    left: -120px;
    animation: car-drive 8s linear infinite;
    transform-origin: center bottom;
}
@keyframes car-drive {
    0%   { left: -120px; transform: rotate(0deg) translateY(0); }
    28%  { left:  28%;   transform: rotate(0deg) translateY(0); }
    /* approach pothole 1 */
    32%  { left:  32%;   transform: rotate(-2deg) translateY(2px); }
    34%  { left:  34%;   transform: rotate(4deg) translateY(8px); }  /* STUCK */
    38%  { left:  36%;   transform: rotate(-3deg) translateY(4px); }
    42%  { left:  40%;   transform: rotate(1deg) translateY(0); }
    /* approach pothole 2 */
    58%  { left:  58%;   transform: rotate(0deg) translateY(0); }
    61%  { left:  61%;   transform: rotate(-3deg) translateY(6px); } /* STUCK */
    65%  { left:  64%;   transform: rotate(2deg) translateY(0); }
    90%  { left: 110%;   transform: rotate(0deg) translateY(0); }
    100% { left: 110%;   transform: rotate(0deg) translateY(0); }
}

/* car body SVG wrapper */
.car-svg { display:block; }

/* headlight beam */
.headlight {
    position: absolute;
    right: -55px; top: 14px;
    width: 55px; height: 20px;
    background: linear-gradient(90deg, rgba(255,240,180,.45), transparent);
    clip-path: polygon(0 40%, 100% 0%, 100% 100%, 0 60%);
    border-radius: 0 8px 8px 0;
    animation: light-flicker 0.15s ease-in-out infinite alternate;
}
@keyframes light-flicker {
    from { opacity:.85; }
    to   { opacity:1; }
}

/* dust puffs when stuck */
.dust {
    position: absolute;
    bottom: 56px;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: rgba(180,150,90,.5);
    filter: blur(3px);
    pointer-events: none;
    opacity: 0;
    animation: dust-puff 8s linear infinite;
}
.d1 { left:31%; animation-delay:2.7s; }
.d2 { left:29%; animation-delay:2.9s; width:7px;height:7px; }
.d3 { left:59%; animation-delay:4.9s; }
.d4 { left:57%; animation-delay:5.1s; width:8px;height:8px; }
@keyframes dust-puff {
    0%,30%,100% { opacity:0; transform: translateY(0) scale(1); }
    32% { opacity:.7; transform: translateY(-6px) scale(1.5); }
    36% { opacity:0; transform: translateY(-14px) scale(2.5); }
}

/* trees */
.tree {
    position: absolute;
    bottom: 72px;
    pointer-events: none;
}
.tree::before {  /* trunk */
    content: "";
    position: absolute;
    bottom: 0; left: 50%;
    transform: translateX(-50%);
    width: 5px; height: 14px;
    background: #5a3a1a;
    border-radius: 2px;
}
.tree::after {   /* leaves */
    content: "";
    position: absolute;
    bottom: 10px; left: 50%;
    transform: translateX(-50%);
    width: 22px; height: 28px;
    background: radial-gradient(ellipse, #2a5a0a 40%, #1a3d06 100%);
    border-radius: 50% 50% 45% 45%;
    box-shadow: 0 -3px 6px rgba(0,0,0,.3);
}
.tree-1 { left: 3%;  }
.tree-2 { left: 12%; }
.tree-3 { left: 52%; }
.tree-4 { left: 73%; }
.tree-5 { left: 91%; }

/* warning sign */
.warn-sign {
    position: absolute;
    bottom: 72px;
    font-size: .7rem;
    color: #f5c842;
    text-shadow: 0 0 6px rgba(245,200,66,.8);
    animation: sign-bob 2s ease-in-out infinite alternate;
}
.ws1 { left:24%; }
.ws2 { left:48%; }
@keyframes sign-bob {
    from { transform: translateY(0); }
    to   { transform: translateY(-3px); }
}

/* ── GLASS CARDS ── */
.glass-card {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(245,200,66,.12);
    border-radius: 14px;
    backdrop-filter: blur(10px);
    padding: 1.6rem;
    position: relative; z-index: 3;
    box-shadow: 0 4px 40px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.04);
}
.section-title {
    font-family: 'Nunito', sans-serif;
    font-weight: 600;
    font-size: .72rem;
    letter-spacing: .22em;
    text-transform: uppercase;
    color: rgba(245,200,66,.45);
    margin-bottom: 1rem;
}

/* ── COMPLAINT CARDS ── */
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
    display: flex; align-items: center;
    gap: .6rem; margin-bottom: .5rem;
}
.priority-dot {
    width: 10px; height: 10px;
    border-radius: 50%; flex-shrink: 0;
    animation: dot-pulse 2s ease-in-out infinite;
}
@keyframes dot-pulse {
    0%,100% { transform:scale(1);   opacity:1; }
    50%      { transform:scale(1.4); opacity:.65; }
}
.priority-badge {
    font-family: 'Nunito', sans-serif;
    font-size: .63rem; font-weight: 700;
    letter-spacing: .14em; text-transform: uppercase;
    padding: .16rem .5rem;
    border-radius: 99px; border: 1px solid;
}
.complaint-date {
    font-family: 'Nunito', sans-serif;
    font-size: .7rem;
    color: rgba(245,200,66,.3);
    margin-left: auto;
}
.complaint-text {
    font-family: 'Nunito', sans-serif;
    font-size: .92rem;
    color: rgba(230,220,190,.8);
    line-height: 1.55;
}
.empty-state {
    text-align: center; padding: 3rem 1rem;
    font-family: 'Nunito', sans-serif;
    color: rgba(245,200,66,.22); font-size: .9rem;
    letter-spacing: .05em;
}

/* ── STREAMLIT OVERRIDES ── */
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(245,200,66,.2) !important;
    border-radius: 10px !important;
    color: rgba(230,220,190,.9) !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: .95rem !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: rgba(245,200,66,.3) !important; }
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(245,200,66,.5) !important;
    box-shadow: 0 0 0 2px rgba(245,200,66,.1) !important;
}
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #5a4200, #3d2d00) !important;
    border: 1px solid rgba(245,200,66,.35) !important;
    color: #f5c842 !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: .88rem !important;
    letter-spacing: .14em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: .65rem !important;
    transition: all .25s !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #7a5800, #5a4200) !important;
    box-shadow: 0 0 22px rgba(245,200,66,.28) !important;
    transform: translateY(-1px) !important;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Road Animation Scene ───────────────────────────────────────────────────────
car_svg = """
<svg class="car-svg" width="88" height="42" viewBox="0 0 88 42" xmlns="http://www.w3.org/2000/svg">
  <!-- shadow -->
  <ellipse cx="44" cy="41" rx="34" ry="4" fill="rgba(0,0,0,.4)"/>
  <!-- body -->
  <rect x="4" y="18" width="80" height="20" rx="5" fill="#c0392b"/>
  <!-- cabin -->
  <path d="M18 18 Q22 4 38 4 L58 4 Q72 4 74 18 Z" fill="#a93226"/>
  <!-- cabin shine -->
  <path d="M24 16 Q27 7 36 6 L46 6 Q58 6 62 16 Z" fill="rgba(255,255,255,.15)" rx="2"/>
  <!-- windows -->
  <rect x="22" y="7" width="18" height="10" rx="2" fill="#7ec8e3" opacity=".85"/>
  <rect x="44" y="7" width="18" height="10" rx="2" fill="#7ec8e3" opacity=".85"/>
  <!-- window shine -->
  <rect x="23" y="8"  width="5" height="3" rx="1" fill="rgba(255,255,255,.4)"/>
  <rect x="45" y="8"  width="5" height="3" rx="1" fill="rgba(255,255,255,.4)"/>
  <!-- headlights -->
  <ellipse cx="82" cy="27" rx="4" ry="3" fill="#fffacd" opacity=".9"/>
  <ellipse cx="82" cy="27" rx="3" ry="2" fill="#fff" opacity=".6"/>
  <!-- tail lights -->
  <ellipse cx="6"  cy="27" rx="3" ry="2.5" fill="#e74c3c" opacity=".9"/>
  <!-- wheels -->
  <circle cx="20" cy="38" r="8" fill="#222"/>
  <circle cx="20" cy="38" r="5" fill="#444"/>
  <circle cx="20" cy="38" r="2" fill="#888"/>
  <circle cx="66" cy="38" r="8" fill="#222"/>
  <circle cx="66" cy="38" r="5" fill="#444"/>
  <circle cx="66" cy="38" r="2" fill="#888"/>
  <!-- door line -->
  <line x1="42" y1="19" x2="42" y2="37" stroke="#9b1c1c" stroke-width="1.5" opacity=".6"/>
  <!-- door handle -->
  <rect x="34" y="27" width="6" height="2" rx="1" fill="#888" opacity=".7"/>
  <rect x="48" y="27" width="6" height="2" rx="1" fill="#888" opacity=".7"/>
  <!-- roof rack -->
  <rect x="22" y="3" width="42" height="2" rx="1" fill="#8b1c1c" opacity=".6"/>
</svg>
"""

scene_html = f"""
<div class="scene-wrapper">
  <!-- sky / ground gradient handled by scene-wrapper bg -->
  <!-- trees -->
  <div class="tree tree-1"></div>
  <div class="tree tree-2"></div>
  <div class="tree tree-3"></div>
  <div class="tree tree-4"></div>
  <div class="tree tree-5"></div>
  <!-- warning signs -->
  <div class="warn-sign ws1">⚠</div>
  <div class="warn-sign ws2">⚠</div>
  <!-- grass -->
  <div class="grass"></div>
  <!-- kerb -->
  <div class="kerb"></div>
  <!-- road -->
  <div class="road"></div>
  <!-- potholes -->
  <div class="pothole ph1"></div>
  <div class="pothole ph2"></div>
  <div class="pothole ph3"></div>
  <div class="pothole ph4"></div>
  <!-- debris -->
  <div class="debris db1"></div>
  <div class="debris db2"></div>
  <div class="debris db3"></div>
  <!-- dust puffs -->
  <div class="dust d1"></div>
  <div class="dust d2"></div>
  <div class="dust d3"></div>
  <div class="dust d4"></div>
  <!-- car -->
  <div class="car-wrap">
    <div class="headlight"></div>
    {car_svg}
  </div>
</div>
"""
st.markdown(scene_html, unsafe_allow_html=True)

# ── Audio: engine hum + pothole thud ─────────────────────────────────────────
st.markdown("""
<script>
(function(){
  const ctx = new (window.AudioContext || window.webkitAudioContext)();

  /* ---- continuous engine hum ---- */
  function startEngine() {
    const osc = ctx.createOscillator();
    const osc2 = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();

    osc.type  = 'sawtooth'; osc.frequency.value  = 82;
    osc2.type = 'square';   osc2.frequency.value = 41;
    filter.type = 'lowpass'; filter.frequency.value = 320;
    gain.gain.value = 0.045;

    osc.connect(filter); osc2.connect(filter);
    filter.connect(gain); gain.connect(ctx.destination);
    osc.start(); osc2.start();

    /* slight RPM wobble */
    setInterval(() => {
      const rpm = 78 + Math.random() * 10;
      osc.frequency.setTargetAtTime(rpm, ctx.currentTime, .15);
      osc2.frequency.setTargetAtTime(rpm/2, ctx.currentTime, .15);
    }, 400);
  }

  /* ---- pothole thud ---- */
  function thud() {
    const buf = ctx.createBuffer(1, ctx.sampleRate * .25, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for(let i=0;i<d.length;i++){
      d[i] = (Math.random()*2-1) * Math.exp(-i/(ctx.sampleRate*.055));
    }
    const s = ctx.createBufferSource(); s.buffer = buf;
    const f = ctx.createBiquadFilter(); f.type='lowpass'; f.frequency.value=180;
    const g = ctx.createGain();
    g.gain.setValueAtTime(.55, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(.0001, ctx.currentTime+.22);
    s.connect(f); f.connect(g); g.connect(ctx.destination);
    s.start();

    /* suspension squeak */
    const o = ctx.createOscillator();
    const og = ctx.createGain();
    o.connect(og); og.connect(ctx.destination);
    o.type='sine'; o.frequency.setValueAtTime(480,ctx.currentTime);
    o.frequency.exponentialRampToValueAtTime(200, ctx.currentTime+.18);
    og.gain.setValueAtTime(.06, ctx.currentTime);
    og.gain.exponentialRampToValueAtTime(.0001, ctx.currentTime+.2);
    o.start(); o.stop(ctx.currentTime+.2);
  }

  /* thud timing matches CSS animation keyframes (8s cycle) */
  /* pothole 1 at ~32% → 2.56s, pothole 2 at ~61% → 4.88s */
  function scheduleThuds() {
    setTimeout(thud, 2560);
    setTimeout(thud, 4880);
    setTimeout(scheduleThuds, 8000);
  }

  function start(){
    if(ctx.state==='suspended') ctx.resume();
    startEngine();
    scheduleThuds();
    document.removeEventListener('click', start);
  }
  document.addEventListener('click', start, {once:true});
  setTimeout(()=>{ if(ctx.state!=='suspended'){ startEngine(); scheduleThuds(); } }, 500);
})();
</script>
""", unsafe_allow_html=True)

# ── Heading ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="roads-heading">
  <h1>🛣️ ROADS</h1>
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
        placeholder="Describe your road-related issue here…\n\nE.g. potholes, broken surface, waterlogging,\nno streetlights, dangerous turns, etc.\n\nThe system auto-detects severity from your tone.",
        height=190,
        key="complaint_input",
        label_visibility="collapsed",
    )

    submitted = st.button("🛣️ Submit Complaint", use_container_width=True)

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
    <div style="font-family:'Nunito',sans-serif;font-size:.78rem;color:rgba(245,200,66,.4);">
      <p style="margin-bottom:.5rem;letter-spacing:.12em;text-transform:uppercase;font-size:.66rem;">Priority Guide</p>
      <div style="display:flex;flex-direction:column;gap:.38rem;">
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#ef4444;box-shadow:0 0 7px #ef4444;flex-shrink:0;"></span>
          <span><b style="color:rgba(239,68,68,.9);">High</b> — Accident risk, injuries, dangerous road</span>
        </div>
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#f59e0b;box-shadow:0 0 7px #f59e0b;flex-shrink:0;"></span>
          <span><b style="color:rgba(245,158,11,.9);">Medium</b> — Potholes, flooding, broken surface</span>
        </div>
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#22c55e;box-shadow:0 0 7px #22c55e;flex-shrink:0;"></span>
          <span><b style="color:rgba(34,197,94,.9);">Low</b> — General feedback or suggestions</span>
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
    counts = {p: sum(1 for c in sorted_complaints if c["priority"]==p)
              for p in ["high","medium","low"]}

    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
                margin-bottom:1.2rem;flex-wrap:wrap;gap:.5rem;">
      <p class="section-title" style="margin-bottom:0;">📋 Complaints Log</p>
      <div style="display:flex;gap:.6rem;font-family:'Nunito',sans-serif;font-size:.72rem;">
        <span style="color:rgba(239,68,68,.85);">● {counts['high']} High</span>
        <span style="color:rgba(245,158,11,.85);">● {counts['medium']} Medium</span>
        <span style="color:rgba(34,197,94,.85);">● {counts['low']} Low</span>
        <span style="color:rgba(245,200,66,.3);">| {total} Total</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not sorted_complaints:
        st.markdown("""
        <div class="empty-state">
          <div style="font-size:2.5rem;margin-bottom:.8rem;">🛣️</div>
          <div>No complaints yet.<br>Report a road issue above.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for c in sorted_complaints:
            p     = c["priority"]
            color = PRIORITY_COLOR[p]
            label = PRIORITY_LABEL[p]
            date_str  = c["date"].strftime("%d %b %Y · %I:%M %p")
            safe_text = c["text"].replace("<","&lt;").replace(">","&gt;")
            bg = {"high":"rgba(239,68,68,.07)",
                  "medium":"rgba(245,158,11,.07)",
                  "low":"rgba(34,197,94,.07)"}[p]

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
<div style="text-align:center;margin-top:2rem;font-family:'Nunito',sans-serif;
            font-size:.72rem;color:rgba(245,200,66,.2);letter-spacing:.1em;">
  🛣️ Click anywhere to enable engine hum &amp; pothole thud sounds
</div>
""", unsafe_allow_html=True)
