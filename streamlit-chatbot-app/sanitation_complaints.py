import streamlit as st
import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sanitation Complaints Portal",
    page_icon="🚿",
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
    "disease", "epidemic", "infection", "contaminated", "toxic", "poisonous",
    "overflowing", "flooded", "stench", "unbearable", "filthy", "sewage",
    "rats", "insects", "maggots", "rotting", "death", "hospital", "vomiting",
    "diarrhea", "cholera", "typhoid", "malaria", "months", "years",
    "!!!", "!!", "nobody", "nothing done", "ignored", "helpless", "disaster",
}
MEDIUM_WORDS = {
    "dirty", "unclean", "garbage", "waste", "drain", "clog", "blocked",
    "overflow", "smell", "odor", "broken", "damaged", "leaking", "toilet",
    "bathroom", "latrine", "dustbin", "sweeper", "cleaning", "not clean",
    "irregular", "missed", "collection", "dustbin", "manhole", "open drain",
    "repair", "fix", "problem", "issue", "concern", "complaint", "bad", "poor",
    "delay", "water", "puddle", "stagnant", "mosquito", "fly", "pest",
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

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Righteous&family=DM+Sans:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #020d1a !important;
}
[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

/* ── deep water background ── */
body::before {
    content: "";
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 80%, rgba(0,80,160,.4) 0%, transparent 60%),
        radial-gradient(ellipse 70% 50% at 80% 20%, rgba(0,120,180,.3) 0%, transparent 60%),
        radial-gradient(ellipse 100% 100% at 50% 50%, rgba(0,40,90,.6) 0%, transparent 80%),
        linear-gradient(160deg, #020d1a 0%, #041828 40%, #061e32 70%, #020d1a 100%);
    z-index: -3;
    animation: bg-shift 12s ease-in-out infinite alternate;
}
@keyframes bg-shift {
    from { filter: hue-rotate(0deg) brightness(1); }
    to   { filter: hue-rotate(8deg) brightness(1.06); }
}

/* ── ripple overlay ── */
body::after {
    content: "";
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 200px 40px at 30% 70%, rgba(0,160,220,.08), transparent),
        radial-gradient(ellipse 160px 30px at 70% 40%, rgba(0,180,240,.06), transparent),
        radial-gradient(ellipse 120px 20px at 55% 85%, rgba(0,140,200,.07), transparent);
    z-index: -2;
    animation: ripple-drift 8s ease-in-out infinite alternate;
}
@keyframes ripple-drift {
    from { transform: translateY(0) scaleX(1); opacity:.7; }
    to   { transform: translateY(-6px) scaleX(1.02); opacity:1; }
}

/* ── SPLASH SHAPES CONTAINER ── */
.splashes {
    position: fixed; inset: 0;
    pointer-events: none; z-index: 0;
    overflow: hidden;
}

/* base splash element */
.splash {
    position: absolute;
    border-radius: 50%;
    border: 2px solid;
    opacity: 0;
    animation: splash-expand ease-out infinite;
}
@keyframes splash-expand {
    0%   { transform: scale(.05); opacity:.85; }
    60%  { opacity:.3; }
    100% { transform: scale(1);   opacity:0;  }
}

/* droplet teardrop shapes */
.drop {
    position: absolute;
    opacity: 0;
    animation: drop-fall linear infinite;
}
.drop::before {
    content: "";
    display: block;
    width: 8px; height: 12px;
    background: radial-gradient(ellipse at 40% 30%, rgba(120,210,255,.8), rgba(0,140,220,.4));
    border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
    filter: blur(.4px);
}
@keyframes drop-fall {
    0%   { transform: translateY(-30px); opacity:0; }
    15%  { opacity:.9; }
    85%  { opacity:.6; }
    100% { transform: translateY(110vh);  opacity:0; }
}

