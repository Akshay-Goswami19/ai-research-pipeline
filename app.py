import streamlit as st
import requests
import time
import threading

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --ink:     #0f0e0d;
    --paper:   #f5f0e8;
    --accent:  #c8410a;
    --green:   #1a6b4a;
    --amber:   #b07d1a;
    --muted:   #7a7060;
    --border:  #d9d0c0;
    --card-bg: #faf7f2;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--paper);
    color: var(--ink);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem; max-width: 1200px; }

/* ── Masthead ── */
.masthead {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    border-bottom: 2px solid #a89f90;
    padding-bottom: 0.75rem;
    margin-bottom: 2.5rem;
}
.masthead-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    line-height: 1;
    color: #f5f0e8 !important;
}
.masthead-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #a89f90 !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ── Input ── */
.stTextInput > div > div > input {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.15rem !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid var(--border) !important;
    border-radius: 0 !important;
    padding: 0.5rem 0.25rem !important;
    color: var(--paper) !important;
}
.stTextInput > div > div > input:focus {
    border-bottom-color: var(--accent) !important;
    box-shadow: none !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
}

/* ── Button ── */
.stButton > button {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 0.6rem 2rem !important;
    transition: background 0.15s, transform 0.1s;
}
.stButton > button:hover { background: #a33308 !important; transform: translateY(-1px); }
.stButton > button:active { transform: translateY(0); }

/* ── Pipeline bar ── */
.pipeline-bar {
    display: flex;
    margin: 2rem 0 2.5rem;
    border: 1.5px solid var(--border);
    border-radius: 3px;
    overflow: hidden;
}
.pipe-step {
    flex: 1;
    padding: 0.6rem 0.5rem;
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    background: var(--card-bg);
    border-right: 1px solid var(--border);
    transition: background 0.3s, color 0.3s;
}
.pipe-step:last-child { border-right: none; }
.pipe-step.active { background: var(--ink); color: #fff; }
.pipe-step.done   { background: var(--green); color: #fff; }
.pipe-icon { display: block; font-size: 1rem; margin-bottom: 2px; }

/* ── Section label ── */
.card-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Report body ── */
.report-body {
    background: var(--card-bg);
    border: 1.5px solid var(--border);
    border-radius: 3px;
    padding: 1.75rem 2rem;
}
.report-body p {
    font-size: 0.95rem;
    line-height: 1.8;
    margin-bottom: 0.85rem;
}
.report-body h1, .report-body h2, .report-body h3 {
    font-family: 'DM Serif Display', serif;
    margin: 1.4rem 0 0.5rem;
}
/* Fix numbered list: number + text stay on same line, wrapped text indents */
.report-body ol {
    padding-left: 0;
    margin: 0.75rem 0;
    list-style: none;
    counter-reset: report-counter;
}
.report-body ol li {
    counter-increment: report-counter;
    display: grid;
    grid-template-columns: 1.8rem 1fr;
    gap: 0 0.5rem;
    margin-bottom: 1rem;
    font-size: 0.95rem;
    line-height: 1.75;
}
.report-body ol li::before {
    content: counter(report-counter) ".";
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    color: var(--accent);
    padding-top: 0.05rem;
}
.report-body ul {
    padding-left: 1.4rem;
    margin: 0.75rem 0;
}
.report-body ul li {
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
    line-height: 1.75;
}

/* ── Score badge ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    font-family: 'DM Mono', monospace;
    font-size: 1.4rem;
    font-weight: 500;
    border: 2px solid currentColor;
    padding: 0.15rem 0.75rem;
    border-radius: 3px;
    margin-bottom: 1.2rem;
}

/* ── Feedback items ── */
.feedback-section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0.75rem 0 0.4rem;
}
.feedback-item {
    font-size: 0.88rem;
    line-height: 1.65;
    padding: 0.45rem 0.75rem;
    border-radius: 2px;
    margin-bottom: 0.35rem;
}
.feedback-strength {
    background: #edf7f1;
    border-left: 3px solid var(--green);
    color: #0f3d27;
}
.feedback-improve {
    background: #fff4ed;
    border-left: 3px solid var(--accent);
    color: #5c1e06;
}
.verdict-box {
    margin-top: 1.2rem;
    padding: 0.8rem 1rem;
    background: var(--card-bg);
    border: 1.5px solid var(--border);
    border-radius: 3px;
    font-family: 'DM Serif Display', serif;
    font-size: 1rem;
    font-style: italic;
    color: var(--ink);
    line-height: 1.6;
}

/* ── Feedback column wrapper ── */
.feedback-col {
    background: var(--card-bg);
    border: 1.5px solid var(--border);
    border-radius: 3px;
    padding: 1.75rem 1.75rem 1.5rem;
}

/* ── Source chips ── */
.source-chip {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.67rem;
    background: var(--ink);
    color: var(--paper);
    padding: 0.25rem 0.65rem;
    border-radius: 2px;
    margin: 0.2rem 0.3rem 0.2rem 0;
    word-break: break-all;
}
.source-chip a { color: var(--paper); text-decoration: none; }
.source-chip a:hover { text-decoration: underline; }

/* ── Error box ── */
.error-box {
    background: #fff0ed;
    border: 1.5px solid var(--accent);
    border-radius: 3px;
    padding: 1rem 1.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: var(--accent);
}

hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
.stSpinner > div { border-top-color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
API_BASE = "https://ai-research-pipeline.onrender.com/research"
PIPELINE_STEPS = [("🔍", "Search"), ("📄", "Scrape"), ("✍️", "Write"), ("🔎", "Critique")]

# ── Helpers ────────────────────────────────────────────────────────────────────
def render_pipeline(active_idx=-1, done_upto=-1):
    html = ""
    for i, (icon, label) in enumerate(PIPELINE_STEPS):
        cls = "pipe-step done" if i < done_upto else "pipe-step active" if i == active_idx else "pipe-step"
        html += f'<div class="{cls}"><span class="pipe-icon">{icon}</span>{label}</div>'
    st.markdown(f'<div class="pipeline-bar">{html}</div>', unsafe_allow_html=True)


def parse_feedback(text):
    score_val = ""
    strengths, improvements = [], []
    verdict = ""
    section = None
    for line in text.splitlines():
        s = line.strip()
        low = s.lower()
        if low.startswith("score:"):
            score_val = s.split(":", 1)[-1].strip()
        elif "strengths" in low and not s.startswith("-"):
            section = "strengths"
        elif ("areas to improve" in low or "weaknesses" in low) and not s.startswith("-"):
            section = "improvements"
        elif ("one line verdict" in low or low.startswith("verdict")) and not s.startswith("-"):
            section = "verdict"
        elif s.startswith("-"):
            content = s.lstrip("-").strip()
            if section == "strengths":
                strengths.append(content)
            elif section == "improvements":
                improvements.append(content)
        elif section == "verdict" and s and "verdict" not in low and "one line" not in low:
            verdict += s + " "
    return score_val, strengths, improvements, verdict.strip()


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <span class="masthead-title">ResearchMind</span>
    <span class="masthead-sub">Multi-agent research pipeline · v1.0</span>
</div>
""", unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], gap="medium")
with col_input:
    topic = st.text_input("Research topic", placeholder="e.g. Quantum computing breakthroughs in 2025")
with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run = st.button("Run →")

# ── Execution ──────────────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.markdown('<div class="error-box">⚠ Please enter a research topic before running.</div>', unsafe_allow_html=True)
    else:
        pipeline_ph = st.empty()
        status_ph   = st.empty()
        with pipeline_ph.container():
            render_pipeline(active_idx=0)

        try:
            result_holder = {"data": None, "error": None}

            def call_api():
                try:
                    r = requests.post(f"{API_BASE}/research", json={"topic": topic}, timeout=180)
                    r.raise_for_status()
                    result_holder["data"] = r.json()
                except requests.exceptions.ConnectionError:
                    result_holder["error"] = "connection"
                except requests.exceptions.Timeout:
                    result_holder["error"] = "timeout"
                except Exception as e:
                    result_holder["error"] = str(e)

            thread = threading.Thread(target=call_api, daemon=True)
            thread.start()

            steps_labels  = ["Searching the web…", "Scraping sources…", "Writing report…", "Critiquing report…"]
            step_durations = [8, 8, 12, 6]
            step_idx = step_elapsed = 0
            tick = 0.4

            with st.spinner(""):
                while thread.is_alive():
                    with pipeline_ph.container():
                        render_pipeline(active_idx=step_idx, done_upto=step_idx)
                    status_ph.markdown(
                        f'<div style="font-family:monospace;font-size:0.78rem;color:#7a7060;'
                        f'margin-top:-1rem;margin-bottom:1rem">● {steps_labels[step_idx]}</div>',
                        unsafe_allow_html=True,
                    )
                    time.sleep(tick)
                    step_elapsed += tick
                    if step_elapsed >= step_durations[step_idx] and step_idx < len(PIPELINE_STEPS) - 1:
                        step_idx += 1
                        step_elapsed = 0

            thread.join()
            with pipeline_ph.container():
                render_pipeline(done_upto=len(PIPELINE_STEPS))
            status_ph.empty()

            # ── Errors ────────────────────────────────────────────────────────
            if result_holder["error"] == "connection":
                st.markdown(
                    '<div class="error-box">⚠ Cannot reach the API at <code>localhost:8000</code>. '
                    'Start it with: <code>uvicorn main:app --reload</code></div>',
                    unsafe_allow_html=True)
            elif result_holder["error"] == "timeout":
                st.markdown('<div class="error-box">⚠ Request timed out (180 s). Try again.</div>', unsafe_allow_html=True)
            elif result_holder["error"]:
                st.markdown(f'<div class="error-box">⚠ {result_holder["error"]}</div>', unsafe_allow_html=True)

            else:
                data = result_holder["data"]
                st.markdown("<hr>", unsafe_allow_html=True)
                col_report, col_feedback = st.columns([3, 2], gap="large")

                # ── Report ────────────────────────────────────────────────────
                with col_report:
                    report_text = data.get("report", {}).get("content", "No report generated.")
                    st.markdown('<div class="card-label">📋 Research Report</div>', unsafe_allow_html=True)
                    st.markdown('<div class="report-body">', unsafe_allow_html=True)
                    st.markdown(report_text)
                    st.markdown('</div>', unsafe_allow_html=True)

                # ── Feedback ──────────────────────────────────────────────────
                with col_feedback:
                    feedback_text = data.get("feedback", {}).get("content", "No feedback generated.")
                    score_val, strengths, improvements, verdict = parse_feedback(feedback_text)

                    st.markdown('<div class="feedback-col">', unsafe_allow_html=True)
                    st.markdown('<div class="card-label">🔎 Critic Feedback</div>', unsafe_allow_html=True)

                    if score_val:
                        try:
                            n = float(score_val.split("/")[0])
                            color = "#1a6b4a" if n >= 7 else "#c8410a" if n < 5 else "#b07d1a"
                        except Exception:
                            color = "#c8410a"
                        st.markdown(
                            f'<div class="score-badge" style="color:{color};border-color:{color};">'
                            f'Score &nbsp; {score_val}</div>',
                            unsafe_allow_html=True)

                    if strengths:
                        st.markdown('<div class="feedback-section-label">✅ Strengths</div>', unsafe_allow_html=True)
                        for s in strengths:
                            st.markdown(f'<div class="feedback-item feedback-strength">▸ {s}</div>', unsafe_allow_html=True)

                    if improvements:
                        st.markdown('<div class="feedback-section-label" style="margin-top:1rem;">⚠ Areas to Improve</div>', unsafe_allow_html=True)
                        for imp in improvements:
                            st.markdown(f'<div class="feedback-item feedback-improve">▸ {imp}</div>', unsafe_allow_html=True)

                    if verdict:
                        st.markdown(f'<div class="verdict-box">💬 {verdict}</div>', unsafe_allow_html=True)

                    if not score_val and not strengths and not improvements:
                        st.markdown(feedback_text)

                    st.markdown('</div>', unsafe_allow_html=True)

                    sources = data.get("sources", [])
                    if sources:
                        st.markdown('<div class="card-label" style="margin-top:1.5rem;">🔗 Sources</div>', unsafe_allow_html=True)
                        chips = "".join(
                            f'<span class="source-chip"><a href="{s}" target="_blank">{s}</a></span>'
                            for s in sources)
                        st.markdown(f'<div style="margin-top:0.4rem">{chips}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f'<div class="error-box">⚠ Unexpected error: {e}</div>', unsafe_allow_html=True)

else:
    render_pipeline()
    st.markdown(
        '<div style="font-family:monospace;font-size:0.78rem;color:#7a7060;text-align:center;margin-top:3rem">'
        'Enter a topic above and press <strong>Run →</strong> to start the pipeline.</div>',
        unsafe_allow_html=True)