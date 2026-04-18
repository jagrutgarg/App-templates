import streamlit as st
import anthropic
import datetime
import time

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Environment Portal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS + JS (birds chirping via Web Audio API) ───────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@600;700&family=Nunito:wght@300;400;500;600&display=swap');

:root {
    --sky:      #e8f5e9;
    --meadow:   #c8e6c9;
    --forest:   #1b5e20;
    --trunk:    #5d4037;
    --leaf:     #2e7d32;
    --leaf2:    #388e3c;
    --leaf3:    #43a047;
    --accent:   #ff8f00;
    --water:    #0288d1;
    --surface:  #ffffff;
    --border:   #c8e6c9;
    --text:     #1b3a1f;
    --muted:    #558b60;
    --red:      #d32f2f;
    --yellow:   #f9a825;
    --green:    #2e7d32;
    --shadow:   rgba(27,94,32,0.12);
}

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background: var(--sky) !important;
    color: var(--text) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; max-width: 1200px; }

/* ══ HERO ══ */
.hero {
    background: linear-gradient(160deg, #a5d6a7 0%, #c8e6c9 40%, #e8f5e9 100%);
    border: 2px solid #81c784;
    border-radius: 24px;
    padding: 2rem 2.5rem 1.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px var(--shadow);
}
.hero::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 40px;
    background: linear-gradient(180deg, transparent, rgba(200,230,201,0.6));
}
.hero h1 {
    font-family: 'Lora', serif;
    font-size: 3rem;
    font-weight: 700;
    color: var(--forest);
    margin: 0 0 .3rem;
    text-shadow: 0 2px 8px rgba(27,94,32,0.15);
    letter-spacing: -0.5px;
}
.hero p { color: var(--muted); font-size: 1rem; margin: 0; font-weight: 500; }

/* ══ FOREST SCENE ══ */
.forest-scene {
    display: flex;
    align-items: flex-end;
    gap: 18px;
    padding: 1rem 2rem 0;
    overflow: hidden;
    height: 160px;
}
/* Bird animations */
.bird {
    position: absolute;
    animation: flyBird linear infinite;
    font-size: 1.1rem;
}
.bird:nth-child(1)  { top: 22px; animation-duration: 9s;  animation-delay: 0s; }
.bird:nth-child(2)  { top: 38px; animation-duration: 13s; animation-delay: -4s; }
.bird:nth-child(3)  { top: 15px; animation-duration: 11s; animation-delay: -7s; }
.bird:nth-child(4)  { top: 50px; animation-duration: 15s; animation-delay: -2s; }
.bird:nth-child(5)  { top: 28px; animation-duration: 10s; animation-delay: -9s; }
@keyframes flyBird {
    0%   { left: -60px;  transform: scaleX(1); }
    49%  { transform: scaleX(1); }
    50%  { left: 110%;   transform: scaleX(-1); }
    100% { left: -60px;  transform: scaleX(-1); }
}
/* Tree bob */
.tree-group { animation: treeSway 4s ease-in-out infinite alternate; transform-origin: bottom center; }
.tree-group:nth-child(even) { animation-duration: 5.5s; animation-direction: alternate-reverse; }
@keyframes treeSway {
    from { transform: rotate(-1.5deg); }
    to   { transform: rotate(1.5deg); }
}

/* ══ SECTION CARDS ══ */
.card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 18px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 4px 18px var(--shadow);
}
.card h3 {
    font-family: 'Lora', serif;
    font-size: 1.15rem;
    color: var(--forest);
    margin: 0 0 1rem;
}