/* curved water arc splashes */
.arc {
    position: absolute;
    border: 0 solid transparent;
    border-top: 3px solid rgba(80,190,255,.5);
    border-radius: 50%;
    opacity: 0;
    animation: arc-pop ease-out infinite;
}
@keyframes arc-pop {
    0%   { transform: scale(.1) rotate(0deg);  opacity:.9; }
    40%  { opacity:.5; }
    100% { transform: scale(1.4) rotate(15deg); opacity:0; }
}

/* water blob splatter */
.blob {
    position: absolute;
    border-radius: 60% 40% 55% 45% / 50% 60% 40% 50%;
    background: radial-gradient(ellipse, rgba(60,180,255,.3), rgba(0,120,200,.12));
    opacity: 0;
    animation: blob-burst ease-out infinite;
}
@keyframes blob-burst {
    0%   { transform: scale(.2); opacity:.8; }
    50%  { opacity:.4; }
    100% { transform: scale(2.5); opacity:0; }
}

/* ── HEADING ── */
.san-heading {
    text-align: center;
    padding: 2rem 0 .4rem;
    position: relative; z-index: 3;
}
.san-heading h1 {
    font-family: 'Righteous', sans-serif;
    font-size: clamp(3rem, 7.5vw, 6rem);
    letter-spacing: .1em;
    background: linear-gradient(135deg,
        #ffffff 0%, #a8e6ff 25%, #5bc8ff 50%, #00aaff 75%, #0080ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 22px rgba(0,170,255,.7));
    animation: heading-flow 4s ease-in-out infinite alternate;
    display: inline-block;
}
@keyframes heading-flow {
    from {
        filter: drop-shadow(0 0 16px rgba(0,170,255,.6));
        transform: translateY(0);
    }
    to {
        filter: drop-shadow(0 0 38px rgba(91,200,255,.95));
        transform: translateY(-3px);
    }
}
.san-heading p {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300; font-size: .88rem;
    letter-spacing: .3em; text-transform: uppercase;
    color: rgba(91,200,255,.45);
    margin-top: .3rem;
}

/* ── GLASS CARDS ── */
.glass-card {
    background: rgba(0,60,120,.12);
    border: 1px solid rgba(91,200,255,.14);
    border-radius: 16px;
    backdrop-filter: blur(14px);
    padding: 1.6rem;
    position: relative; z-index: 3;
    box-shadow:
        0 4px 40px rgba(0,0,0,.55),
        inset 0 1px 0 rgba(255,255,255,.05),
        inset 0 -1px 0 rgba(0,100,200,.1);
}
.section-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600; font-size: .7rem;
    letter-spacing: .24em; text-transform: uppercase;
    color: rgba(91,200,255,.42);
    margin-bottom: 1rem;
}

/* ── COMPLAINT CARDS ── */
.complaint-card {
    background: rgba(0,60,100,.15);
    border: 1px solid rgba(255,255,255,.06);
    border-left: 3px solid;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: .85rem;
    transition: transform .2s, box-shadow .2s;
}
.complaint-card:hover {
    transform: translateX(3px);
    box-shadow: 0 4px 22px rgba(0,0,0,.4);
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
    50%      { transform:scale(1.45);opacity:.6; }
}
.priority-badge {
    font-family: 'DM Sans', sans-serif;
    font-size: .62rem; font-weight: 600;
    letter-spacing: .14em; text-transform: uppercase;
    padding: .16rem .52rem;
    border-radius: 99px; border: 1px solid;
}
.complaint-date {
    font-family: 'DM Sans', sans-serif;
    font-size: .7rem;
    color: rgba(91,200,255,.28);
    margin-left: auto;
}
.complaint-text {
    font-family: 'DM Sans', sans-serif;
    font-size: .92rem;
    color: rgba(210,235,255,.78);
    line-height: 1.56;
}
.empty-state {
    text-align: center; padding: 3rem 1rem;
    font-family: 'DM Sans', sans-serif;
    color: rgba(91,200,255,.22); font-size: .9rem;
}

