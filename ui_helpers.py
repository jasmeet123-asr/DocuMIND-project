# ════════════════════════════════════════════════════════════
#  ui_helpers.py  —  Reusable UI Components & Global CSS
# ════════════════════════════════════════════════════════════

import streamlit as st

# ── Global CSS ────────────────────────────────────────────────
GLOBAL_CSS = (
    "<link href='https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800"
    "&family=JetBrains+Mono:wght@300;400;500&display=swap' rel='stylesheet'>"
    "<style>"
    "html,body,.stApp{"
    "background-color:#04080f !important;"
    "background-image:radial-gradient(ellipse 90% 50% at 50% -5%,rgba(56,189,248,0.07) 0%,transparent 65%),"
    "linear-gradient(rgba(56,189,248,0.022) 1px,transparent 1px),"
    "linear-gradient(90deg,rgba(56,189,248,0.022) 1px,transparent 1px) !important;"
    "background-size:100% 100%,56px 56px,56px 56px !important;"
    "color:#e2e8f0 !important;font-family:'Syne',sans-serif !important;}"
    "#MainMenu,footer,header{visibility:hidden !important;}"
    ".block-container{padding:1.2rem 2.2rem 4rem !important;max-width:1280px !important;}"
    "::-webkit-scrollbar{width:5px;height:5px;}"
    "::-webkit-scrollbar-thumb{background:#38bdf8;border-radius:3px;}"
    "[data-testid='stSidebar']{"
    "background:linear-gradient(180deg,#06101f,#040c1a) !important;"
    "border-right:1px solid rgba(56,189,248,0.1) !important;}"
    "[data-testid='stSidebar'] *{font-family:'Syne',sans-serif !important;}"
    "[data-testid='stSidebar'] .stButton>button{"
    "background:transparent !important;color:#64748b !important;"
    "border:1px solid rgba(56,189,248,0.12) !important;border-radius:10px !important;"
    "height:44px !important;font-size:13px !important;font-weight:600 !important;"
    "font-family:'Syne',sans-serif !important;box-shadow:none !important;"
    "margin-bottom:6px !important;transition:all 0.2s ease !important;transform:none !important;}"
    "[data-testid='stSidebar'] .stButton>button:hover{"
    "background:rgba(56,189,248,0.07) !important;border-color:rgba(56,189,248,0.35) !important;"
    "color:#e2e8f0 !important;transform:none !important;box-shadow:none !important;}"
    ".stSelectbox>div>div{"
    "background:rgba(8,18,38,0.88) !important;border:1px solid rgba(56,189,248,0.13) !important;"
    "border-radius:10px !important;color:#e2e8f0 !important;"
    "font-family:'JetBrains Mono',monospace !important;}"
    ".stTextInput>div>div>input{"
    "background:rgba(8,18,38,0.88) !important;border:1px solid rgba(56,189,248,0.13) !important;"
    "border-radius:10px !important;color:#e2e8f0 !important;"
    "font-family:'JetBrains Mono',monospace !important;font-size:14px !important;}"
    ".stTextInput>div>div>input:focus{"
    "border-color:#38bdf8 !important;box-shadow:0 0 0 2px rgba(56,189,248,0.12) !important;}"
    ".stTextArea>div>div>textarea{"
    "background:rgba(8,18,38,0.88) !important;border:1px solid rgba(56,189,248,0.13) !important;"
    "border-radius:10px !important;color:#e2e8f0 !important;"
    "font-family:'JetBrains Mono',monospace !important;font-size:13px !important;}"
    ".stTextArea>div>div>textarea:focus{"
    "border-color:#38bdf8 !important;box-shadow:0 0 0 2px rgba(56,189,248,0.12) !important;}"
    "[data-testid='stFileUploader']{"
    "background:rgba(8,18,38,0.5) !important;"
    "border:2px dashed rgba(56,189,248,0.32) !important;"
    "border-radius:14px !important;transition:all 0.3s ease;}"
    "[data-testid='stFileUploader']:hover{"
    "border-color:#38bdf8 !important;box-shadow:0 0 22px rgba(56,189,248,0.12) !important;}"
    "[data-testid='stAppViewContainer'] .stButton>button,"
    "[data-testid='stMain'] .stButton>button,"
    "section.main .stButton>button{"
    "background:linear-gradient(135deg,#1d4ed8,#7c3aed) !important;"
    "color:white !important;border:none !important;border-radius:11px !important;"
    "height:50px !important;width:100% !important;font-size:15px !important;"
    "font-family:'Syne',sans-serif !important;font-weight:700 !important;"
    "letter-spacing:0.3px !important;box-shadow:0 4px 20px rgba(124,58,237,0.3) !important;"
    "transition:all 0.25s ease !important;}"
    "[data-testid='stAppViewContainer'] .stButton>button:hover,"
    "[data-testid='stMain'] .stButton>button:hover,"
    "section.main .stButton>button:hover{"
    "transform:translateY(-2px) !important;box-shadow:0 8px 28px rgba(124,58,237,0.5) !important;}"
    ".stDownloadButton>button{"
    "background:rgba(52,211,153,0.08) !important;color:#34d399 !important;"
    "border:1px solid rgba(52,211,153,0.3) !important;border-radius:10px !important;"
    "font-family:'Syne',sans-serif !important;font-weight:600 !important;"
    "box-shadow:none !important;transform:none !important;}"
    ".stDownloadButton>button:hover{"
    "background:rgba(52,211,153,0.15) !important;"
    "transform:translateY(-1px) !important;box-shadow:none !important;}"
    "[data-testid='stMetric']{"
    "background:rgba(8,18,38,0.88) !important;border:1px solid rgba(56,189,248,0.13) !important;"
    "border-radius:14px !important;padding:18px 22px !important;transition:border-color 0.3s ease;}"
    "[data-testid='stMetric']:hover{border-color:rgba(56,189,248,0.38) !important;}"
    "[data-testid='stMetricValue']{"
    "color:#38bdf8 !important;font-family:'Syne',sans-serif !important;"
    "font-size:28px !important;font-weight:800 !important;}"
    "[data-testid='stMetricLabel']{"
    "color:#64748b !important;font-size:11px !important;text-transform:uppercase;"
    "letter-spacing:0.8px;font-family:'JetBrains Mono',monospace !important;}"
    ".stProgress>div>div>div>div{"
    "background:linear-gradient(90deg,#38bdf8,#a78bfa) !important;"
    "border-radius:99px !important;box-shadow:0 0 8px rgba(56,189,248,0.35);}"
    ".stProgress>div>div{"
    "background:rgba(255,255,255,0.05) !important;"
    "border-radius:99px !important;height:7px !important;}"
    "div[data-testid='stAlert']{border-radius:12px !important;}"
    "[data-testid='stDataFrame']{"
    "border:1px solid rgba(56,189,248,0.13) !important;"
    "border-radius:12px !important;overflow:hidden;}"
    "details{"
    "background:rgba(8,18,38,0.88) !important;border:1px solid rgba(56,189,248,0.13) !important;"
    "border-radius:12px !important;padding:4px 8px !important;}"
    "summary{color:#e2e8f0 !important;font-family:'Syne',sans-serif !important;}"
    ".stSpinner>div{border-top-color:#38bdf8 !important;}"
    "@keyframes fadeUp{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:translateY(0);}}"
    "@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.4;}}"
    "</style>"
)


