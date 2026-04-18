import streamlit as st
import anthropic
import datetime
import time

st.set_page_config(
    page_title="Public Safety Portal",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg:        #0a0e1a;
    --surface:   #111827;
    --surface2:  #1a2235;
    --red:       #ef4444;
    --red-glow:  rgba(239,68,68,0.25);
    --blue:      #3b82f6;
    --blue-glow: rgba(59,130,246,0.2);
    --amber:     #f59e0b;
    --green:     #22c55e;
    --yellow:    #eab308;
    --text:      #f1f5f9;
    --muted:     #94a3b8;
    --border:    rgba(255,255,255,0.08);
    --stripe:    rgba(239,68,68,0.06);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.8rem !important; max-width: 1280px; }

/* ══ HERO ══ */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #0a0e1a 0%, #0f1729 50%, #0a0e1a 100%);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 20px;
    padding: 0;
    margin-bottom: 1.4rem;
    box-shadow: 0 0 60px rgba(239,68,68,0.1), 0 0 120px rgba(59,130,246,0.06);
}
/* animated alert stripe */
.hero::before {
    content:'';
    position:absolute; top:0; left:0; right:0; height:4px;
    background: repeating-linear-gradient(90deg, var(--red) 0px, var(--red) 30px, var(--blue) 30px, var(--blue) 60px);
    animation: stripeScroll 1.2s linear infinite;
}
@keyframes stripeScroll {
    from { background-position: 0 0; }
    to   { background-position: 60px 0; }
}
.hero-inner {
    display: flex;
    align-items: center;
    gap: 2rem;
    padding: 2rem 2.5rem 1.8rem;
}
.hero-text h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.6rem;
    letter-spacing: 3px;
    margin: 0 0 .3rem;
    background: linear-gradient(90deg, var(--red) 0%, #fff 55%, var(--blue) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
    0%,100% { filter: brightness(1); }
    50%      { filter: brightness(1.15); }
}
.hero-text p { color: var(--muted); font-size:.95rem; margin:0; letter-spacing:.3px; }

/* ══ CITY SCENE (SVG) ══ */
.city-wrap svg .ambulance-body { animation: driveAmb 14s linear infinite; }
.siren-left  { animation: sirenFlash 0.5s ease-in-out infinite alternate; }
.siren-right { animation: sirenFlash 0.5s ease-in-out 0.25s infinite alternate; }
@keyframes sirenFlash {
    from { fill: var(--red);  opacity:1; }
    to   { fill: var(--blue); opacity:0.7; }
}
@keyframes driveAmb {
    0%   { transform: translateX(0); }
    100% { transform: translateX(620px); }
}
/* crowd sway */
.person { animation: sway 2.5s ease-in-out infinite alternate; transform-origin: bottom center; }
.person:nth-child(even) { animation-duration:3.2s; animation-direction:alternate-reverse; }
@keyframes sway {
    from { transform: rotate(-2deg); }
    to   { transform: rotate(2deg); }
}

/* ══ TICKER ══ */
.ticker-wrap {
    background: var(--red);
    padding: .35rem 0;
    overflow: hidden;
    margin-bottom: 1.4rem;
    border-radius: 8px;
}
.ticker-track {
    display: flex;
    white-space: nowrap;
    animation: tickerScroll 22s linear infinite;
    width: max-content;
}
@keyframes tickerScroll {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
}
.ticker-item {
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #fff;
    padding: 0 2.5rem;
}
.ticker-item::before { content:'⚠ '; }

/* ══ CARDS ══ */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
.card h3 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: 1.5px;
    color: var(--red);
    margin: 0 0 1rem;
}

