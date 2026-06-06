# ════════════════════════════════════════════════════════════
#  backend.py  —  All AI / Data Processing Logic
# ════════════════════════════════════════════════════════════

import tempfile, os, time, re
import streamlit as st

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

from config import SKILLS_MAP, SKILL_WEIGHTS


# ── Model loaders (cached) ────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@st.cache_resource(show_spinner=False)
def get_llm():
    return Ollama(model="tinyllama")


# ── PDF helpers ───────────────────────────────────────────────
def extract_text(pdf_bytes: bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        path = tmp.name
    try:
        loader = PDFPlumberLoader(path)
        docs   = loader.load()
        return " ".join(d.page_content for d in docs), docs
    finally:
        os.unlink(path)

def build_index(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=60)
    chunks   = splitter.split_documents(docs)
    db       = FAISS.from_documents(chunks, get_embeddings())
    return db, len(chunks)


# ── Skill detection ───────────────────────────────────────────
def detect_skills(text_lower: str, skills_map: dict) -> list:
    found = []
    for skill, aliases in skills_map.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill)
                break
    return list(set(found))


# ── Contact info extractors ───────────────────────────────────
def guess_name(text: str) -> str:
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    for line in lines[:6]:
        if 2 <= len(line.split()) <= 5 and line[0].isupper() and "@" not in line:
            return line
    return ""

def guess_email(text: str) -> str:
    m = re.search(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', text, re.I)
    return m.group(0) if m else ""

def guess_phone(text: str) -> str:
    m = re.search(r'(\+?\d[\d\s\-().]{8,14}\d)', text)
    return m.group(0).strip() if m else ""

def guess_linkedin(text: str) -> str:
    m = re.search(r'(linkedin\.com/in/[\w\-]+)', text, re.I)
    return "linkedin.com/in/..." if m else ""

def guess_github(text: str) -> str:
    m = re.search(r'(github\.com/[\w\-]+)', text, re.I)
    return "github.com/..." if m else ""


# ── ATS Score calculator ──────────────────────────────────────
def compute_score(matched, jd_skills, weights,
                  name, email, phone, linkedin, github) -> dict:
    """
    Internal breakdown (not shown to user):
      40 pts — Contact info  (Name/Email/Phone/LinkedIn/GitHub × 8 each)
      60 pts — Skills match  (weighted, normalised to 60)
    """
    contact_breakdown = {
        "Name":     8 if name     else 0,
        "Email":    8 if email    else 0,
        "Phone":    8 if phone    else 0,
        "LinkedIn": 8 if linkedin else 0,
        "GitHub":   8 if github   else 0,
    }
    contact_score = sum(contact_breakdown.values())

    total_possible = sum(weights.get(s, 10) for s in jd_skills)
    got            = sum(weights.get(s, 10) for s in matched)
    skills_score   = round((got / total_possible) * 60, 1) if total_possible > 0 else 0.0

    return {
        "total":             int(contact_score + skills_score),
        "contact_score":     contact_score,
        "skills_score":      int(skills_score),
        "contact_breakdown": contact_breakdown,
    }


# ── LLM calls ─────────────────────────────────────────────────
def llm_summary(resume_text: str, score: int) -> str:
    llm     = get_llm()
    snippet = resume_text[:1200]
    prompt  = (
        f"Read this resume snippet and write ONE sentence (max 20 words) "
        f"summarising the candidate's main profile and experience level.\n\n"
        f"Resume:\n{snippet}\n\nOne-sentence summary:"
    )
    try:
        return llm.invoke(prompt).strip().split("\n")[0]
    except Exception:
        return f"ATS Score: {score}%"

def llm_answer(question: str, context: str) -> str:
    llm    = get_llm()
    prompt = (
        f"Answer ONLY from the context below.\n"
        f"If the answer is not present, say 'Not found in document'.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )
    return llm.invoke(prompt).strip()


# ── History helper ─────────────────────────────────────────────
def push_history(label: str, kind: str = "📄"):
    item = {"label": label, "kind": kind, "ts": time.strftime("%H:%M")}
    st.session_state.history = [
        i for i in st.session_state.history if i["label"] != label
    ]
    st.session_state.history.insert(0, item)
    st.session_state.history = st.session_state.history[:12]
