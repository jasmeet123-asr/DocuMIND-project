DocuMind AI is a final-year engineering project that combines Retrieval-Augmented Generation (RAG) with an intelligent ATS Resume Analyzer — all running locally on your machine, no cloud API required.
Features • Tech Stack • Installation • Usage • Project Structure

Features:
📄 Document Q&A (RAG Pipeline)

Upload any PDF document and ask questions in natural language
Answers are grounded in your document — no hallucinations
Powered by FAISS vector search + HuggingFace embeddings
Local LLM inference via Ollama (TinyLLaMA) — fully offline

📋 Resume Analyzer (ATS Scoring)

Paste your resume and a job description
Get a weighted ATS compatibility score with detailed breakdown
Analyzes: Skills match, Experience relevance, Education fit, Keyword density
Actionable feedback on what to improve


🛠 Tech Stack
LayerTechnologyLLMTinyLLaMA via Ollama (local inference)EmbeddingsHuggingFace sentence-transformersVector StoreFAISS (Facebook AI Similarity Search)RAG FrameworkLangChainFrontend UIStreamlitLanguagePython 3.10+

📁 Project Structure
DocuMind-AI/
├── app.py                  # Main entry point
├── config.py               # Configuration & constants
├── backend.py              # RAG pipeline & ATS scoring logic
├── ui_helpers.py           # Reusable UI components
├── pages/
│   ├── document_qa.py      # Document Q&A page
│   └── resume_analyzer.py  # Resume Analyzer page
└── requirements.txt

⚙️ Installation
Prerequisites

Python 3.10+
Ollama installed on your system

Steps
bash# 1. Clone the repository
git clone https://github.com/jasmeet123-asr/DocuMind-AI.git
cd DocuMind-AI

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Pull the TinyLLaMA model via Ollama
ollama pull tinyllama

# 4. Run the app
streamlit run app.py
The app will open at http://localhost:8501

🚀 Usage
Document Q&A

Navigate to the Document Q&A tab
Upload a PDF file
Wait for the document to be indexed
Type your question and get an AI-powered answer

Resume Analyzer

Navigate to the Resume Analyzer tab
Paste your Resume text
Paste the Job Description you're applying for
Click Analyze to get your ATS score and feedback


📸 Screenshots

Coming soon — UI walkthrough


🔮 Future Improvements

 Support for DOCX and TXT file formats
 Multi-document Q&A (query across multiple PDFs)
 Export ATS report as PDF
 Upgrade to larger LLMs (Mistral, LLaMA 3)
 Deploy to cloud (Streamlit Cloud / HuggingFace Spaces)


👨‍💻 Author
Jasmeet Singh

GitHub: @jasmeet123-asr
Final Year B.tech Student | AI & ML Enthusiast


📄 License
This project is licensed under the MIT License.