/* ══ COMPLAINTS ══ */
.complaint-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 3px solid transparent;
    border-radius: 10px;
    padding: .85rem 1rem;
    margin-bottom: .6rem;
    animation: slideIn .35s ease both;
    transition: border-color .2s;
}
.complaint-item.high-item   { border-left-color: var(--red); }
.complaint-item.medium-item { border-left-color: var(--yellow); }
.complaint-item.low-item    { border-left-color: var(--green); }
.complaint-item:hover { border-color: rgba(255,255,255,0.18); }
@keyframes slideIn {
    from { opacity:0; transform:translateX(-14px); }
    to   { opacity:1; transform:translateX(0); }
}
.priority-dot {
    width:13px; height:13px; border-radius:50%; flex-shrink:0; margin-top:4px;
    animation: dotPulse 2s ease-in-out infinite;
}
.dot-high   { background:var(--red);    box-shadow:0 0 10px var(--red); }
.dot-medium { background:var(--yellow); box-shadow:0 0 8px var(--yellow); }
.dot-low    { background:var(--green);  box-shadow:0 0 6px var(--green); }
@keyframes dotPulse {
    0%,100% { transform:scale(1); }
    50%     { transform:scale(1.25); }
}
.complaint-text { font-size:.9rem; line-height:1.5; margin:0 0 .3rem; color:var(--text); }
.complaint-meta { font-size:.72rem; color:var(--muted); display:flex; gap:10px; align-items:center; }
.badge {
    font-size:.65rem; font-weight:700; padding:2px 8px;
    border-radius:20px; text-transform:uppercase; letter-spacing:.6px;
}
.badge-high   { background:rgba(239,68,68,.18);  color:var(--red); }
.badge-medium { background:rgba(234,179,8,.18);  color:var(--yellow); }
.badge-low    { background:rgba(34,197,94,.18);  color:var(--green); }