/* ══ COMPLAINTS ══ */
.complaint-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: #f1f8f1;
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: .85rem 1rem;
    margin-bottom: .6rem;
    animation: slideIn .35s ease both;
}
@keyframes slideIn {
    from { opacity:0; transform: translateX(-14px); }
    to   { opacity:1; transform: translateX(0); }
}
.priority-dot {
    width: 13px; height: 13px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-top: 4px;
    box-shadow: 0 0 8px currentColor;
}
.dot-high   { background: var(--red);    color: var(--red); }
.dot-medium { background: var(--yellow); color: var(--yellow); }
.dot-low    { background: var(--green);  color: var(--green); }
.complaint-text { font-size: .9rem; line-height: 1.5; margin: 0 0 .3rem; color: var(--text); }
.complaint-meta { font-size: .72rem; color: var(--muted); display: flex; gap: 10px; align-items: center; }
.badge {
    font-size: .65rem; font-weight: 700; padding: 2px 8px;
    border-radius: 20px; text-transform: uppercase; letter-spacing: .5px;
}
.badge-high   { background: #ffcdd2; color: var(--red); }
.badge-medium { background: #fff8e1; color: #e65100; }
.badge-low    { background: #e8f5e9; color: var(--green); }

/* ══ INPUTS ══ */
.stTextArea textarea {
    background: #f1f8f1 !important;
    border: 1.5px solid #a5d6a7 !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: .9rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--forest) !important;
    box-shadow: 0 0 0 3px rgba(27,94,32,0.12) !important;
}
div.stButton > button {
    background: linear-gradient(135deg, #2e7d32, #1b5e20) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: .55rem 1.8rem !important;
    font-size: .9rem !important;
    font-family: 'Nunito', sans-serif !important;
    letter-spacing: .3px !important;
    box-shadow: 0 4px 12px rgba(27,94,32,0.25) !important;
}
div.stButton > button:hover { opacity: .88 !important; }

/* ══ CHAT BUBBLES ══ */
.chat-bubble {
    padding: .75rem 1rem;
    border-radius: 14px;
    margin-bottom: .55rem;
    max-width: 80%;
    font-size: .9rem;
    line-height: 1.55;
    animation: slideIn .3s ease both;
}
.bubble-user {
    background: #c8e6c9;
    border: 1.5px solid #a5d6a7;
    margin-left: auto;
    text-align: right;
}
.bubble-ai {
    background: #fff;
    border: 1.5px solid var(--border);
}
.bubble-role {
    font-size: .68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: .6px;
    color: var(--muted); margin-bottom: 4px;
}
</style>

<!-- Birds chirping sound via Web Audio API -->
<script>
(function(){
    var ctx, loop;
    function chirp(freq, t){
        var osc = ctx.createOscillator();
        var g   = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, t);
        osc.frequency.exponentialRampToValueAtTime(freq*1.4, t+0.07);
        osc.frequency.exponentialRampToValueAtTime(freq*0.9, t+0.14);
        g.gain.setValueAtTime(0, t);
        g.gain.linearRampToValueAtTime(0.18, t+0.03);
        g.gain.linearRampToValueAtTime(0, t+0.18);
        osc.connect(g); g.connect(ctx.destination);
        osc.start(t); osc.stop(t+0.22);
    }
    function birdCall(){
        var now = ctx.currentTime;
        var bird = [
            [1800,1900,2100],
            [2400,2000],
            [1600,1750,1900,2200],
            [2800,2600,2900],
        ][Math.floor(Math.random()*4)];
        bird.forEach(function(f,i){ chirp(f, now + i*0.22); });
    }
    function startChirping(){
        if(loop) return;
        loop = setInterval(function(){
            birdCall();
            if(Math.random()>.5) setTimeout(birdCall, 600+Math.random()*800);
        }, 2200 + Math.random()*1800);
        birdCall();
    }
    function init(){
        if(ctx) return;
        ctx = new (window.AudioContext||window.webkitAudioContext)();
        startChirping();
        document.removeEventListener('click', init);
    }
    document.addEventListener('click', init);
    window.addEventListener('load', function(){ setTimeout(function(){
        try{ ctx = new (window.AudioContext||window.webkitAudioContext)(); startChirping(); } catch(e){}
    }, 1000); });
})();
</script>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "complaints" not in st.session_state:
    st.session_state.complaints = [
        {"text": "River water is COMPLETELY BLACK with chemical waste! Children are getting sick! This is OUTRAGEOUS!", "priority": "high",   "date": (datetime.date.today()-datetime.timedelta(days=1)).strftime("%d %b %Y")},
        {"text": "Industrial effluents being dumped directly into the lake near Sector 4. Immediate action needed.", "priority": "medium", "date": (datetime.date.today()-datetime.timedelta(days=3)).strftime("%d %b %Y")},
        {"text": "Mild discoloration of tap water noticed in Block B. Please look into it when possible.",            "priority": "low",    "date": (datetime.date.today()-datetime.timedelta(days=6)).strftime("%d %b %Y")},
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Priority classifier ───────────────────────────────────────────────────────
ANGER = {"unacceptable","outrageous","disgusting","terrible","horrible","furious","angry",
         "pathetic","useless","worst","appalling","sick","enough","ridiculous","shameful",
         "criminal","disgusted","!!","!!!","fed up","infuriating","immediately","urgent"}

def classify(text):
    lo = text.lower()
    score  = sum(2 for w in ANGER if w in lo)
    score += text.count("!")
    score += (sum(1 for c in text if c.isupper()) / max(len(text),1)) * 12
    if score >= 5:   return "high"
    if score >= 1.5: return "medium"
    return "low"

def sorted_complaints():
    order = {"high":0,"medium":1,"low":2}
    return sorted(st.session_state.complaints, key=lambda x: order[x["priority"]])

# ══════════════════════════════════════════════════════════════════════════════
#  HERO with inline SVG forest + animated birds
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <!-- Flying birds -->
  <span class="bird">🐦</span>
  <span class="bird">🐦</span>
  <span class="bird">🐤</span>
  <span class="bird">🐦</span>
  <span class="bird">🐤</span>

  <div style="display:flex; align-items:center; gap:2rem; flex-wrap:wrap;">
    <div>
      <h1>🌿 Environment</h1>
      <p>Citizen portal · Environmental complaints · Green future</p>
    </div>

    <!-- SVG Forest Scene -->
    <svg width="520" height="140" viewBox="0 0 520 140" xmlns="http://www.w3.org/2000/svg" style="margin-left:auto; flex-shrink:0;">
      <!-- Sky gradient -->
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#b2dfdb"/>
          <stop offset="100%" stop-color="#e8f5e9"/>
        </linearGradient>
        <linearGradient id="grass" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#66bb6a"/>
          <stop offset="100%" stop-color="#388e3c"/>
        </linearGradient>
      </defs>
      <rect width="520" height="140" fill="url(#sky)" rx="12"/>
      <!-- Ground strip -->
      <rect x="0" y="112" width="520" height="28" fill="url(#grass)" rx="4"/>
      <!-- Sun -->
      <circle cx="470" cy="28" r="20" fill="#fff176" opacity=".85"/>
      <circle cx="470" cy="28" r="14" fill="#ffee58"/>

      <!-- Tree macro: trunk + 3 layered canopies -->
      <!-- Tree 1 (tall, centre-left) -->
      <g class="tree-group">
        <rect x="118" y="72" width="10" height="42" fill="#6d4c41" rx="3"/>
        <ellipse cx="123" cy="85" rx="22" ry="18" fill="#388e3c"/>
        <ellipse cx="123" cy="68" rx="18" ry="16" fill="#2e7d32"/>
        <ellipse cx="123" cy="54" rx="13" ry="13" fill="#1b5e20"/>
      </g>
      <!-- Tree 2 (medium, far left) -->
      <g class="tree-group" style="animation-delay:-.8s">
        <rect x="42"  y="82" width="8"  height="32" fill="#795548" rx="2"/>
        <ellipse cx="46"  cy="92" rx="17" ry="14" fill="#43a047"/>
        <ellipse cx="46"  cy="78" rx="14" ry="12" fill="#388e3c"/>
        <ellipse cx="46"  cy="66" rx="10" ry="10" fill="#2e7d32"/>
      </g>
      <!-- Tree 3 (small, very left) -->
      <g class="tree-group" style="animation-delay:-.3s">
        <rect x="12"  y="92" width="6"  height="22" fill="#8d6e63" rx="2"/>
        <ellipse cx="15"  cy="98" rx="12" ry="10" fill="#66bb6a"/>
        <ellipse cx="15"  cy="88" rx="10" ry="9"  fill="#43a047"/>
        <ellipse cx="15"  cy="79" rx="7"  ry="7"  fill="#388e3c"/>
      </g>
      <!-- Tree 4 (tall right) -->
      <g class="tree-group" style="animation-delay:-1.2s">
        <rect x="222" y="68" width="11" height="46" fill="#6d4c41" rx="3"/>
        <ellipse cx="228" cy="80" rx="24" ry="20" fill="#2e7d32"/>
        <ellipse cx="228" cy="62" rx="19" ry="17" fill="#1b5e20"/>
        <ellipse cx="228" cy="46" rx="14" ry="13" fill="#33691e"/>
      </g>
      <!-- Tree 5 -->
      <g class="tree-group" style="animation-delay:-.6s">
        <rect x="290" y="78" width="9"  height="36" fill="#795548" rx="2"/>
        <ellipse cx="295" cy="88" rx="20" ry="16" fill="#43a047"/>
        <ellipse cx="295" cy="73" rx="16" ry="14" fill="#388e3c"/>
        <ellipse cx="295" cy="60" rx="11" ry="11" fill="#2e7d32"/>
      </g>
      <!-- Tree 6 (far right tall) -->
      <g class="tree-group" style="animation-delay:-2s">
        <rect x="368" y="62" width="12" height="52" fill="#6d4c41" rx="3"/>
        <ellipse cx="374" cy="76" rx="26" ry="22" fill="#388e3c"/>
        <ellipse cx="374" cy="57" rx="21" ry="18" fill="#2e7d32"/>
        <ellipse cx="374" cy="40" rx="15" ry="14" fill="#1b5e20"/>
      </g>
      <!-- Tree 7 -->
      <g class="tree-group" style="animation-delay:-.4s">
        <rect x="452" y="80" width="8"  height="34" fill="#8d6e63" rx="2"/>
        <ellipse cx="456" cy="90" rx="18" ry="15" fill="#66bb6a"/>
        <ellipse cx="456" cy="76" rx="15" ry="13" fill="#43a047"/>
        <ellipse cx="456" cy="64" rx="11" ry="10" fill="#388e3c"/>
      </g>
      <!-- Tree 8 small far right -->
      <g class="tree-group" style="animation-delay:-1.7s">
        <rect x="498" y="90" width="7"  height="24" fill="#8d6e63" rx="2"/>
        <ellipse cx="502" cy="96" rx="13" ry="11" fill="#66bb6a"/>
        <ellipse cx="502" cy="85" rx="10" ry="9"  fill="#43a047"/>
      </g>

      <!-- Stream / water ripple -->
      <ellipse cx="170" cy="118" rx="42" ry="7" fill="#81d4fa" opacity=".6"/>
      <ellipse cx="170" cy="118" rx="28" ry="4" fill="#4fc3f7" opacity=".5"/>

      <!-- Deer silhouette -->
      <g opacity=".7" transform="translate(155,98)">
        <ellipse cx="0" cy="8" rx="10" ry="6" fill="#5d4037"/>
        <rect x="-2" y="2" width="4" height="8" fill="#5d4037" rx="2"/>
        <ellipse cx="-1" cy="1" rx="4" ry="3" fill="#5d4037"/>
        <!-- antlers -->
        <line x1="0" y1="-2" x2="-4" y2="-9" stroke="#5d4037" stroke-width="1.5"/>
        <line x1="0" y1="-2" x2="4"  y2="-9" stroke="#5d4037" stroke-width="1.5"/>
        <line x1="-4" y1="-9" x2="-6" y2="-6" stroke="#5d4037" stroke-width="1"/>
        <line x1="4" y1="-9"  x2="6"  y2="-6" stroke="#5d4037" stroke-width="1"/>
        <!-- legs -->
        <line x1="-5" y1="13" x2="-6" y2="20" stroke="#5d4037" stroke-width="2"/>
        <line x1="-1" y1="13" x2="-1" y2="20" stroke="#5d4037" stroke-width="2"/>
        <line x1="3"  y1="13" x2="4"  y2="20" stroke="#5d4037" stroke-width="2"/>
        <line x1="7"  y1="13" x2="8"  y2="20" stroke="#5d4037" stroke-width="2"/>
      </g>
    </svg>
  </div>
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
        dot  = f"dot-{c['priority']}"
        bdg  = f"badge-{c['priority']}"
        items_html += f"""
<div class="complaint-item">
  <div class="priority-dot {dot}"></div>
  <div style="flex:1">
    <div class="complaint-text">{c['text']}</div>
    <div class="complaint-meta">
      <span>📅 {c['date']}</span>
      <span class="badge {bdg}">{c['priority']} priority</span>
    </div>
  </div>
</div>"""

    st.markdown(f"""
<div class="card">
  <h3>💧 Environmental Water Complaints</h3>
  {items_html}
</div>
""", unsafe_allow_html=True)

# ── RIGHT: Submit ─────────────────────────────────────────────────────────────
with col_right:
    st.markdown('<div class="card"><h3>📝 Submit an Environmental Complaint</h3>', unsafe_allow_html=True)

    new_text = st.text_area(
        "Describe the issue",
        placeholder="e.g. The river near our village is completely polluted! This is absolutely unacceptable!",
        height=140,
        label_visibility="collapsed",
    )

    if st.button("Submit Complaint 🌿"):
        txt = new_text.strip()
        if txt:
            p = classify(txt)
            st.session_state.complaints.append({
                "text": txt,
                "priority": p,
                "date": datetime.date.today().strftime("%d %b %Y"),
            })
            icons = {"high":"🔴","medium":"🟡","low":"🟢"}
            st.success(f"{icons[p]} Filed as **{p.upper()} priority**!")
            time.sleep(0.7)
            st.rerun()
        else:
            st.warning("Please describe the environmental issue before submitting.")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CHAT ASSISTANT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="card"><h3>🤖 Environment Assistant</h3>', unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    cls   = "bubble-user" if msg["role"] == "user" else "bubble-ai"
    label = "You" if msg["role"] == "user" else "Assistant"
    st.markdown(
        f'<div class="chat-bubble {cls}"><div class="bubble-role">{label}</div>{msg["content"]}</div>',
        unsafe_allow_html=True,
    )

user_input = st.chat_input("Ask about pollution, water quality, environmental laws…")

if user_input:
    st.session_state.chat_history.append({"role":"user","content":user_input})
    st.markdown(
        f'<div class="chat-bubble bubble-user"><div class="bubble-role">You</div>{user_input}</div>',
        unsafe_allow_html=True,
    )
    with st.spinner("🌱 Thinking…"):
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=(
                "You are an expert Environmental Affairs Assistant embedded in a citizen portal. "
                "You help citizens with water pollution complaints, industrial waste issues, "
                "environmental regulations, green policies, and reporting environmental hazards. "
                "Be empathetic, actionable, and concise. Use short paragraphs."
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
