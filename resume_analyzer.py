# ════════════════════════════════════════════════════════════
#  pages/resume_analyzer.py  —  Resume Analyzer Page
# ════════════════════════════════════════════════════════════

import time
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from config   import SKILLS_MAP, SKILL_WEIGHTS
from backend  import (extract_text, detect_skills, compute_score,
                      llm_summary, push_history, get_llm,
                      guess_name, guess_email, guess_phone,
                      guess_linkedin, guess_github)
from ui_helpers import sec, chip, score_col


# ── Upload view ───────────────────────────────────────────────
def _upload_view():
    col_up, col_jd = st.columns([1, 1], gap="large")

    with col_up:
        sec("📁", "Upload Resumes", "STEP 01")
        uploaded_files = st.file_uploader(
            "Upload PDFs", type="pdf", accept_multiple_files=True,
            label_visibility="collapsed", key="resume_uploader"
        )
        if uploaded_files:
            st.markdown(f"""
            <div style="background:rgba(52,211,153,0.07);border:1px solid rgba(52,211,153,0.22);
                        border-radius:10px;padding:10px 16px;margin-top:10px;">
              <span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#34d399;">
                ✦ {len(uploaded_files)} file{"s" if len(uploaded_files)>1 else ""} ready
              </span>
            </div>""", unsafe_allow_html=True)

    with col_jd:
        sec("📋", "Job Description", "STEP 02")
        job_description = st.text_area(
            "Paste JD", height=200,
            placeholder="Paste the full job description — required skills, responsibilities, qualifications…",
            label_visibility="collapsed", key="jd_input"
        )

    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        run_btn = st.button("⚡  Analyze & Rank Candidates", key="run_analysis")

    if run_btn:
        if not uploaded_files:
            st.warning("⚠️  Please upload at least one resume PDF.")
        elif not job_description.strip():
            st.warning("⚠️  Please paste a job description.")
        else:
            _run_analysis(uploaded_files, job_description)


# ── Analysis runner ───────────────────────────────────────────
def _run_analysis(uploaded_files, job_description):
    candidate_results = []
    prog  = st.progress(0, text="⏳ Starting analysis…")
    total = len(uploaded_files)

    for idx, uf in enumerate(uploaded_files):
        prog.progress(int((idx / total) * 85), text=f"🔍 Analysing {uf.name} ({idx+1}/{total})…")
        try:
            full_text, _ = extract_text(uf.read())
        except Exception as e:
            st.error(f"Could not read {uf.name}: {e}")
            continue

        resume_lower = full_text.lower()
        jd_lower     = job_description.lower()
        res_skills   = detect_skills(resume_lower, SKILLS_MAP)
        jd_skills    = detect_skills(jd_lower,     SKILLS_MAP)
        matched      = list(set(res_skills) & set(jd_skills))
        missing      = list(set(jd_skills)  - set(res_skills))
        extra        = list(set(res_skills) - set(jd_skills))
        name         = guess_name(full_text)
        email        = guess_email(full_text)
        phone        = guess_phone(full_text)
        linkedin     = guess_linkedin(full_text)
        github       = guess_github(full_text)
        score_data   = compute_score(matched, jd_skills, SKILL_WEIGHTS,
                                     name, email, phone, linkedin, github)

        candidate_results.append({
            "File":              uf.name,
            "Name":              name  or uf.name.replace(".pdf", ""),
            "Email":             email    or "—",
            "Phone":             phone    or "—",
            "LinkedIn":          linkedin or "—",
            "GitHub":            github   or "—",
            "Score":             score_data["total"],
            "Contact Score":     score_data["contact_score"],   # internal only
            "Skills Score":      score_data["skills_score"],    # internal only
            "Contact Breakdown": score_data["contact_breakdown"],
            "Matched Skills":    ", ".join(sorted(matched)),
            "Missing Skills":    ", ".join(sorted(missing)),
            "Extra Skills":      ", ".join(sorted(extra)),
            "Matched Count":     len(matched),
            "Missing Count":     len(missing),
            "Extra Count":       len(extra),
            "_text":             full_text,
        })

    prog.progress(90, text="🧠 Generating AI summaries…")
    for c in candidate_results:
        c["Summary"] = llm_summary(c["_text"], c["Score"])
        del c["_text"]

    prog.progress(100, text="✅ Done!")
    time.sleep(0.3)
    prog.empty()

    results_df = (
        pd.DataFrame(candidate_results)
        .sort_values("Score", ascending=False)
        .reset_index(drop=True)
    )
    st.session_state.analysis_results = results_df
    st.session_state.view = "results"
    push_history(f"Analyzed {len(uploaded_files)} resume(s)", "📄")
    st.rerun()


