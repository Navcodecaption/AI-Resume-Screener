# 🤖 AI Resume Screener

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent resume screening system that automatically analyzes and ranks resumes against job descriptions using advanced NLP techniques. Built with Python, spaCy, Sentence-Transformers, and Streamlit.

## 🎯 Overview

This tool helps HR professionals and recruiters quickly identify the best candidates by:
- **Semantic Analysis**: Understanding resume meaning beyond keywords
- **Multi-Factor Scoring**: Experience, education, skills, and certifications
- **Smart Keyword Matching**: Groups related technologies (Python → Django, Pandas, etc.)
- **Interactive Dashboard**: Visual rankings and detailed metrics

## Features
- Upload multiple resumes (PDF, DOCX, or TXT)
- Paste a job description
- **Smart Keyword Extraction** with synonym grouping (e.g., Python → Django, Pandas, NumPy)
- **Semantic Similarity** using `all-MiniLM-L6-v2` embeddings
- **Experience Years Matching** - automatically extracts and matches experience requirements
- **Education Matching** - detects and matches degree requirements (PhD, Masters, Bachelors, Diploma)
- **Certification Detection** - identifies and scores certifications
- **Recent Roles Extraction** - extracts job titles and positions
- **Weighted Multi-Factor Scoring** with customizable weights
- **Interactive Dashboard** with dual visualizations
- **CSV Export** with all metrics

## Quickstart

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Run the app:

```bash
streamlit run app.py
```

4. In the UI:
- Paste the job description
- Upload resumes
- Click Analyze

## Notes
- The app attempts to lazily download `en_core_web_sm` if missing.
- For PDFs, it tries `pdfplumber` first then falls back to `PyPDF2`.
- Embeddings use `sentence-transformers/all-MiniLM-L6-v2` (downloads on first run).

## 📁 Project Structure
```
ai-resume-screener/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore               # Git ignore rules
└── src/
    ├── __init__.py
    ├── scoring.py            # Multi-factor scoring logic
    ├── processing/
    │   ├── embedding.py      # Sentence transformer embeddings
    │   └── nlp.py            # Keyword extraction with synonym support
    └── utils/
        ├── __init__.py
        ├── parser.py         # PDF/DOCX/TXT text extraction
        ├── keyword_mapping.py  # Skill groups and synonym mapping
        └── resume_extractor.py # Experience, education, certs extraction
```

## Scoring System

The total score is a weighted combination of:

1. **Semantic Similarity** (default: 0.4) - Meaning-based similarity using embeddings
2. **Keyword Coverage** (default: 0.3) - Exact skill keyword matches with synonym expansion
3. **Experience Match** (default: 0.15) - Years of experience vs JD requirement
4. **Education Match** (default: 0.1) - Degree level matching
5. **Certifications** (default: 0.05) - Certification relevance

### Keyword Mapping

The system groups related technologies:
- **Python** → Django, Flask, FastAPI, Pandas, NumPy, TensorFlow, PyTorch
- **JavaScript** → Node.js, React, Vue, Angular, TypeScript
- **Cloud** → AWS, Azure, GCP (grouped separately)
- **Databases** → SQL variants, NoSQL variants

### Experience Extraction

Automatically extracts experience from:
- Direct mentions: "5 years of experience"
- Date ranges: "2020 - Present" or "Jan 2020 - Dec 2023"
- Calculates total years from work history

### Education Detection

Recognizes:
- PhD, Doctorate
- Masters (MS, MBA, M.Tech, MCA)
- Bachelors (BS, B.Tech, BE, BCA, B.Com)
- Diploma, Certificate

### Certification Patterns

Detects:
- Cloud certifications (AWS, Azure, GCP)
- Professional certs (PMP, Scrum, Agile)
- Vendor certifications (Microsoft, Oracle, Salesforce)
- Custom patterns

## Customization

- **Adjust Weights**: Use sidebar sliders to prioritize different factors
- **Keyword Synonyms**: Toggle synonym grouping on/off
- **Keyword Count**: Adjust number of keywords extracted (5-30)

## 🛠️ Installation Notes

- The app attempts to lazily download `en_core_web_sm` if missing.
- For PDFs, it tries `pdfplumber` first then falls back to `PyPDF2`.
- Embeddings use `sentence-transformers/all-MiniLM-L6-v2` (downloads on first run).
- **Windows users**: Use CPU-only PyTorch to avoid DLL issues:
  ```bash
  pip install --index-url https://download.pytorch.org/whl/cpu torch==2.2.2+cpu
  ```

## 📦 Tech Stack

- **Python 3.10+**
- **Streamlit** - Web UI framework
- **spaCy** - NLP and keyword extraction
- **Sentence-Transformers** - Semantic embeddings
- **PyTorch** - Deep learning backend
- **pandas** - Data processing
- **pdfplumber/PyPDF2** - PDF parsing
- **python-docx** - DOCX parsing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🌐 Live Deployment

### Streamlit Cloud (Recommended - FREE)

1. **Streamlit Cloud pe jao:** https://share.streamlit.io/
2. **GitHub se sign in karo**
3. **New app create karo:**
   - Repository: `kunwardhruv/AI-Resume-Screener`
   - Branch: `main`
   - Main file: `app.py`
4. **Deploy!** (2-3 minutes me live ho jayega)

**Live URL:** Apko Streamlit Cloud se mil jayega (jaise: `https://ai-resume-screener.streamlit.app`)

**Note:** Pehli baar deployment me models download honge (5-10 minutes lag sakte hain)

### Other Platforms
- **Railway.app** - Alternative deployment option
- **Render.com** - Another free hosting option
- See `DEPLOYMENT.md` for detailed instructions

## 👤 Author

Created with ❤️ for efficient resume screening

---

**⭐ Star this repo if you find it useful!**

