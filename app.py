# ════════════════════════════════════════════════════════════
#  app.py  —  Entry Point
#  Run with:  streamlit run app.py
# ════════════════════════════════════════════════════════════

import streamlit as st

from config import DEFAULTS
from ui_helpers import inject_css, footer
from pages import resume_analyzer, document_qa


# ── Page config (must be first Streamlit call) ────────────────
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state ─────────────────────────────────────────────
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Global CSS ────────────────────────────────────────────────
inject_css()


# ════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:

    st.markdown("""
    <div style="padding:10px 0 20px;">
      <div style="font-family:'Syne',sans-serif;font-size:21px;font-weight:800;color:white;">
        📄 DocuMind AI
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#38bdf8;
                  letter-spacing:2px;margin-top:3px;">RECRUITMENT INTELLIGENCE v2</div>
    </div>
    <hr style="border:none;border-top:1px solid rgba(56,189,248,0.1);margin-bottom:16px;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;background:rgba(52,211,153,0.07);
                border:1px solid rgba(52,211,153,0.2);border-radius:8px;
                padding:8px 13px;margin-bottom:20px;">
      <span style="width:7px;height:7px;border-radius:50%;background:#34d399;
                   display:inline-block;flex-shrink:0;animation:pulse 2s infinite;"></span>
      <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#34d399;">
        TinyLLaMA · FAISS online
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#38bdf8;
                text-transform:uppercase;letter-spacing:2.5px;margin-bottom:10px;">
      🧭 Navigation
    </div>""", unsafe_allow_html=True)

    for icon, name in [("🗂️", "Resume Analyzer"), ("💬", "Document Q&A")]:
        active = st.session_state.page == name
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.rerun()
        if active:
            st.markdown("""
            <div style="height:2px;background:linear-gradient(90deg,#38bdf8,#a78bfa);
                        border-radius:99px;margin:-4px 4px 6px;opacity:0.7;"></div>
            """, unsafe_allow_html=True)

    st.markdown('<hr style="border:none;border-top:1px solid rgba(56,189,248,0.1);margin:14px 0 16px;">',
                unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#38bdf8;
                text-transform:uppercase;letter-spacing:2.5px;margin-bottom:10px;">
      📜 Search History
    </div>""", unsafe_allow_html=True)

    if st.session_state.history:
        for item in st.session_state.history:
            st.markdown(f"""
            <div style="background:rgba(56,189,248,0.04);border-left:3px solid rgba(56,189,248,0.3);
                        border-radius:0 8px 8px 0;padding:7px 11px;margin-bottom:5px;
                        display:flex;justify-content:space-between;align-items:center;">
              <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#94a3b8;
                           white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:160px;">
                {item['kind']} {item['label']}
              </span>
              <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                           color:#334155;flex-shrink:0;margin-left:6px;">{item['ts']}</span>
            </div>""", unsafe_allow_html=True)
        if st.button("🗑️  Clear History", key="clear_hist", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#1e3a5f;
                    padding:14px;text-align:center;
                    border:1px dashed rgba(56,189,248,0.1);border-radius:10px;">
          No activity yet
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <hr style="border:none;border-top:1px solid rgba(56,189,248,0.08);margin:16px 0;">
    <div style="background:rgba(124,58,237,0.07);border:1px solid rgba(167,139,250,0.16);
                border-radius:12px;padding:14px;">
      <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
                  color:#a78bfa;margin-bottom:8px;">⚙️ Tech Stack</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                  color:#475569;line-height:2.0;">
        TinyLLaMA · Ollama<br>FAISS · LangChain<br>
        HuggingFace · PDFPlumber<br>Streamlit · Plotly
      </div>
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  HERO BANNER
# ════════════════════════════════════════════════════════════
st.markdown("""
<div style="position:relative;overflow:hidden;
            background:linear-gradient(135deg,rgba(8,18,48,0.97),rgba(18,8,48,0.97));
            border:1px solid rgba(56,189,248,0.18);border-radius:22px;
            padding:44px 44px 36px;margin-bottom:20px;">
  <div style="position:absolute;top:-70px;right:-70px;width:280px;height:280px;border-radius:50%;
              background:radial-gradient(circle,rgba(124,58,237,0.14),transparent 70%);
              pointer-events:none;"></div>
  <h1 style="font-family:'Syne',sans-serif;font-size:clamp(34px,4.5vw,56px);
             font-weight:800;color:white;margin:0 0 10px;letter-spacing:-1px;line-height:1.1;">
    Docu<span style="background:linear-gradient(90deg,#38bdf8,#a78bfa);
                     -webkit-background-clip:text;-webkit-text-fill-color:transparent;">Mind</span> AI
  </h1>
  <p style="font-family:'JetBrains Mono',monospace;font-size:13px;color:#64748b;margin:0 0 22px;">
    Analyze resumes &nbsp;·&nbsp; Rank candidates &nbsp;·&nbsp; Ask questions from PDFs
  </p>
  <div style="display:flex;flex-wrap:wrap;gap:8px;">
    <span style="background:rgba(56,189,248,0.09);border:1px solid rgba(56,189,248,0.2);border-radius:7px;padding:5px 12px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#38bdf8;">⚡ Weighted ATS</span>
    <span style="background:rgba(167,139,250,0.09);border:1px solid rgba(167,139,250,0.2);border-radius:7px;padding:5px 12px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#a78bfa;">🧠 LLM Summaries</span>
    <span style="background:rgba(52,211,153,0.09);border:1px solid rgba(52,211,153,0.2);border-radius:7px;padding:5px 12px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#34d399;">📊 Radar Charts</span>
    <span style="background:rgba(251,191,36,0.09);border:1px solid rgba(251,191,36,0.2);border-radius:7px;padding:5px 12px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#fbbf24;">🏆 Leaderboard</span>
    <span style="background:rgba(248,113,113,0.09);border:1px solid rgba(248,113,113,0.2);border-radius:7px;padding:5px 12px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#f87171;">📥 CSV Export</span>
    <span style="background:rgba(56,189,248,0.09);border:1px solid rgba(56,189,248,0.2);border-radius:7px;padding:5px 12px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#38bdf8;">50+ Skills DB</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  TOP NAV BAR
# ════════════════════════════════════════════════════════════
nav_col1, nav_col2, hist_col = st.columns([1, 1, 2], gap="small")

with nav_col1:
    if st.button("🗂️  Resume Analyzer", key="nav_main_resume", use_container_width=True):
        st.session_state.page = "Resume Analyzer"
        st.rerun()

with nav_col2:
    if st.button("💬  Document Q&A", key="nav_main_qa", use_container_width=True):
        st.session_state.page = "Document Q&A"
        st.rerun()

with hist_col:
    history_pills = "".join(
        f'<span style="display:inline-block;background:rgba(56,189,248,0.06);'
        f'border:1px solid rgba(56,189,248,0.18);border-radius:6px;'
        f'padding:3px 10px;margin:2px;font-family:JetBrains Mono,monospace;'
        f'font-size:10px;color:#64748b;white-space:nowrap;overflow:hidden;'
        f'max-width:180px;text-overflow:ellipsis;">'
        f'{h["kind"]} {h["label"]}</span>'
        for h in st.session_state.history[:4]
    )
    no_hist = '<span style="font-family:JetBrains Mono,monospace;font-size:11px;color:#1e3a5f;">No history yet</span>'
    st.markdown(f"""
    <div style="background:rgba(8,18,38,0.6);border:1px solid rgba(56,189,248,0.1);
                border-radius:12px;padding:10px 16px;height:54px;
                display:flex;align-items:center;gap:8px;overflow:hidden;">
      <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                   color:#38bdf8;white-space:nowrap;flex-shrink:0;">📜 History:</span>
      <div style="display:flex;flex-wrap:nowrap;gap:4px;overflow:hidden;">
        {history_pills if history_pills else no_hist}
      </div>
    </div>""", unsafe_allow_html=True)

active_color = "#38bdf8" if st.session_state.page == "Resume Analyzer" else "#a78bfa"
st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;margin:10px 0 20px;padding:10px 18px;
            background:rgba(8,18,38,0.5);border-left:4px solid {active_color};
            border-radius:0 10px 10px 0;">
  <span style="width:8px;height:8px;border-radius:50%;background:{active_color};
               display:inline-block;animation:pulse 2s infinite;"></span>
  <span style="font-family:'JetBrains Mono',monospace;font-size:12px;
               color:{active_color};letter-spacing:1px;text-transform:uppercase;">
    Active: {st.session_state.page}
  </span>
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  PAGE ROUTER  — delegate to page modules
# ════════════════════════════════════════════════════════════
if st.session_state.page == "Resume Analyzer":
    resume_analyzer.render()

elif st.session_state.page == "Document Q&A":
    document_qa.render()


# ════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════
footer()