# ── Results view ──────────────────────────────────────────────
def _results_view():
    df  = st.session_state.analysis_results
    top = df.iloc[0]

    back_col, _ = st.columns([1, 6])
    with back_col:
        if st.button("⬅ Back", key="back_upload"):
            st.session_state.view = "upload"
            st.rerun()

    # Top candidate banner
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(56,189,248,0.09),rgba(167,139,250,0.09));
                border:1px solid rgba(56,189,248,0.28);border-radius:18px;
                padding:24px 30px;margin:26px 0 18px;display:flex;align-items:center;gap:20px;">
      <span style="font-size:40px;line-height:1;flex-shrink:0;">🏆</span>
      <div style="flex:1;min-width:0;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#38bdf8;
                    letter-spacing:2px;text-transform:uppercase;margin-bottom:3px;">Top Candidate</div>
        <div style="font-family:'Syne',sans-serif;font-size:21px;font-weight:800;
                    color:white;margin-bottom:4px;">{top['Name']}</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#64748b;">
          ATS Score: <span style="color:#38bdf8;font-weight:600;">{top['Score']}%</span>
          &nbsp;·&nbsp; {top['Email']} &nbsp;·&nbsp; #1 of {len(df)}
        </div>
        <div style="font-family:'Syne',sans-serif;font-size:13px;color:#94a3b8;
                    margin-top:6px;font-style:italic;">"{top['Summary']}"</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # KPI metrics
    sec("📊", "Overview", "METRICS")
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("📄 Resumes",    len(df))
    with k2: st.metric("🏆 Best Score", f"{top['Score']}%")
    with k3: st.metric("📈 Average",    f"{int(df['Score'].mean())}%")
    with k4: st.metric("🧩 JD Skills",  top['Matched Count'] + top['Missing Count'])

    # Leaderboard
    _render_leaderboard(df)

    # Deep dive
    _render_deep_dive(df)

    # Charts
    _render_charts(df)

    # Full table + CSV
    _render_table_and_export(df)


# ── Leaderboard ───────────────────────────────────────────────
def _render_leaderboard(df):
    sec("🏅", "Candidate Leaderboard", "RANKED BY ATS SCORE")
    medals = ["🥇", "🥈", "🥉"]
    for rank, row in df.iterrows():
        medal = medals[rank] if rank < 3 else "🏅"
        s     = int(row['Score'])
        col   = score_col(s)
        st.markdown(f"""
        <div style="background:rgba(8,18,38,0.82);border:1px solid rgba(56,189,248,0.1);
                    border-radius:16px;padding:18px 24px;margin-bottom:11px;
                    position:relative;overflow:hidden;">
          <div style="position:absolute;left:0;top:0;bottom:0;width:4px;
                      background:linear-gradient(180deg,#38bdf8,#a78bfa);
                      border-radius:16px 0 0 16px;"></div>
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
            <div style="min-width:0;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:2px;">
                <span style="font-size:20px;">{medal}</span>
                <span style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:white;">
                  {row['Name']}</span>
              </div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                          color:#475569;margin-left:28px;">{row['Email']} · {row['File']}</div>
              <div style="font-family:'Syne',sans-serif;font-size:12px;color:#64748b;
                          font-style:italic;margin-left:28px;margin-top:4px;">"{row['Summary']}"</div>
            </div>
            <span style="border:1px solid {col}44;border-radius:7px;padding:4px 13px;
                         font-family:'JetBrains Mono',monospace;font-size:13px;
                         color:{col};font-weight:600;flex-shrink:0;margin-left:12px;">{s}%</span>
          </div>
          <div style="background:rgba(255,255,255,0.04);border-radius:99px;height:5px;overflow:hidden;">
            <div style="height:100%;width:{s}%;background:linear-gradient(90deg,#38bdf8,#a78bfa);
                        border-radius:99px;box-shadow:0 0 8px rgba(56,189,248,0.35);"></div>
          </div>
          <div style="margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:10px;color:#334155;">
            Matched: {row['Matched Count']} &nbsp;·&nbsp;
            Missing: {row['Missing Count']} &nbsp;·&nbsp;
            Extra: {row['Extra Count']}
          </div>
        </div>""", unsafe_allow_html=True)