/* ── STREAMLIT OVERRIDES ── */
[data-testid="stTextArea"] textarea {
    background: rgba(0,60,120,.18) !important;
    border: 1px solid rgba(91,200,255,.22) !important;
    border-radius: 10px !important;
    color: rgba(210,235,255,.9) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .95rem !important;
}
[data-testid="stTextArea"] textarea::placeholder {
    color: rgba(91,200,255,.32) !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(91,200,255,.55) !important;
    box-shadow: 0 0 0 2px rgba(91,200,255,.1) !important;
}
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #005a8e, #003d66) !important;
    border: 1px solid rgba(91,200,255,.35) !important;
    color: #a8e6ff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: .88rem !important;
    letter-spacing: .14em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: .65rem !important;
    transition: all .25s !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #0077bb, #005a8e) !important;
    box-shadow: 0 0 24px rgba(91,200,255,.28) !important;
    transform: translateY(-1px) !important;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Splash shapes HTML ────────────────────────────────────────────────────────
splashes_html = '<div class="splashes">'

# Large concentric ring splashes
ring_configs = [
    (15, 30, 90,  90,  "rgba(0,160,220,.35)", "6s",  "0s"),
    (15, 30, 60,  60,  "rgba(0,180,240,.3)",  "6s",  ".5s"),
    (15, 30, 30,  30,  "rgba(0,200,255,.4)",  "6s",  "1s"),
    (70, 20, 110, 110, "rgba(0,140,200,.3)",  "8s",  "2s"),
    (70, 20, 70,  70,  "rgba(0,160,220,.35)", "8s",  "2.6s"),
    (70, 20, 35,  35,  "rgba(0,180,240,.4)",  "8s",  "3.2s"),
    (45, 65, 80,  80,  "rgba(0,170,230,.32)", "7s",  "1s"),
    (45, 65, 45,  45,  "rgba(0,190,250,.38)", "7s",  "1.5s"),
    (45, 65, 20,  20,  "rgba(0,210,255,.44)", "7s",  "2s"),
    (85, 55, 70,  70,  "rgba(0,150,210,.3)",  "9s",  "4s"),
    (85, 55, 40,  40,  "rgba(0,170,230,.35)", "9s",  "4.7s"),
    (25, 75, 60,  60,  "rgba(0,160,225,.3)",  "7.5s","3s"),
    (25, 75, 32,  32,  "rgba(0,180,245,.38)", "7.5s","3.6s"),
    (60, 10, 55,  55,  "rgba(0,155,215,.32)", "10s", "5s"),
    (60, 10, 28,  28,  "rgba(0,175,235,.4)",  "10s", "5.8s"),
]
for lft, top, w, h, color, dur, delay in ring_configs:
    splashes_html += (
        f'<div class="splash" style="'
        f'left:{lft}%;top:{top}%;'
        f'width:{w}px;height:{h}px;'
        f'border-color:{color};'
        f'margin-left:-{w//2}px;margin-top:-{h//2}px;'
        f'animation-duration:{dur};animation-delay:{delay};"></div>'
    )

# Water arc splashes
arc_configs = [
    (20, 28, 80,  40,  "6.5s", "1.2s"),
    (65, 18, 100, 50,  "8.5s", "3.5s"),
    (40, 60, 70,  35,  "7s",   "2s"),
    (80, 50, 90,  45,  "9s",   "0.5s"),
    (10, 70, 60,  30,  "7.5s", "4.5s"),
]
for lft, top, w, h, dur, delay in arc_configs:
    splashes_html += (
        f'<div class="arc" style="'
        f'left:{lft}%;top:{top}%;'
        f'width:{w}px;height:{h}px;'
        f'animation-duration:{dur};animation-delay:{delay};"></div>'
    )

# Blob splatter shapes
blob_configs = [
    (30, 40, 50, 50,  "7s",  "0.8s"),
    (72, 30, 40, 40,  "9s",  "2.2s"),
    (50, 70, 60, 60,  "8s",  "4s"),
    (12, 50, 35, 35,  "6.5s","1.5s"),
    (88, 65, 45, 45,  "10s", "6s"),
]
for lft, top, w, h, dur, delay in blob_configs:
    splashes_html += (
        f'<div class="blob" style="'
        f'left:{lft}%;top:{top}%;'
        f'width:{w}px;height:{h}px;'
        f'animation-duration:{dur};animation-delay:{delay};"></div>'
    )