# ── Reusable UI components ────────────────────────────────────
def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

def sec(icon, title, tag=""):
    tag_html = (
        f'<div style="font-family:JetBrains Mono,monospace;font-size:10px;color:#38bdf8;'
        f'text-transform:uppercase;letter-spacing:3px;margin-bottom:3px;">{tag}</div>'
    ) if tag else ""
    st.markdown(f"""
    <div style="margin:28px 0 14px;">
      {tag_html}
      <h2 style="font-family:Syne,sans-serif;font-size:20px;font-weight:700;
                 color:#e2e8f0;margin:0;">{icon}&nbsp; {title}</h2>
    </div>""", unsafe_allow_html=True)

def chip(skill, kind="match"):
    c = "#34d399" if kind == "match" else "#f87171"
    b = "rgba(52,211,153,0.1)"  if kind == "match" else "rgba(248,113,113,0.1)"
    d = "rgba(52,211,153,0.28)" if kind == "match" else "rgba(248,113,113,0.28)"
    i = "✦" if kind == "match" else "✕"
    return (
        f'<span style="display:inline-block;background:{b};border:1px solid {d};'
        f'color:{c};border-radius:6px;padding:4px 11px;margin:3px;'
        f'font-family:JetBrains Mono,monospace;font-size:12px;">{i} {skill}</span>'
    )

def score_col(s):
    return "#34d399" if s >= 80 else ("#fbbf24" if s >= 60 else "#f87171")

def card(content, border="#38bdf8", pad="22px 26px", extra=""):
    st.markdown(
        f'<div style="background:rgba(8,18,38,0.82);border:1px solid {border}33;'
        f'border-radius:16px;padding:{pad};{extra}">{content}</div>',
        unsafe_allow_html=True
    )

def footer():
    st.markdown("""
    <div style="margin-top:60px;border-top:1px solid rgba(56,189,248,0.07);padding-top:20px;
                text-align:center;font-family:'JetBrains Mono',monospace;
                font-size:10px;color:#0f2035;letter-spacing:1.5px;">
      DOCUMIND AI &nbsp;·&nbsp; STREAMLIT · LANGCHAIN · TINYLLAMA · FAISS
    </div>""", unsafe_allow_html=True)
