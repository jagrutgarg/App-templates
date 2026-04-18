import streamlit as st
import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Health Complaints Portal",
    page_icon="🏥",
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
    "death", "died", "dying", "killed", "fatal", "critical", "serious",
    "negligence", "malpractice", "overdose", "wrong medicine", "misdiagnosis",
    "collapsed", "unconscious", "bleeding", "cancer", "heart attack", "stroke",
    "no doctor", "refused", "denied", "bribe", "corruption", "scam",
    "expired medicine", "dirty", "infection", "sepsis", "icu", "operation",
    "!!!","!!", "months", "years", "nobody", "nothing done", "helpless",
}
MEDIUM_WORDS = {
    "doctor", "nurse", "hospital", "clinic", "medicine", "treatment",
    "appointment", "waiting", "delay", "queue", "long wait", "rude",
    "unprofessional", "staff", "facility", "equipment", "broken", "missing",
    "unavailable", "shortage", "overcharging", "billing", "ambulance",
    "bed", "ward", "hygiene", "dirty", "unclean", "no water", "toilet",
    "complaint", "issue", "problem", "concern", "bad", "poor", "service",
    "slow", "not responding", "not available", "closed", "shut",
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
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&family=Inter:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0f0608 !important;
}
[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

/* ── deep crimson background ── */
body::before {
    content: "";
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 90% 55% at 15% 85%, rgba(180,0,30,.22) 0%, transparent 65%),
        radial-gradient(ellipse 70% 50% at 85% 15%, rgba(160,0,25,.18) 0%, transparent 65%),
        radial-gradient(ellipse 110% 80% at 50% 50%, rgba(100,0,18,.3)  0%, transparent 75%),
        linear-gradient(155deg, #0f0608 0%, #180508 35%, #1c060a 65%, #0f0608 100%);
    z-index: -3;
    animation: bg-breathe 10s ease-in-out infinite alternate;
}
@keyframes bg-breathe {
    from { filter: brightness(1); }
    to   { filter: brightness(1.08) hue-rotate(4deg); }
}

/* subtle scanline texture */
body::after {
    content: "";
    position: fixed; inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 3px,
        rgba(255,255,255,.008) 3px,
        rgba(255,255,255,.008) 4px
    );
    z-index: -1;
    pointer-events: none;
}

/* ── PLUS SIGNS LAYER ── */
.plus-layer {
    position: fixed; inset: 0;
    pointer-events: none; z-index: 0;
    overflow: hidden;
}

.plus {
    position: absolute;
    color: rgba(220,30,60,.13);
    font-size: 28px;
    font-weight: 900;
    font-family: 'Montserrat', sans-serif;
    line-height: 1;
    user-select: none;
    animation: plus-float ease-in-out infinite alternate;
    filter: blur(.3px);
    text-shadow: 0 0 12px rgba(220,30,60,.2);
}
@keyframes plus-float {
    0%   { transform: translateY(0px)   rotate(0deg)   scale(1);   opacity:.7; }
    100% { transform: translateY(-18px) rotate(12deg)  scale(1.08); opacity:1; }
}

/* EKG / heartbeat line */
.ekg-line {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    z-index: 1;
    pointer-events: none;
    background: linear-gradient(90deg,
        transparent 0%, rgba(220,30,60,.5) 40%,
        rgba(255,60,90,.9) 50%, rgba(220,30,60,.5) 60%,
        transparent 100%);
    animation: ekg-sweep 3s linear infinite;
    filter: blur(.5px);
}
@keyframes ekg-sweep {
    from { transform: translateX(-100%); }
    to   { transform: translateX(200%); }
}

/* pulse ring top-center */
.pulse-ring {
    position: fixed;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 200px;
    border-radius: 50%;
    border: 2px solid rgba(220,30,60,.25);
    animation: ring-expand 4s ease-out infinite;
    pointer-events: none; z-index: 0;
}
.pulse-ring:nth-child(2) { animation-delay: 1.3s; }
.pulse-ring:nth-child(3) { animation-delay: 2.6s; }
@keyframes ring-expand {
    0%   { transform: translateX(-50%) scale(.3); opacity:.7; }
    100% { transform: translateX(-50%) scale(3);  opacity:0; }
}