# Falling droplets
drop_configs = [
    (5,  "9s",  "0s"),  (12, "12s", "3s"),  (22, "11s", "1.5s"),
    (33, "14s", "5s"),  (44, "10s", "2.5s"), (55, "13s", "0.5s"),
    (63, "11s", "4s"),  (74, "15s", "7s"),   (82, "10s", "1s"),
    (91, "12s", "6s"),  (8,  "16s", "8s"),   (48, "11s", "3.5s"),
    (68, "13s", "9s"),  (38, "10s", "2s"),   (78, "14s", "4.5s"),
]
for lft, dur, delay in drop_configs:
    splashes_html += (
        f'<div class="drop" style="'
        f'left:{lft}%;'
        f'animation-duration:{dur};animation-delay:{delay};"></div>'
    )

splashes_html += "</div>"
st.markdown(splashes_html, unsafe_allow_html=True)

# ── Flush sound (Web Audio API) ───────────────────────────────────────────────
st.markdown("""
<script>
(function(){
  const ctx = new (window.AudioContext || window.webkitAudioContext)();

  function flush() {
    const dur = 2.8;

    /* --- rushing water noise --- */
    const bufLen = ctx.sampleRate * dur;
    const buf = ctx.createBuffer(2, bufLen, ctx.sampleRate);
    for(let ch=0;ch<2;ch++){
      const d = buf.getChannelData(ch);
      for(let i=0;i<bufLen;i++){
        d[i] = (Math.random()*2-1);
      }
    }
    const noise = ctx.createBufferSource();
    noise.buffer = buf;

    /* bandpass → sounds like rushing water, not static */
    const bp1 = ctx.createBiquadFilter();
    bp1.type = 'bandpass'; bp1.frequency.value = 800; bp1.Q.value = 0.6;

    const bp2 = ctx.createBiquadFilter();
    bp2.type = 'bandpass'; bp2.frequency.value = 400; bp2.Q.value = 0.4;

    const lp = ctx.createBiquadFilter();
    lp.type = 'lowpass'; lp.frequency.value = 1800;

    /* gain envelope: rush up → sustain → fade */
    const gain = ctx.createGain();
    gain.gain.setValueAtTime(0.0001, ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.28, ctx.currentTime + 0.18);
    gain.gain.setValueAtTime(0.28, ctx.currentTime + 0.5);
    gain.gain.linearRampToValueAtTime(0.20, ctx.currentTime + 1.6);
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + dur);

    noise.connect(bp1); noise.connect(bp2);
    bp1.connect(lp); bp2.connect(lp);
    lp.connect(gain); gain.connect(ctx.destination);
    noise.start(ctx.currentTime);
    noise.stop(ctx.currentTime + dur);

    /* --- swirl tone: descending spiral --- */
    const swirl = ctx.createOscillator();
    const sg = ctx.createGain();
    swirl.connect(sg); sg.connect(ctx.destination);
    swirl.type = 'sine';
    swirl.frequency.setValueAtTime(380, ctx.currentTime);
    swirl.frequency.exponentialRampToValueAtTime(90, ctx.currentTime + 2.2);
    sg.gain.setValueAtTime(0.0001, ctx.currentTime);
    sg.gain.linearRampToValueAtTime(0.07, ctx.currentTime + 0.2);
    sg.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 2.4);
    swirl.start(ctx.currentTime);
    swirl.stop(ctx.currentTime + 2.4);

    /* --- initial plop impact --- */
    const plop = ctx.createOscillator();
    const pg = ctx.createGain();
    plop.connect(pg); pg.connect(ctx.destination);
    plop.type = 'sine';
    plop.frequency.setValueAtTime(600, ctx.currentTime);
    plop.frequency.exponentialRampToValueAtTime(120, ctx.currentTime + .25);
    pg.gain.setValueAtTime(0.18, ctx.currentTime);
    pg.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + .3);
    plop.start(ctx.currentTime);
    plop.stop(ctx.currentTime + .3);

    /* schedule next flush */
    const nextIn = 8000 + Math.random() * 7000;
    setTimeout(flush, nextIn);
  }

  function start(){
    if(ctx.state==='suspended') ctx.resume();
    setTimeout(flush, 600);
    document.removeEventListener('click', start);
  }
  document.addEventListener('click', start, {once:true});
  setTimeout(()=>{ if(ctx.state!=='suspended') flush(); }, 800);
})();
</script>
""", unsafe_allow_html=True)