/* ══ INPUTS ══ */
.stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .9rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 3px rgba(239,68,68,0.15) !important;
}
div.stButton > button {
    background: linear-gradient(135deg, var(--red), #b91c1c) !important;
    color: #fff !important; border:none !important;
    border-radius:10px !important; font-weight:700 !important;
    padding:.55rem 1.8rem !important; font-size:.9rem !important;
    font-family:'Inter',sans-serif !important; letter-spacing:.4px !important;
    box-shadow: 0 4px 14px rgba(239,68,68,0.35) !important;
}
div.stButton > button:hover { opacity:.85 !important; }

/* ══ CHAT ══ */
.chat-bubble {
    padding:.75rem 1rem; border-radius:12px;
    margin-bottom:.55rem; max-width:80%;
    font-size:.9rem; line-height:1.55;
    animation: slideIn .3s ease both;
}
.bubble-user {
    background:rgba(239,68,68,.12);
    border:1px solid rgba(239,68,68,.3);
    margin-left:auto; text-align:right;
}
.bubble-ai {
    background:var(--surface2);
    border:1px solid var(--border);
}
.bubble-role {
    font-size:.68rem; font-weight:700;
    text-transform:uppercase; letter-spacing:.6px;
    color:var(--muted); margin-bottom:4px;
}
</style>

<!-- Ambulance siren via Web Audio API -->
<script>
(function(){
    var ctx, sirenLoop;
    function buildSiren(){
        var osc  = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'sawtooth';
        gain.gain.value = 0.08;
        // oscillate frequency up/down like a real siren
        var now = ctx.currentTime;
        function sweep(t){
            osc.frequency.setValueAtTime(650, t);
            osc.frequency.linearRampToValueAtTime(1050, t + 0.9);
            osc.frequency.linearRampToValueAtTime(650,  t + 1.8);
        }
        sweep(now);
        // schedule repeating sweeps
        sirenLoop = setInterval(function(){
            sweep(ctx.currentTime);
        }, 1800);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start();
        // store ref for cleanup
        ctx._osc  = osc;
        ctx._gain = gain;
    }
    function startSiren(){
        if(ctx) return;
        try {
            ctx = new (window.AudioContext||window.webkitAudioContext)();
            buildSiren();
            // fade siren out after 4 seconds (just a brief alert on load)
            setTimeout(function(){
                if(ctx && ctx._gain){
                    ctx._gain.gain.linearRampToValueAtTime(0, ctx.currentTime+1.2);
                    setTimeout(function(){
                        try{ ctx._osc.stop(); clearInterval(sirenLoop); }catch(e){}
                    }, 1300);
                }
            }, 4000);
        } catch(e){}
    }
    // Try on load, fallback to first click
    window.addEventListener('load', function(){ setTimeout(startSiren, 800); });
    document.addEventListener('click', function once(){ startSiren(); document.removeEventListener('click',once); });
})();
</script>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "complaints" not in st.session_state:
    st.session_state.complaints = [
        {"text": "Sewage water OVERFLOWING into streets! People slipping and getting injured! This is a PUBLIC HEALTH EMERGENCY!!!",
         "priority": "high",   "date": (datetime.date.today()-datetime.timedelta(days=1)).strftime("%d %b %Y")},
        {"text": "Contaminated water supply causing illness in multiple households in Ward 5. Urgent testing required.",
         "priority": "medium", "date": (datetime.date.today()-datetime.timedelta(days=3)).strftime("%d %b %Y")},
        {"text": "Water pressure is very low in our building since last week. Please look into this.",
         "priority": "low",    "date": (datetime.date.today()-datetime.timedelta(days=7)).strftime("%d %b %Y")},
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Priority classifier ───────────────────────────────────────────────────────
ANGER = {"unacceptable","outrageous","disgusting","terrible","horrible","furious","angry",
         "emergency","dangerous","deadly","critical","urgent","pathetic","useless","worst",
         "appalling","sick","enough","ridiculous","shameful","immediately","criminal",
         "life-threatening","hazardous","injur","death","die","!!","!!!","fed up"}

def classify(text):
    lo = text.lower()
    score  = sum(2 for w in ANGER if w in lo)
    score += text.count("!")
    score += (sum(1 for c in text if c.isupper()) / max(len(text), 1)) * 14
    if score >= 5:   return "high"
    if score >= 1.5: return "medium"
    return "low"

def sorted_complaints():
    order = {"high":0, "medium":1, "low":2}
    return sorted(st.session_state.complaints, key=lambda x: order[x["priority"]])

# ══════════════════════════════════════════════════════════════════════════════
#  HERO — city scene with crowd + ambulance
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-inner">
    <div class="hero-text">
      <h1>PUBLIC SAFETY</h1>
      <p>🚨 Citizen Emergency Portal · Water Safety · Incident Reporting</p>
    </div>

    <!-- City scene SVG -->
    <div class="city-wrap" style="flex:1; min-width:0; overflow:hidden; border-radius:10px;">
    <svg viewBox="0 0 620 170" width="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="night" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#060c1a"/>
          <stop offset="100%" stop-color="#0f1729"/>
        </linearGradient>
        <linearGradient id="road" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#1e293b"/>
          <stop offset="100%" stop-color="#0f172a"/>
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2.5" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>

      <!-- Sky -->
      <rect width="620" height="170" fill="url(#night)"/>

      <!-- Moon -->
      <circle cx="560" cy="22" r="14" fill="#fef3c7" opacity=".9" filter="url(#glow)"/>
      <circle cx="566" cy="18" r="11" fill="#0f172a"/>

      <!-- Stars -->
      <circle cx="30"  cy="12" r="1.2" fill="#fff" opacity=".8"/>
      <circle cx="80"  cy="8"  r="1"   fill="#fff" opacity=".6"/>
      <circle cx="150" cy="15" r="1.3" fill="#fff" opacity=".9"/>
      <circle cx="240" cy="6"  r="1"   fill="#fff" opacity=".7"/>
      <circle cx="330" cy="18" r="1.2" fill="#fff" opacity=".5"/>
      <circle cx="420" cy="9"  r="1"   fill="#fff" opacity=".8"/>
      <circle cx="490" cy="20" r="1.1" fill="#fff" opacity=".6"/>

      <!-- Buildings -->
      <!-- B1 -->
      <rect x="0"   y="40" width="55" height="100" fill="#1e293b" stroke="#334155" stroke-width=".5"/>
      <rect x="5"   y="48" width="12" height="10"  fill="#fbbf24" opacity=".7"/>
      <rect x="22"  y="48" width="12" height="10"  fill="#60a5fa" opacity=".5"/>
      <rect x="39"  y="48" width="12" height="10"  fill="#fbbf24" opacity=".3"/>
      <rect x="5"   y="65" width="12" height="10"  fill="#60a5fa" opacity=".6"/>
      <rect x="22"  y="65" width="12" height="10"  fill="#fbbf24" opacity=".4"/>
      <rect x="39"  y="65" width="12" height="10"  fill="#60a5fa" opacity=".7"/>
      <rect x="5"   y="82" width="12" height="10"  fill="#fbbf24" opacity=".5"/>
      <rect x="39"  y="82" width="12" height="10"  fill="#60a5fa" opacity=".4"/>
      <!-- antenna -->
      <rect x="26"  y="33" width="3"  height="10"  fill="#475569"/>
      <circle cx="27" cy="31" r="2" fill="#ef4444" opacity=".9" filter="url(#glow)"/>

      <!-- B2 tall -->
      <rect x="60"  y="15" width="70" height="125" fill="#162032" stroke="#334155" stroke-width=".5"/>
      <rect x="88"  y="6"  width="14" height="12"  fill="#475569"/>
      <circle cx="95" cy="5" r="3" fill="#ef4444" filter="url(#glow)"/>
      <rect x="66"  y="22" width="15" height="12"  fill="#fbbf24" opacity=".6"/>
      <rect x="87"  y="22" width="15" height="12"  fill="#60a5fa" opacity=".5"/>
      <rect x="108" y="22" width="15" height="12"  fill="#fbbf24" opacity=".4"/>
      <rect x="66"  y="40" width="15" height="12"  fill="#60a5fa" opacity=".7"/>
      <rect x="87"  y="40" width="15" height="12"  fill="#fbbf24" opacity=".5"/>
      <rect x="108" y="40" width="15" height="12"  fill="#60a5fa" opacity=".3"/>
      <rect x="66"  y="58" width="15" height="12"  fill="#fbbf24" opacity=".4"/>
      <rect x="108" y="58" width="15" height="12"  fill="#fbbf24" opacity=".6"/>
      <rect x="66"  y="76" width="15" height="12"  fill="#60a5fa" opacity=".5"/>
      <rect x="87"  y="76" width="15" height="12"  fill="#fbbf24" opacity=".3"/>
      <rect x="108" y="76" width="15" height="12"  fill="#60a5fa" opacity=".6"/>

      <!-- B3 -->
      <rect x="135" y="50" width="50" height="90"  fill="#1e293b" stroke="#334155" stroke-width=".5"/>
      <rect x="141" y="57" width="12" height="10"  fill="#fbbf24" opacity=".5"/>
      <rect x="158" y="57" width="12" height="10"  fill="#60a5fa" opacity=".4"/>
      <rect x="141" y="73" width="12" height="10"  fill="#60a5fa" opacity=".6"/>
      <rect x="158" y="73" width="12" height="10"  fill="#fbbf24" opacity=".3"/>
      <rect x="141" y="89" width="12" height="10"  fill="#fbbf24" opacity=".7"/>

      <!-- B4 short wide -->
      <rect x="190" y="65" width="80" height="75"  fill="#162032" stroke="#334155" stroke-width=".5"/>
      <rect x="197" y="72" width="14" height="11"  fill="#fbbf24" opacity=".6"/>
      <rect x="217" y="72" width="14" height="11"  fill="#60a5fa" opacity=".4"/>
      <rect x="237" y="72" width="14" height="11"  fill="#fbbf24" opacity=".5"/>
      <rect x="197" y="89" width="14" height="11"  fill="#60a5fa" opacity=".5"/>
      <rect x="237" y="89" width="14" height="11"  fill="#60a5fa" opacity=".3"/>
      <!-- hospital cross -->
      <rect x="220" y="42" width="20" height="6"   fill="#ef4444" rx="2"/>
      <rect x="226" y="36" width="6"  height="18"  fill="#ef4444" rx="2"/>

      <!-- B5 -->
      <rect x="275" y="30" width="60" height="110" fill="#1e293b" stroke="#334155" stroke-width=".5"/>
      <rect x="303" y="20" width="4"  height="13"  fill="#475569"/>
      <circle cx="305" cy="19" r="2.5" fill="#3b82f6" filter="url(#glow)"/>
      <rect x="281" y="38" width="13" height="11"  fill="#fbbf24" opacity=".6"/>
      <rect x="300" y="38" width="13" height="11"  fill="#60a5fa" opacity=".4"/>
      <rect x="319" y="38" width="13" height="11"  fill="#fbbf24" opacity=".5"/>
      <rect x="281" y="55" width="13" height="11"  fill="#60a5fa" opacity=".5"/>
      <rect x="300" y="55" width="13" height="11"  fill="#fbbf24" opacity=".3"/>
      <rect x="319" y="55" width="13" height="11"  fill="#60a5fa" opacity=".7"/>
      <rect x="281" y="72" width="13" height="11"  fill="#fbbf24" opacity=".4"/>
      <rect x="319" y="72" width="13" height="11"  fill="#fbbf24" opacity=".6"/>
      <rect x="281" y="89" width="13" height="11"  fill="#60a5fa" opacity=".6"/>
      <rect x="300" y="89" width="13" height="11"  fill="#fbbf24" opacity=".5"/>

      <!-- B6 -->
      <rect x="340" y="55" width="45" height="85"  fill="#162032" stroke="#334155" stroke-width=".5"/>
      <rect x="346" y="62" width="11" height="10"  fill="#fbbf24" opacity=".5"/>
      <rect x="362" y="62" width="11" height="10"  fill="#60a5fa" opacity=".6"/>
      <rect x="346" y="78" width="11" height="10"  fill="#60a5fa" opacity=".4"/>
      <rect x="362" y="78" width="11" height="10"  fill="#fbbf24" opacity=".3"/>
      <rect x="346" y="94" width="11" height="10"  fill="#fbbf24" opacity=".6"/>

      <!-- B7 -->
      <rect x="390" y="45" width="55" height="95"  fill="#1e293b" stroke="#334155" stroke-width=".5"/>
      <rect x="396" y="52" width="12" height="11"  fill="#60a5fa" opacity=".5"/>
      <rect x="414" y="52" width="12" height="11"  fill="#fbbf24" opacity=".4"/>
      <rect x="430" y="52" width="12" height="11"  fill="#60a5fa" opacity=".6"/>
      <rect x="396" y="69" width="12" height="11"  fill="#fbbf24" opacity=".3"/>
      <rect x="414" y="69" width="12" height="11"  fill="#60a5fa" opacity=".5"/>
      <rect x="396" y="86" width="12" height="11"  fill="#60a5fa" opacity=".6"/>
      <rect x="430" y="86" width="12" height="11"  fill="#fbbf24" opacity=".4"/>

      <!-- B8 far right -->
      <rect x="450" y="60" width="40" height="80"  fill="#162032" stroke="#334155" stroke-width=".5"/>
      <rect x="456" y="67" width="10" height="9"   fill="#fbbf24" opacity=".5"/>
      <rect x="472" y="67" width="10" height="9"   fill="#60a5fa" opacity=".4"/>
      <rect x="456" y="82" width="10" height="9"   fill="#60a5fa" opacity=".6"/>
      <rect x="472" y="82" width="10" height="9"   fill="#fbbf24" opacity=".3"/>

      <!-- B9 -->
      <rect x="495" y="35" width="60" height="105" fill="#1e293b" stroke="#334155" stroke-width=".5"/>
      <rect x="521" y="26" width="4"  height="12"  fill="#475569"/>
      <circle cx="523" cy="25" r="2.5" fill="#ef4444" filter="url(#glow)"/>
      <rect x="501" y="43" width="13" height="11"  fill="#60a5fa" opacity=".5"/>
      <rect x="520" y="43" width="13" height="11"  fill="#fbbf24" opacity=".4"/>
      <rect x="539" y="43" width="13" height="11"  fill="#60a5fa" opacity=".6"/>
      <rect x="501" y="60" width="13" height="11"  fill="#fbbf24" opacity=".3"/>
      <rect x="520" y="60" width="13" height="11"  fill="#60a5fa" opacity=".5"/>
      <rect x="539" y="60" width="13" height="11"  fill="#fbbf24" opacity=".6"/>
      <rect x="501" y="77" width="13" height="11"  fill="#60a5fa" opacity=".4"/>
      <rect x="539" y="77" width="13" height="11"  fill="#fbbf24" opacity=".5"/>

      <!-- Road -->
      <rect x="0" y="138" width="620" height="32" fill="url(#road)"/>
      <!-- road markings -->
      <rect x="0"   y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>
      <rect x="55"  y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>
      <rect x="110" y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>
      <rect x="165" y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>
      <rect x="220" y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>
      <rect x="275" y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>
      <rect x="330" y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>
      <rect x="385" y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>
      <rect x="440" y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>
      <rect x="495" y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>
      <rect x="555" y="153" width="40" height="3" fill="#fbbf24" rx="1" opacity=".7"/>

      <!-- Sidewalk -->
      <rect x="0" y="130" width="620" height="10" fill="#1e293b"/>

      <!-- Crowd (people silhouettes) -->
      <!-- Person 1 -->
      <g class="person" transform="translate(30,108)">
        <circle cx="0" cy="-18" r="5" fill="#94a3b8"/>
        <rect x="-4" y="-13" width="8" height="14" fill="#475569" rx="2"/>
        <rect x="-7" y="-1"  width="5" height="10" fill="#334155" rx="1"/>
        <rect x="2"  y="-1"  width="5" height="10" fill="#334155" rx="1"/>
      </g>
      <!-- Person 2 -->
      <g class="person" transform="translate(52,108)" style="animation-delay:-.4s">
        <circle cx="0" cy="-18" r="5" fill="#cbd5e1"/>
        <rect x="-4" y="-13" width="8" height="14" fill="#64748b" rx="2"/>
        <rect x="-7" y="-1"  width="5" height="10" fill="#475569" rx="1"/>
        <rect x="2"  y="-1"  width="5" height="10" fill="#475569" rx="1"/>
      </g>
      <!-- Person 3 -->
      <g class="person" transform="translate(155,110)" style="animation-delay:-.7s">
        <circle cx="0" cy="-18" r="5" fill="#94a3b8"/>
        <rect x="-4" y="-13" width="8" height="14" fill="#334155" rx="2"/>
        <rect x="-7" y="-1"  width="5" height="10" fill="#1e293b" rx="1"/>
        <rect x="2"  y="-1"  width="5" height="10" fill="#1e293b" rx="1"/>
      </g>
      <!-- Person 4 -->
      <g class="person" transform="translate(175,108)" style="animation-delay:-1.1s">
        <circle cx="0" cy="-18" r="5" fill="#e2e8f0"/>
        <rect x="-4" y="-13" width="8" height="14" fill="#475569" rx="2"/>
        <rect x="-7" y="-1"  width="5" height="10" fill="#334155" rx="1"/>
        <rect x="2"  y="-1"  width="5" height="10" fill="#334155" rx="1"/>
      </g>
      <!-- Person 5 -->
      <g class="person" transform="translate(355,109)" style="animation-delay:-.3s">
        <circle cx="0" cy="-18" r="5" fill="#94a3b8"/>
        <rect x="-4" y="-13" width="8" height="14" fill="#64748b" rx="2"/>
        <rect x="-7" y="-1"  width="5" height="10" fill="#475569" rx="1"/>
        <rect x="2"  y="-1"  width="5" height="10" fill="#475569" rx="1"/>
      </g>
      <!-- Person 6 -->
      <g class="person" transform="translate(375,108)" style="animation-delay:-.9s">
        <circle cx="0" cy="-18" r="5" fill="#cbd5e1"/>
        <rect x="-4" y="-13" width="8" height="14" fill="#1e3a5f" rx="2"/>
        <rect x="-7" y="-1"  width="5" height="10" fill="#1e293b" rx="1"/>
        <rect x="2"  y="-1"  width="5" height="10" fill="#1e293b" rx="1"/>
      </g>
      <!-- Person 7 -->
      <g class="person" transform="translate(500,110)" style="animation-delay:-.5s">
        <circle cx="0" cy="-18" r="5" fill="#94a3b8"/>
        <rect x="-4" y="-13" width="8" height="14" fill="#475569" rx="2"/>
        <rect x="-7" y="-1"  width="5" height="10" fill="#334155" rx="1"/>
        <rect x="2"  y="-1"  width="5" height="10" fill="#334155" rx="1"/>
      </g>
      <!-- Person 8 -->
      <g class="person" transform="translate(520,109)" style="animation-delay:-1.3s">
        <circle cx="0" cy="-18" r="5" fill="#e2e8f0"/>
        <rect x="-4" y="-13" width="8" height="14" fill="#334155" rx="2"/>
        <rect x="-7" y="-1"  width="5" height="10" fill="#1e293b" rx="1"/>
        <rect x="2"  y="-1"  width="5" height="10" fill="#1e293b" rx="1"/>
      </g>

      <!-- Ambulance (driving on road) -->
      <g class="ambulance-body" transform="translate(-110, 130)">
        <!-- Body -->
        <rect x="0"  y="0" width="100" height="34" fill="#f1f5f9" rx="4"/>
        <rect x="68" y="2" width="30"  height="22" fill="#e2e8f0" rx="3"/>
        <!-- cab window -->
        <rect x="70" y="5" width="26"  height="14" fill="#60a5fa" opacity=".7" rx="2"/>
        <!-- red stripe -->
        <rect x="0"  y="10" width="68" height="6"  fill="#ef4444"/>
        <!-- cross -->
        <rect x="28" y="13" width="12" height="4"  fill="#fff" rx="1"/>
        <rect x="32" y="9"  width="4"  height="12" fill="#fff" rx="1"/>
        <!-- AMBULANCE text -->
        <text x="8" y="26" fill="#1e293b" font-size="7" font-weight="700" font-family="Inter,sans-serif" letter-spacing="1">AMBULANCE</text>
        <!-- Wheels -->
        <circle cx="20"  cy="35" r="8" fill="#1e293b" stroke="#475569" stroke-width="2"/>
        <circle cx="20"  cy="35" r="3" fill="#475569"/>
        <circle cx="78"  cy="35" r="8" fill="#1e293b" stroke="#475569" stroke-width="2"/>
        <circle cx="78"  cy="35" r="3" fill="#475569"/>
        <!-- Sirens on roof -->
        <rect x="20" y="-8" width="60" height="7" fill="#cbd5e1" rx="2"/>
        <circle cx="32"  cy="-4" r="5" class="siren-left"  fill="#ef4444" filter="url(#glow)"/>
        <circle cx="68"  cy="-4" r="5" class="siren-right" fill="#3b82f6" filter="url(#glow)"/>
        <!-- headlights -->
        <ellipse cx="100" cy="22" rx="4" ry="3" fill="#fef08a" opacity=".9" filter="url(#glow)"/>
      </g>

      <!-- Street lamp -->
      <rect x="256" y="85"  width="4" height="48" fill="#334155"/>
      <rect x="248" y="85"  width="20" height="4"  fill="#334155" rx="2"/>
      <ellipse cx="258" cy="85" rx="10" ry="4" fill="#fef08a" opacity=".6" filter="url(#glow)"/>
      <rect x="458" y="85"  width="4" height="48" fill="#334155"/>
      <rect x="450" y="85"  width="20" height="4"  fill="#334155" rx="2"/>
      <ellipse cx="460" cy="85" rx="10" ry="4" fill="#fef08a" opacity=".6" filter="url(#glow)"/>
    </svg>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── News ticker ───────────────────────────────────────────────────────────────
ticker_items = [
    "Water contamination alert in Zone 3",
    "Sewage overflow reported on Main Road",
    "Emergency response team deployed to Ward 7",
    "Water quality testing underway in Sector 5",
    "Pipeline repair scheduled for tomorrow morning",
    "Citizens advised to boil water before use",
    "New water safety helpline: 1800-SAFE-H2O",
]
ticker_html = "".join(f'<span class="ticker-item">{t}</span>' for t in ticker_items * 2)
st.markdown(f"""
<div class="ticker-wrap">
  <div class="ticker-track">{ticker_html}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TWO COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
col_left, col_right = st.columns([1.1, 0.9], gap="large")

# ── LEFT: Complaints board ────────────────────────────────────────────────────
with col_left:
    items_html = ""
    for c in sorted_complaints():
        p    = c["priority"]
        items_html += f"""
<div class="complaint-item {p}-item">
  <div class="priority-dot dot-{p}"></div>
  <div style="flex:1">
    <div class="complaint-text">{c['text']}</div>
    <div class="complaint-meta">
      <span>📅 {c['date']}</span>
      <span class="badge badge-{p}">{p} priority</span>
    </div>
  </div>
</div>"""

    st.markdown(f"""
<div class="card">
  <h3>💧 WATER SAFETY COMPLAINTS</h3>
  {items_html}
</div>
""", unsafe_allow_html=True)

# ── RIGHT: Submit ─────────────────────────────────────────────────────────────
with col_right:
    st.markdown('<div class="card"><h3>📋 FILE A COMPLAINT</h3>', unsafe_allow_html=True)

    new_text = st.text_area(
        "Describe the issue",
        placeholder="e.g. There is sewage water flooding our street! This is dangerous and UNACCEPTABLE!!!",
        height=148,
        label_visibility="collapsed",
    )

    if st.button("🚨 Submit Emergency Report"):
        txt = new_text.strip()
        if txt:
            p = classify(txt)
            st.session_state.complaints.append({
                "text": txt,
                "priority": p,
                "date": datetime.date.today().strftime("%d %b %Y"),
            })
            icons = {"high":"🔴","medium":"🟡","low":"🟢"}
            st.success(f"{icons[p]} Complaint filed as **{p.upper()} PRIORITY**!")
            time.sleep(0.7)
            st.rerun()
        else:
            st.warning("Please describe the issue before submitting.")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CHAT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="card"><h3>🤖 PUBLIC SAFETY ASSISTANT</h3>', unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    cls   = "bubble-user" if msg["role"] == "user" else "bubble-ai"
    label = "You" if msg["role"] == "user" else "Assistant"
    st.markdown(
        f'<div class="chat-bubble {cls}"><div class="bubble-role">{label}</div>{msg["content"]}</div>',
        unsafe_allow_html=True,
    )

user_input = st.chat_input("Ask about water safety, emergency procedures, reporting incidents…")

if user_input:
    st.session_state.chat_history.append({"role":"user","content":user_input})
    st.markdown(
        f'<div class="chat-bubble bubble-user"><div class="bubble-role">You</div>{user_input}</div>',
        unsafe_allow_html=True,
    )
    with st.spinner("🚨 Connecting to safety officer…"):
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=(
                "You are an expert Public Safety Assistant embedded in a citizen emergency portal. "
                "You help citizens with water contamination complaints, sewage issues, public health hazards, "
                "emergency reporting, and municipal safety services. "
                "Be calm, professional, action-oriented, and concise. Use short paragraphs. "
                "For life-threatening situations, always advise contacting emergency services immediately."
            ),
            messages=st.session_state.chat_history,
        )
        reply = resp.content[0].text

    st.session_state.chat_history.append({"role":"assistant","content":reply})
    st.markdown(
        f'<div class="chat-bubble bubble-ai"><div class="bubble-role">Assistant</div>{reply}</div>',
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)