/* ── HEADING ── */
.health-heading {
    text-align: center;
    padding: 2rem 0 .4rem;
    position: relative; z-index: 3;
}
.health-heading h1 {
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: clamp(3.2rem, 8vw, 6.2rem);
    letter-spacing: .08em;
    color: #fff;
    text-shadow:
        0 0 12px rgba(220,30,60,.8),
        0 0 35px rgba(220,30,60,.5),
        0 0 80px rgba(180,0,30,.35),
        0 2px 0 rgba(0,0,0,.4);
    animation: heading-pulse 2.5s ease-in-out infinite alternate;
    display: inline-block;
}
@keyframes heading-pulse {
    from {
        text-shadow: 0 0 10px rgba(220,30,60,.7), 0 0 28px rgba(220,30,60,.4);
        letter-spacing: .08em;
    }
    to {
        text-shadow: 0 0 20px rgba(255,60,90,1), 0 0 55px rgba(220,30,60,.7), 0 0 100px rgba(180,0,30,.4);
        letter-spacing: .09em;
    }
}
.health-heading p {
    font-family: 'Inter', sans-serif;
    font-weight: 300; font-size: .88rem;
    letter-spacing: .3em; text-transform: uppercase;
    color: rgba(255,100,120,.38);
    margin-top: .35rem;
}

/* ── GLASS CARDS ── */
.glass-card {
    background: rgba(30,5,8,.45);
    border: 1px solid rgba(220,30,60,.14);
    border-radius: 16px;
    backdrop-filter: blur(14px);
    padding: 1.6rem;
    position: relative; z-index: 3;
    box-shadow:
        0 4px 40px rgba(0,0,0,.65),
        inset 0 1px 0 rgba(255,80,100,.07),
        inset 0 -1px 0 rgba(180,0,30,.08);
}
.section-title {
    font-family: 'Inter', sans-serif;
    font-weight: 500; font-size: .7rem;
    letter-spacing: .24em; text-transform: uppercase;
    color: rgba(255,100,120,.38);
    margin-bottom: 1rem;
}

/* ── COMPLAINT CARDS ── */
.complaint-card {
    background: rgba(30,4,8,.5);
    border: 1px solid rgba(255,255,255,.05);
    border-left: 3px solid;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: .85rem;
    transition: transform .2s, box-shadow .2s;
}
.complaint-card:hover {
    transform: translateX(3px);
    box-shadow: 0 4px 22px rgba(0,0,0,.5);
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
    0%,100% { transform:scale(1);    opacity:1; }
    50%      { transform:scale(1.45); opacity:.6; }
}
.priority-badge {
    font-family: 'Inter', sans-serif;
    font-size: .62rem; font-weight: 600;
    letter-spacing: .14em; text-transform: uppercase;
    padding: .16rem .52rem;
    border-radius: 99px; border: 1px solid;
}
.complaint-date {
    font-family: 'Inter', sans-serif;
    font-size: .7rem;
    color: rgba(255,100,120,.25);
    margin-left: auto;
}
.complaint-text {
    font-family: 'Inter', sans-serif;
    font-size: .92rem;
    color: rgba(240,220,222,.78);
    line-height: 1.56;
}
.empty-state {
    text-align: center; padding: 3rem 1rem;
    font-family: 'Inter', sans-serif;
    color: rgba(220,30,60,.2); font-size: .9rem;
}

/* ── STREAMLIT OVERRIDES ── */
[data-testid="stTextArea"] textarea {
    background: rgba(30,4,8,.5) !important;
    border: 1px solid rgba(220,30,60,.2) !important;
    border-radius: 10px !important;
    color: rgba(240,220,222,.9) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .95rem !important;
}
[data-testid="stTextArea"] textarea::placeholder {
    color: rgba(220,30,60,.3) !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(220,30,60,.5) !important;
    box-shadow: 0 0 0 2px rgba(220,30,60,.1) !important;
}
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #8b0000, #5c0011) !important;
    border: 1px solid rgba(220,30,60,.38) !important;
    color: #ffb3be !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: .88rem !important;
    letter-spacing: .14em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: .65rem !important;
    transition: all .25s !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #a00010, #7a0000) !important;
    box-shadow: 0 0 24px rgba(220,30,60,.3) !important;
    transform: translateY(-1px) !important;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Plus signs + pulse rings HTML ─────────────────────────────────────────────
