# ════════════════════════════════════════════════════════════
#  pages/document_qa.py  —  Document Q&A Page
# ════════════════════════════════════════════════════════════

import streamlit as st
from backend import extract_text, build_index, llm_answer, push_history
from ui_helpers import sec


def render():

    sec("💬", "Document Q&A", "UPLOAD · INDEX · ASK")

    qa_file = st.file_uploader(
        "Upload a PDF document to query",
        type="pdf", key="qa_uploader"
    )

    if qa_file is not None:

        # Re-index only when a new file is uploaded
        if st.session_state.pdf_filename != qa_file.name:
            with st.spinner("📚 Indexing document — please wait…"):
                _, docs      = extract_text(qa_file.read())
                db, n_chunks = build_index(docs)
                st.session_state.faiss_db     = db
                st.session_state.pdf_filename = qa_file.name
                st.session_state.pdf_chunks   = n_chunks
                st.session_state.qa_answer    = None
                st.session_state.qa_context   = None

        # File info card
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;
                    background:rgba(52,211,153,0.06);border:1px solid rgba(52,211,153,0.2);
                    border-radius:12px;padding:14px 20px;margin:14px 0 24px;">
          <span style="font-size:28px;">📎</span>
          <div>
            <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:700;color:white;">
              {qa_file.name}</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#64748b;margin-top:3px;">
              ✦ {st.session_state.pdf_chunks} chunks indexed and ready for questions
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Question input
        sec("❓", "Ask a Question", "NATURAL LANGUAGE QUERY")
        q_col, btn_col = st.columns([5, 1], gap="small")
        with q_col:
            query = st.text_input(
                "Question", value=st.session_state.qa_query,
                placeholder="e.g. What are the candidate's key technical skills?",
                label_visibility="collapsed", key="qa_query_input"
            )
        with btn_col:
            ask_btn = st.button("🔍 Ask", key="ask_btn")

        if ask_btn or (query and query != st.session_state.qa_query):
            if query.strip():
                with st.spinner("🧠 Searching document and generating answer…"):
                    results = st.session_state.faiss_db.similarity_search(query, k=3)
                    context = "\n\n".join(r.page_content for r in results)
                    answer  = llm_answer(query, context)
                st.session_state.qa_answer  = answer
                st.session_state.qa_context = context
                st.session_state.qa_query   = query
                push_history(query[:50] + ("…" if len(query) > 50 else ""), "💬")

        # Answer display
        if st.session_state.qa_answer:
            qa_l, qa_r = st.columns([3, 2], gap="large")

            with qa_l:
                st.markdown(f"""
                <div style="background:rgba(8,18,38,0.85);border:1px solid rgba(56,189,248,0.2);
                            border-radius:16px;padding:26px 28px;min-height:160px;">
                  <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#38bdf8;
                              letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;">
                    💡 Answer
                  </div>
                  <div style="font-family:'Syne',sans-serif;font-size:15px;color:#e2e8f0;line-height:1.8;">
                    {st.session_state.qa_answer}
                  </div>
                </div>""", unsafe_allow_html=True)

            with qa_r:
                ctx = (st.session_state.qa_context[:800]
                       .replace("<", "&lt;").replace(">", "&gt;"))
                st.markdown(f"""
                <div style="background:rgba(8,12,28,0.85);border:1px solid rgba(167,139,250,0.18);
                            border-radius:16px;padding:26px 28px;min-height:160px;">
                  <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#a78bfa;
                              letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;">
                    📖 Source Context
                  </div>
                  <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#475569;
                              line-height:1.85;max-height:280px;overflow-y:auto;">
                    {ctx}…
                  </div>
                </div>""", unsafe_allow_html=True)

            st.markdown("""
            <div style="margin-top:14px;font-family:'JetBrains Mono',monospace;
                        font-size:12px;color:#334155;text-align:center;">
              Type a new question above and click 🔍 Ask to continue
            </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center;padding:70px 20px;
                    border:2px dashed rgba(56,189,248,0.12);
                    border-radius:18px;margin-top:16px;">
          <div style="font-size:54px;margin-bottom:16px;">📄</div>
          <div style="font-family:'Syne',sans-serif;font-size:19px;font-weight:700;
                      color:#1e3a5f;margin-bottom:8px;">Upload a PDF to get started</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#0f2035;">
            Supports resumes, reports, research papers — any PDF document
          </div>
        </div>""", unsafe_allow_html=True)
