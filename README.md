# 🤖 AI Resume Screener

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/) [![Streamlit](https://img.shields.io/badge/Streamlit-1.39+-red.svg)](https://streamlit.io/) [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An AI-powered resume screening application that analyzes and ranks resumes based on a job description. It uses Natural Language Processing (NLP), semantic similarity, and multi-factor scoring to help recruiters identify relevant candidates efficiently.

## Overview

The AI Resume Screener evaluates resumes against job requirements and generates rankings based on several factors, including skills, experience, education, certifications, and semantic similarity.

## Features

- **Multiple Resume Uploads:** Supports PDF, DOCX, and TXT files.
- **Semantic Similarity:** Compares resume content with job descriptions using sentence embeddings.
- **Keyword Extraction:** Identifies relevant skills and related technologies.
- **Experience Matching:** Extracts and evaluates professional experience.
- **Education Matching:** Identifies degree levels and educational qualifications.
- **Certification Detection:** Recognizes relevant professional certifications.
- **Multi-Factor Scoring:** Combines multiple evaluation factors into an overall score.
- **Interactive Dashboard:** Displays resume rankings and evaluation metrics.
- **CSV Export:** Allows users to export screening results for further analysis.
- **Customizable Scoring:** Adjusts the importance of different evaluation factors.

## Tech Stack

- **Python 3.10+** — Core programming language
- **Streamlit** — Interactive web interface
- **spaCy** — Natural Language Processing
- **Sentence-Transformers** — Semantic similarity and text embeddings
- **PyTorch** — Deep learning backend
- **pandas** — Data processing
- **pdfplumber / PyPDF2** — PDF text extraction
- **python-docx** — DOCX text extraction

## Project Structure

```text
ai-resume-screener/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── src/
    ├── __init__.py
    ├── scoring.py
    ├── processing/
    │   ├── embedding.py
    │   └── nlp.py
    └── utils/
        ├── __init__.py
        ├── parser.py
        ├── keyword_mapping.py
        └── resume_extractor.py
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- pip

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-resume-screener
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Download the spaCy English language model:

```bash
python -m spacy download en_core_web_sm
```

### 4. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## How to Use

1. Launch the application.
2. Enter or paste the job description.
3. Upload one or more resumes.
4. Start the resume analysis.
5. Review the candidate rankings and evaluation metrics.
6. Export the results as a CSV file if needed.

## Scoring System

The application calculates an overall score using five weighted factors.

| Evaluation Factor | Default Weight |
|---|---:|
| Semantic Similarity | 40% |
| Keyword Coverage | 30% |
| Experience Match | 15% |
| Education Match | 10% |
| Certification Relevance | 5% |
| **Total** | **100%** |

The scoring weights can be adjusted to prioritize different candidate evaluation criteria.

### Semantic Similarity

Uses the `sentence-transformers/all-MiniLM-L6-v2` model to compare the meaning of resume content with the job description.

### Keyword Mapping

Groups related technologies to improve skill matching. Examples include:

- **Python:** Django, Flask, FastAPI, Pandas, NumPy
- **JavaScript:** React, Angular, Vue, TypeScript, Node.js
- **Cloud Computing:** AWS, Microsoft Azure, Google Cloud
- **Databases:** SQL and NoSQL technologies

Related technologies are not necessarily interchangeable; their relevance depends on the job requirements.

### Experience and Education Matching

Identifies relevant information from resumes, including:

- Years of professional experience
- Employment dates and recent job roles
- Degree levels, such as bachelor's, master's, and doctoral degrees
- Relevant certifications and professional qualifications

## Configuration and Customization

The application can be customized to support different recruitment requirements.

- Adjust the weights assigned to scoring factors.
- Configure keyword extraction and synonym grouping.
- Change the number of keywords extracted.
- Extend the keyword mappings and resume information extraction rules.

## Deployment

The application can be deployed using Streamlit Community Cloud or another hosting platform that supports Python and Streamlit.

For deployment, configure the correct GitHub repository, branch, and main application file (`app.py`). Ensure that all dependencies are listed in `requirements.txt`.

The first run may require downloading the language model and sentence-transformer model, depending on the environment.

## Limitations

- Resume parsing accuracy depends on document formatting and text quality.
- Automated scores may not capture every aspect of a candidate's suitability.
- Similarity scores should be treated as decision-support information, not definitive hiring decisions.
- Candidate information should be handled securely and in accordance with applicable privacy requirements.

## Future Improvements

- Add support for more resume formats.
- Improve skill extraction and job-specific matching.
- Add detailed candidate comparison reports.
- Enhance explainability by showing which qualifications influenced each score.

## Contributing

Contributions, suggestions, and bug reports are welcome. Feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**Naveen Kumar Salla**

GitHub: [Visit my GitHub profile](https://github.com/)

---

If you find this project useful, consider giving the repository a ⭐ on GitHub.