plus_configs = [
    ( 4,  8, "22px", "5.5s", "0s",    ".10"),
    (12, 35, "36px", "7s",   "1.2s",  ".08"),
    (19, 62, "18px", "6s",   "0.5s",  ".12"),
    (27, 18, "42px", "8s",   "2.1s",  ".07"),
    (34, 78, "26px", "5s",   "3.3s",  ".11"),
    (41, 45, "14px", "9s",   "0.8s",  ".09"),
    (48, 12, "32px", "6.5s", "4s",    ".10"),
    (55, 68, "20px", "7.5s", "1.8s",  ".08"),
    (62, 30, "44px", "5.8s", "2.6s",  ".07"),
    (69, 85, "16px", "8.5s", "0.3s",  ".12"),
    (76, 52, "28px", "6.2s", "3.7s",  ".09"),
    (83, 22, "38px", "7.2s", "1.5s",  ".08"),
    (90, 70, "22px", "5.3s", "4.5s",  ".11"),
    (96, 40, "16px", "9s",   "2.9s",  ".09"),
    ( 8, 88, "30px", "6.8s", "1s",    ".10"),
    (22, 48, "40px", "7.8s", "3s",    ".07"),
    (50, 90, "24px", "5.6s", "0.6s",  ".11"),
    (72, 10, "34px", "8.2s", "2.3s",  ".08"),
    (38, 95, "18px", "6.4s", "4.8s",  ".12"),
    (88, 55, "28px", "7.4s", "1.1s",  ".09"),
]

plus_html = '<div class="plus-layer">'
plus_html += '<div class="pulse-ring"></div>'
plus_html += '<div class="pulse-ring"></div>'
plus_html += '<div class="pulse-ring"></div>'

for lft, top, size, dur, delay, opacity in plus_configs:
    plus_html += (
        f'<div class="plus" style="'
        f'left:{lft}%;top:{top}%;'
        f'font-size:{size};'
        f'animation-duration:{dur};'
        f'animation-delay:{delay};'
        f'color:rgba(220,30,60,{opacity});'
        f'">+</div>'
    )
plus_html += '</div>'
plus_html += '<div class="ekg-line"></div>'
st.markdown(plus_html, unsafe_allow_html=True)

# ── Ambulance siren (Web Audio API) ──────────────────────────────────────────
st.markdown("""
<script>
(function(){
  const ctx = new (window.AudioContext || window.webkitAudioContext)();

  /* ---- ambulance wail: two-tone European siren ---- */
  function siren(cycles) {
    const osc   = ctx.createOscillator();
    const osc2  = ctx.createOscillator();   /* harmony */
    const gain  = ctx.createGain();
    const dist  = ctx.createWaveShaper();

    /* gentle distortion for realism */
    const curve = new Float32Array(256);
    for(let i=0;i<256;i++){
      const x = (i*2/256)-1;
      curve[i] = (Math.PI+200)*x/(Math.PI+200*Math.abs(x));
    }
    dist.curve = curve;

    osc.type  = 'sawtooth';
    osc2.type = 'sawtooth';

    osc.connect(dist);
    osc2.connect(dist);
    dist.connect(gain);
    gain.connect(ctx.destination);

    /* fade in/out envelope */
    gain.gain.setValueAtTime(0.0001, ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.06, ctx.currentTime + 0.35);

    const cycleDur = 1.1;   /* one hi-lo cycle */
    const totalDur = cycles * cycleDur;

    for(let i = 0; i < cycles; i++){
      const t = ctx.currentTime + i * cycleDur;
      /* HIGH tone */
      osc.frequency.setValueAtTime(960, t);
      osc2.frequency.setValueAtTime(1200, t);
      /* LOW tone */
      osc.frequency.setValueAtTime(720, t + cycleDur * 0.5);
      osc2.frequency.setValueAtTime(900, t + cycleDur * 0.5);
    }

    /* fade out */
    gain.gain.setValueAtTime(0.06, ctx.currentTime + totalDur - 0.4);
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + totalDur);

    osc.start(ctx.currentTime);
    osc2.start(ctx.currentTime);
    osc.stop(ctx.currentTime + totalDur);
    osc2.stop(ctx.currentTime + totalDur);
  }

  /* ---- distant doppler pass: pitch rises then falls ---- */
  function doppler() {
    const osc  = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain); gain.connect(ctx.destination);
    osc.type = 'sawtooth';

    /* approaching */
    osc.frequency.setValueAtTime(600, ctx.currentTime);
    osc.frequency.linearRampToValueAtTime(850, ctx.currentTime + 1.2);
    /* passing */
    osc.frequency.linearRampToValueAtTime(500, ctx.currentTime + 2.0);
    osc.frequency.linearRampToValueAtTime(360, ctx.currentTime + 3.2);

    gain.gain.setValueAtTime(0.0001, ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.04, ctx.currentTime + 0.5);
    gain.gain.setValueAtTime(0.04, ctx.currentTime + 1.4);
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 3.5);

    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 3.6);
  }

  /* ---- heartbeat click ---- */
  function heartbeat() {
    function beat(t) {
      const b = ctx.createOscillator();
      const g = ctx.createGain();
      b.connect(g); g.connect(ctx.destination);
      b.type = 'sine';
      b.frequency.setValueAtTime(80, t);
      b.frequency.exponentialRampToValueAtTime(40, t + .08);
      g.gain.setValueAtTime(.12, t);
      g.gain.exponentialRampToValueAtTime(.0001, t + .09);
      b.start(t); b.stop(t + .1);
    }
    const now = ctx.currentTime;
    beat(now);
    beat(now + .18);   /* lub-DUB */
    setTimeout(heartbeat, 950 + Math.random()*200);
  }

  /* ---- scheduling ---- */
  function scheduleSiren() {
    siren(4);                                       /* 4 cycles ≈ 4.4s */
    setTimeout(() => {
      doppler();
      setTimeout(scheduleSiren, 9000 + Math.random() * 6000);
    }, 5500);
  }

  function start(){
    if(ctx.state==='suspended') ctx.resume();
    heartbeat();
    setTimeout(scheduleSiren, 800);
    document.removeEventListener('click', start);
  }
  document.addEventListener('click', start, {once:true});
  /* try auto */
  setTimeout(()=>{ if(ctx.state!=='suspended'){ heartbeat(); setTimeout(scheduleSiren,800); }}, 600);
})();
</script>
""", unsafe_allow_html=True)