# ── Heading ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="san-heading">
  <h1>🚿 SANITATION</h1>
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
        placeholder="Describe your sanitation issue here…\n\nE.g. garbage not collected, open drain, clogged\nmanhole, filthy public toilet, sewage overflow,\nmosquitoes, stench in area, etc.\n\nThe system auto-detects severity from your tone.",
        height=195,
        key="complaint_input",
        label_visibility="collapsed",
    )

    submitted = st.button("🚿 Submit Complaint", use_container_width=True)

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
    <div style="font-family:'DM Sans',sans-serif;font-size:.78rem;color:rgba(91,200,255,.4);">
      <p style="margin-bottom:.5rem;letter-spacing:.12em;text-transform:uppercase;font-size:.66rem;">Priority Guide</p>
      <div style="display:flex;flex-direction:column;gap:.4rem;">
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#ef4444;
                       box-shadow:0 0 7px #ef4444;flex-shrink:0;"></span>
          <span><b style="color:rgba(239,68,68,.9);">High</b> — Disease risk, epidemic, toxic overflow</span>
        </div>
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#f59e0b;
                       box-shadow:0 0 7px #f59e0b;flex-shrink:0;"></span>
          <span><b style="color:rgba(245,158,11,.9);">Medium</b> — Garbage, drains, blocked manholes</span>
        </div>
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#22c55e;
                       box-shadow:0 0 7px #22c55e;flex-shrink:0;"></span>
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
      <div style="display:flex;gap:.6rem;font-family:'DM Sans',sans-serif;font-size:.72rem;">
        <span style="color:rgba(239,68,68,.85);">● {counts['high']} High</span>
        <span style="color:rgba(245,158,11,.85);">● {counts['medium']} Medium</span>
        <span style="color:rgba(34,197,94,.85);">● {counts['low']} Low</span>
        <span style="color:rgba(91,200,255,.3);">| {total} Total</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not sorted_complaints:
        st.markdown("""
        <div class="empty-state">
          <div style="font-size:2.5rem;margin-bottom:.8rem;">🚿</div>
          <div>No complaints yet.<br>Report a sanitation issue above.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for c in sorted_complaints:
            p         = c["priority"]
            color     = PRIORITY_COLOR[p]
            label     = PRIORITY_LABEL[p]
            date_str  = c["date"].strftime("%d %b %Y · %I:%M %p")
            safe_text = c["text"].replace("<","&lt;").replace(">","&gt;")
            bg = {"high":  "rgba(239,68,68,.07)",
                  "medium":"rgba(245,158,11,.07)",
                  "low":   "rgba(34,197,94,.07)"}[p]

            st.markdown(f"""
            <div class="complaint-card" style="border-left-color:{color};">
              <div class="complaint-header">
                <span class="priority-dot"
                      style="background:{color};box-shadow:0 0 9px {color};"></span>
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
<div style="text-align:center;margin-top:2rem;font-family:'DM Sans',sans-serif;
            font-size:.72rem;color:rgba(91,200,255,.18);letter-spacing:.1em;">
  🚿 Click anywhere to enable ambient flush &amp; water sounds
</div>
""", unsafe_allow_html=True)