# ── Deep Dive ─────────────────────────────────────────────────
def _render_deep_dive(df):
    sec("🔍", "Candidate Deep Dive", "SELECT TO INSPECT")
    selected = st.selectbox("Candidate", df["Name"],
                            label_visibility="collapsed", key="deep_dive")
    cdata  = df[df["Name"] == selected].iloc[0]
    csc    = int(cdata['Score'])
    m_list = [s for s in cdata["Matched Skills"].split(", ") if s]
    x_list = [s for s in cdata["Missing Skills"].split(", ") if s]
    e_list = [s for s in cdata["Extra Skills"].split(", ")   if s]
    cb     = cdata["Contact Breakdown"]

    # Profile card + gauge
    prof_col, gauge_col = st.columns([3, 2], gap="large")

    with prof_col:
        def info_item(label, value, found):
            icon  = "✦" if found else "✕"
            color = "#34d399" if found else "#f87171"
            return (
                f'<div style="display:flex;align-items:center;gap:10px;padding:9px 0;'
                f'border-bottom:1px solid rgba(56,189,248,0.06);">'
                f'<span style="color:{color};font-size:13px;flex-shrink:0;">{icon}</span>'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:10px;color:#64748b;'
                f'text-transform:uppercase;letter-spacing:1px;width:70px;flex-shrink:0;">{label}</span>'
                f'<span style="font-family:JetBrains Mono,monospace;font-size:12px;color:#94a3b8;">{value}</span>'
                f'</div>'
            )
        rows = (
            info_item("Name",     cdata["Name"],     bool(cdata["Name"]))
            + info_item("Email",    cdata["Email"],    cdata["Email"]    != "—")
            + info_item("Phone",    cdata["Phone"],    cdata["Phone"]    != "—")
            + info_item("LinkedIn", cdata["LinkedIn"], cdata["LinkedIn"] != "—")
            + info_item("GitHub",   cdata["GitHub"],   cdata["GitHub"]   != "—")
        )
        st.markdown(f"""
        <div style="background:rgba(8,18,38,0.82);border:1px solid rgba(56,189,248,0.13);
                    border-radius:16px;padding:20px 24px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#38bdf8;
                      letter-spacing:2.5px;text-transform:uppercase;margin-bottom:14px;">
            Contact Profile</div>
          {rows}
          <div style="margin-top:14px;font-family:'Syne',sans-serif;font-size:12px;
                      color:#a78bfa;font-style:italic;">"{cdata['Summary']}"</div>
        </div>""", unsafe_allow_html=True)

    with gauge_col:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=csc,
            number={"suffix": "%", "font": {"size": 38, "color": "#e2e8f0", "family": "Syne"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#334155",
                         "tickfont": {"size": 10, "color": "#475569"}},
                "bar":  {"color": "#38bdf8", "thickness": 0.22},
                "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
                "steps": [
                    {"range": [0,  60], "color": "rgba(248,113,113,0.12)"},
                    {"range": [60, 80], "color": "rgba(251,191,36,0.12)"},
                    {"range": [80,100], "color": "rgba(52,211,153,0.12)"},
                ],
                "threshold": {"line": {"color": score_col(csc), "width": 3},
                              "thickness": 0.85, "value": csc}
            }
        ))
        gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Syne", color="#94a3b8"),
            margin=dict(l=20, r=20, t=30, b=10), height=220
        )
        st.plotly_chart(gauge, use_container_width=True)

        # Score breakdown bars (% only — no raw points shown)
        c_pct = int((cb.get("Name",0)+cb.get("Email",0)+cb.get("Phone",0)
                     +cb.get("LinkedIn",0)+cb.get("GitHub",0)) / 40 * 100)
        s_pct = int(cdata["Skills Score"] / 60 * 100)
        st.markdown(f"""
        <div style="background:rgba(8,18,38,0.7);border:1px solid rgba(56,189,248,0.1);
                    border-radius:12px;padding:14px 18px;">
          <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#64748b;">Contact Profile</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#38bdf8;">{c_pct}%</span>
          </div>
          <div style="background:rgba(255,255,255,0.05);border-radius:99px;height:6px;margin-bottom:12px;overflow:hidden;">
            <div style="height:100%;width:{c_pct}%;background:linear-gradient(90deg,#38bdf8,#34d399);border-radius:99px;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#64748b;">Skills Match</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#a78bfa;">{s_pct}%</span>
          </div>
          <div style="background:rgba(255,255,255,0.05);border-radius:99px;height:6px;overflow:hidden;">
            <div style="height:100%;width:{s_pct}%;background:linear-gradient(90deg,#a78bfa,#38bdf8);border-radius:99px;"></div>
          </div>
        </div>""", unsafe_allow_html=True)

    # 4 metrics
    dm1, dm2, dm3, dm4 = st.columns(4)
    with dm1: st.metric("ATS Score",  f"{csc}%")
    with dm2: st.metric("✅ Matched", len(m_list))
    with dm3: st.metric("❌ Missing", len(x_list))
    with dm4: st.metric("✨ Bonus",   len(e_list))

    # Skills chips
    sc1, sc2, sc3 = st.columns(3, gap="small")
    with sc1:
        matched_html = "".join(chip(s, "match") for s in m_list) or \
            '<span style="color:#1e3a5f;font-family:JetBrains Mono,monospace;font-size:12px;">None detected</span>'
        st.markdown(f"""
        <div style="background:rgba(8,18,38,0.75);border:1px solid rgba(52,211,153,0.18);
                    border-radius:14px;padding:18px;min-height:120px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#34d399;
                      letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">
            Matched Skills ({len(m_list)})</div>
          <div>{matched_html}</div>
        </div>""", unsafe_allow_html=True)

    with sc2:
        missing_html = "".join(chip(s, "miss") for s in x_list) or \
            '<span style="color:#34d399;font-family:JetBrains Mono,monospace;font-size:12px;">All skills present!</span>'
        st.markdown(f"""
        <div style="background:rgba(8,18,38,0.75);border:1px solid rgba(248,113,113,0.18);
                    border-radius:14px;padding:18px;min-height:120px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#f87171;
                      letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">
            Missing Skills ({len(x_list)})</div>
          <div>{missing_html}</div>
        </div>""", unsafe_allow_html=True)

    with sc3:
        bonus_html = "".join(
            f'<span style="display:inline-block;background:rgba(167,139,250,0.1);'
            f'border:1px solid rgba(167,139,250,0.25);color:#a78bfa;border-radius:6px;'
            f'padding:4px 10px;margin:3px;font-family:JetBrains Mono,monospace;font-size:12px;">★ {s}</span>'
            for s in e_list[:8]
        ) if e_list else '<span style="color:#334155;font-family:JetBrains Mono,monospace;font-size:12px;">None</span>'
        st.markdown(f"""
        <div style="background:rgba(8,18,38,0.75);border:1px solid rgba(167,139,250,0.18);
                    border-radius:14px;padding:18px;min-height:120px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#a78bfa;
                      letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">
            Bonus Skills ({len(e_list)})</div>
          <div>{bonus_html}</div>
        </div>""", unsafe_allow_html=True)

    # Hiring verdict
    sec("🤖", "Hiring Verdict", "AI DECISION")
    if csc >= 80:
        st.success(f"✅ **Highly Suitable** — Strong ATS score of {csc}%. Candidate matches most required skills and has a complete profile.")
    elif csc >= 60:
        st.warning(f"⚠️ **Moderately Suitable** — ATS score {csc}%. Good foundation but skill gaps remain.")
    else:
        st.error(f"❌ **Not Suitable** — ATS score {csc}%. Candidate lacks major required skills for this role.")

    # Improvement Tips
    sec("💡", "Resume Improvement Tips", "AI COACHING")
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#64748b;margin-bottom:12px;">
      Tell the candidate exactly what to add or improve to get a higher ATS score.
    </div>""", unsafe_allow_html=True)

    if st.button("💡 Generate Improvement Tips", key="gen_tips"):
        with st.spinner("💡 Analysing resume gaps..."):
            llm    = get_llm()
            prompt = (
                f"You are a professional resume coach. Give exactly 5 specific, "
                f"actionable tips to help this candidate improve their resume and ATS score.\n\n"
                f"Current ATS Score: {csc}%\n"
                f"Missing Skills: {', '.join(x_list)}\n"
                f"Has LinkedIn: {'Yes' if cdata['LinkedIn'] != '—' else 'No'}\n"
                f"Has GitHub: {'Yes' if cdata['GitHub'] != '—' else 'No'}\n"
                f"Has Phone: {'Yes' if cdata['Phone'] != '—' else 'No'}\n\n"
                f"Format as numbered list. Be specific and encouraging. No preamble."
            )
            st.session_state["tips_result"] = llm.invoke(prompt)
        push_history(f"Resume tips for {selected[:30]}", "💡")

    if st.session_state.get("tips_result"):
        tips      = [t.strip() for t in st.session_state["tips_result"].split("\n") if t.strip()]
        tip_icons = ["🔹", "🔸", "🔹", "🔸", "🔹"]
        tips_html = "".join(
            f'<div style="display:flex;gap:12px;padding:11px 0;'
            f'border-bottom:1px solid rgba(56,189,248,0.05);">'
            f'<span style="font-size:16px;flex-shrink:0;">{tip_icons[i % len(tip_icons)]}</span>'
            f'<span style="font-family:Syne,sans-serif;font-size:14px;'
            f'color:#e2e8f0;line-height:1.65;">{tip}</span>'
            f'</div>'
            for i, tip in enumerate(tips[:5])
        )
        st.markdown(f"""
        <div style="background:rgba(8,18,38,0.82);border:1px solid rgba(52,211,153,0.15);
                    border-radius:16px;padding:20px 24px;margin-top:12px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#34d399;
                      letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;">
            Personalised Improvement Plan</div>
          {tips_html}
        </div>""", unsafe_allow_html=True)


# ── Charts ────────────────────────────────────────────────────
def _render_charts(df):
    # Grab currently selected candidate's skill lists for pie/radar
    selected = st.session_state.get("deep_dive", df["Name"].iloc[0])
    cdata    = df[df["Name"] == selected].iloc[0]
    m_list   = [s for s in cdata["Matched Skills"].split(", ") if s]
    x_list   = [s for s in cdata["Missing Skills"].split(", ") if s]
    e_list   = [s for s in cdata["Extra Skills"].split(", ")   if s]

    sec("📊", "Visual Analytics", "CHARTS")
    cl, cr = st.columns([3, 2], gap="large")

    with cl:
        bar = go.Figure(go.Bar(
            x=df["Name"], y=df["Score"],
            text=[f"{s}%" for s in df["Score"]], textposition="outside",
            marker=dict(color=df["Score"],
                        colorscale=[[0, "#f87171"], [0.6, "#fbbf24"], [1, "#34d399"]],
                        line=dict(width=0))
        ))
        bar.update_layout(
            title=dict(text="ATS Score Comparison",
                       font=dict(family="Syne", size=14, color="#94a3b8")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="JetBrains Mono", color="#64748b"),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#64748b")),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
                       range=[0, 115], ticksuffix="%", tickfont=dict(color="#64748b")),
            margin=dict(l=10, r=10, t=36, b=10), height=300
        )
        st.plotly_chart(bar, use_container_width=True)

    with cr:
        pie = go.Figure(go.Pie(
            labels=["Matched", "Missing", "Bonus"],
            values=[max(len(m_list),1), max(len(x_list),1), max(len(e_list),1)],
            hole=0.55,
            marker=dict(colors=["#34d399", "#f87171", "#a78bfa"],
                        line=dict(color="#04080f", width=3))
        ))
        pie.update_layout(
            title=dict(text="Skill Coverage",
                       font=dict(family="Syne", size=14, color="#94a3b8")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="JetBrains Mono", color="#94a3b8"),
            legend=dict(font=dict(color="#64748b", size=11)),
            margin=dict(l=10, r=10, t=36, b=10), height=300
        )
        st.plotly_chart(pie, use_container_width=True)

    if m_list or x_list:
        sec("🕸️", f"Skill Radar — {selected}", "COVERAGE MAP")
        skills_for_radar = (m_list + x_list)[:14]
        r_vals = [100 if s in m_list else 0 for s in skills_for_radar]
        radar  = go.Figure(go.Scatterpolar(
            r=r_vals + [r_vals[0]], theta=skills_for_radar + [skills_for_radar[0]],
            fill="toself", fillcolor="rgba(56,189,248,0.09)",
            line=dict(color="#38bdf8", width=2)
        ))
        radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 100],
                               tickfont=dict(color="#334155", size=9),
                               gridcolor="rgba(255,255,255,0.05)"),
                angularaxis=dict(tickfont=dict(color="#64748b", size=11),
                                 gridcolor="rgba(255,255,255,0.05)")
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="JetBrains Mono", color="#64748b"),
            showlegend=False, margin=dict(l=40, r=40, t=20, b=20), height=380
        )
        st.plotly_chart(radar, use_container_width=True)


# ── Full table + CSV export ───────────────────────────────────
def _render_table_and_export(df):
    sec("📋", "Full Results Table", "ALL CANDIDATES")

    # Contact Score & Skills Score are internal — not shown here
    show_df = df[[
        "Name", "Email", "Phone", "LinkedIn", "GitHub", "Score",
        "Matched Count", "Missing Count", "Extra Count", "Summary"
    ]].copy()
    show_df.index = range(1, len(show_df) + 1)
    st.dataframe(show_df, use_container_width=True)

    with st.expander("🔎 View full skill details for all candidates"):
        detail_df = df[["Name", "Matched Skills", "Missing Skills", "Extra Skills"]].copy()
        detail_df.index = range(1, len(detail_df) + 1)
        st.dataframe(detail_df, use_container_width=True)

    csv_bytes = df.drop(
        columns=["Contact Breakdown", "Contact Score", "Skills Score"]
    ).to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥  Download Full Results as CSV",
        data=csv_bytes, file_name="documind_results.csv", mime="text/csv"
    )


# ── Main render entry point ───────────────────────────────────
def render():
    if st.session_state.view == "upload":
        _upload_view()
    elif st.session_state.view == "results" and st.session_state.analysis_results is not None:
        _results_view()