# ── Heading ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="health-heading">
  <h1>🏥 HEALTH</h1>
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
        placeholder="Describe your health service issue here…\n\nE.g. no doctor available, wrong treatment,\nrude staff, medicine shortage, overcharging,\nhospital negligence, dirty facility, etc.\n\nSystem auto-detects severity from your tone.",
        height=195,
        key="complaint_input",
        label_visibility="collapsed",
    )

    submitted = st.button("🏥 Submit Complaint", use_container_width=True)

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
    <div style="font-family:'Inter',sans-serif;font-size:.78rem;color:rgba(255,100,120,.38);">
      <p style="margin-bottom:.5rem;letter-spacing:.12em;text-transform:uppercase;
                font-size:.66rem;color:rgba(255,100,120,.35);">Priority Guide</p>
      <div style="display:flex;flex-direction:column;gap:.42rem;">
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#ef4444;
                       box-shadow:0 0 7px #ef4444;flex-shrink:0;"></span>
          <span><b style="color:rgba(239,68,68,.9);">High</b> &mdash; Death risk, malpractice, critical</span>
        </div>
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#f59e0b;
                       box-shadow:0 0 7px #f59e0b;flex-shrink:0;"></span>
          <span><b style="color:rgba(245,158,11,.9);">Medium</b> &mdash; Staff issues, long wait, billing</span>
        </div>
        <div style="display:flex;align-items:center;gap:.55rem;">
          <span style="width:9px;height:9px;border-radius:50%;background:#22c55e;
                       box-shadow:0 0 7px #22c55e;flex-shrink:0;"></span>
          <span><b style="color:rgba(34,197,94,.9);">Low</b> &mdash; General feedback or suggestions</span>
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
    counts = {p: sum(1 for c in sorted_complaints if c["priority"] == p)
              for p in ["high","medium","low"]}

    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
                margin-bottom:1.2rem;flex-wrap:wrap;gap:.5rem;">
      <p class="section-title" style="margin-bottom:0;">📋 Complaints Log</p>
      <div style="display:flex;gap:.6rem;font-family:'Inter',sans-serif;font-size:.72rem;">
        <span style="color:rgba(239,68,68,.85);">● {counts['high']} High</span>
        <span style="color:rgba(245,158,11,.85);">● {counts['medium']} Medium</span>
        <span style="color:rgba(34,197,94,.85);">● {counts['low']} Low</span>
        <span style="color:rgba(255,100,120,.25);">| {total} Total</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not sorted_complaints:
        st.markdown("""
        <div class="empty-state">
          <div style="font-size:2.5rem;margin-bottom:.8rem;">🏥</div>
          <div>No complaints yet.<br>Report a health service issue above.</div>
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
<div style="text-align:center;margin-top:2rem;font-family:'Inter',sans-serif;
            font-size:.72rem;color:rgba(220,30,60,.16);letter-spacing:.1em;">
  🏥 Click anywhere to enable ambulance siren &amp; heartbeat sounds
</div>
""", unsafe_allow_html=True)
