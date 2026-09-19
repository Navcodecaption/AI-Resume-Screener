import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["TRANSFORMERS_NO_FLAX"] = "1"
os.environ["USE_TF"] = "0"
os.environ["USE_JAX"] = "0"

import io
from typing import List, Dict

import pandas as pd
import streamlit as st

from src.utils.parser import extract_text_from_file
from src.utils.resume_extractor import extract_all_resume_features
from src.processing.nlp import extract_keywords, normalize_text
from src.processing.embedding import get_embedder, embed_texts, cosine_similarity_matrix
from src.scoring import compute_scores


st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #F5F7FA;
}

section[data-testid="stSidebar"] {
    background-color: #E8EEF7;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_embedder():
    return get_embedder()


def main() -> None:
    st.title("AI Resume Screener")
    st.caption("Analyze and rank resumes against a job description using embeddings and keywords.")

    # Sidebar controls
    with st.sidebar:
        st.header("Scoring Weights")
        
        # Preset weight profiles
        st.subheader("📋 Quick Presets")
        preset_col1, preset_col2 = st.columns(2)
        
        # Initialize session state for weights if not exists
        if "weights" not in st.session_state:
            st.session_state.weights = {
                "similarity": 0.4, "keywords": 0.3, "experience": 0.15, 
                "education": 0.1, "certs": 0.05
            }
        
        with preset_col1:
            if st.button("🎯 Balanced", use_container_width=True):
                st.session_state.weights = {"similarity": 0.4, "keywords": 0.3, "experience": 0.15, "education": 0.1, "certs": 0.05}
                st.rerun()
            if st.button("💼 Senior Role", use_container_width=True):
                st.session_state.weights = {"similarity": 0.3, "keywords": 0.25, "experience": 0.3, "education": 0.1, "certs": 0.05}
                st.rerun()
        
        with preset_col2:
            if st.button("🚀 Entry Level", use_container_width=True):
                st.session_state.weights = {"similarity": 0.35, "keywords": 0.4, "experience": 0.05, "education": 0.15, "certs": 0.05}
                st.rerun()
            if st.button("☁️ Cloud Role", use_container_width=True):
                st.session_state.weights = {"similarity": 0.3, "keywords": 0.3, "experience": 0.15, "education": 0.1, "certs": 0.15}
                st.rerun()
        
        # Get weights from session state
        default_weights = st.session_state.weights
        
        st.divider()
        st.subheader("⚙️ Custom Weights")
        
        # Help tooltip
        with st.expander("ℹ️ Weights Kya Hain?"):
            st.markdown("""
            **Weights = Har factor ko kitna importance do**
            
            - **0.0** = Is factor ko ignore karo
            - **1.0** = Maximum importance
            - **0.5** = Medium importance
            
            **Example:**
            - Senior role ke liye Experience ko zyada weight do (0.3-0.4)
            - Entry level ke liye Keywords ko zyada weight do (0.4-0.5)
            - Cloud jobs ke liye Certifications ko zyada weight do (0.2-0.3)
            """)
        
        weight_similarity = st.slider(
            "Semantic Similarity", 
            0.0, 1.0, 
            default_weights["similarity"], 
            0.05,
            key="weight_similarity",
            help="Meaning-based similarity (JD aur resume ka overall match)"
        )
        weight_keywords = st.slider(
            "Keyword Coverage", 
            0.0, 1.0, 
            default_weights["keywords"], 
            0.05,
            key="weight_keywords",
            help="Exact skill keywords ka match (Python, AWS, etc.)"
        )
        weight_experience = st.slider(
            "Experience Match", 
            0.0, 1.0, 
            default_weights["experience"], 
            0.05,
            key="weight_experience",
            help="Years of experience ka match (JD requirement vs resume)"
        )
        weight_education = st.slider(
            "Education Match", 
            0.0, 1.0, 
            default_weights["education"], 
            0.05,
            key="weight_education",
            help="Degree level ka match (PhD, Masters, Bachelors)"
        )
        weight_certifications = st.slider(
            "Certifications", 
            0.0, 1.0, 
            default_weights["certs"], 
            0.05,
            key="weight_certifications",
            help="Certifications ka relevance (AWS, Azure, PMP, etc.)"
        )
        
        # Update session state when sliders change
        st.session_state.weights = {
            "similarity": weight_similarity,
            "keywords": weight_keywords,
            "experience": weight_experience,
            "education": weight_education,
            "certs": weight_certifications,
        }
        
        total_weight = weight_similarity + weight_keywords + weight_experience + weight_education + weight_certifications
        if total_weight == 0:
            st.warning("⚠️ Increase at least one weight to proceed.")
        else:
            # Show weight distribution
            st.info(f"📊 Total Weight: {total_weight:.2f}")
            
            # Visual weight distribution
            if total_weight > 0:
                st.markdown("**Weight Distribution:**")
                weight_data = {
                    "Similarity": weight_similarity / total_weight * 100,
                    "Keywords": weight_keywords / total_weight * 100,
                    "Experience": weight_experience / total_weight * 100,
                    "Education": weight_education / total_weight * 100,
                    "Certs": weight_certifications / total_weight * 100,
                }
                for name, pct in weight_data.items():
                    st.progress(pct / 100, text=f"{name}: {pct:.1f}%")
        
        st.divider()
        st.header("Keyword Options")
        num_keywords = st.slider("Top Keywords to Extract", 5, 30, 15)
        use_synonyms = st.checkbox("Use Keyword Synonyms", value=True, help="Group related skills (e.g., Python → Django, Pandas)")

    st.subheader("Job Description")
    jd_text = st.text_area("Paste the job description here", height=200, placeholder="Responsibilities...\nRequirements...\nTech stack...\nNice to haves...")

    st.subheader("Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload resume files (PDF, DOCX, or TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )

    if st.button("Analyze", type="primary"):
        if not jd_text:
            st.error("Please provide a job description.")
            return
        if not uploaded_files:
            st.error("Please upload at least one resume file.")
            return

        with st.spinner("Loading models and analyzing resumes..."):
            embedder = load_embedder()

            # Preprocess JD
            jd_clean = normalize_text(jd_text)
            jd_keywords = extract_keywords(jd_clean, top_k=num_keywords, use_synonyms=use_synonyms)

            # Parse resumes
            resume_records: List[Dict] = []
            for uf in uploaded_files:
                try:
                    content_bytes = uf.getvalue()
                    text = extract_text_from_file(uf.name, io.BytesIO(content_bytes))
                    text_clean = normalize_text(text)
                    kws = extract_keywords(text_clean, top_k=num_keywords, use_synonyms=use_synonyms)
                    
                    # Extract structured features
                    features = extract_all_resume_features(text_clean)
                    
                    resume_records.append({
                        "filename": uf.name,
                        "text": text_clean,
                        "keywords": kws,
                        "experience_years": features["experience_years"],
                        "education": features["education"],
                        "certifications": features["certifications"],
                        "recent_roles": features["recent_roles"],
                    })
                except Exception as e:
                    st.warning(f"Failed to parse {uf.name}: {e}")

            if not resume_records:
                st.error("No resumes could be processed.")
                return

            # Embeddings
            all_texts = [jd_clean] + [r["text"] for r in resume_records]
            embeddings = embed_texts(embedder, all_texts)
            sim_matrix = cosine_similarity_matrix(embeddings)

            # Scores
            scores_df = compute_scores(
                jd_text=jd_clean,
                jd_keywords=jd_keywords,
                resumes=resume_records,
                sim_matrix=sim_matrix,
                weight_similarity=weight_similarity,
                weight_keywords=weight_keywords,
                weight_experience=weight_experience,
                weight_education=weight_education,
                weight_certifications=weight_certifications,
            )

        st.success("Analysis complete")

        # Show JD keywords
        with st.expander("Top Job Description Keywords"):
            st.write(", ".join(jd_keywords))

        # Rankings table
        st.subheader("Ranked Resumes")
        
        # Select columns to display
        display_cols = [
            "rank", "filename", "total_score", 
            "similarity", "keyword_coverage",
            "experience_score", "education_score", "certification_score",
            "experience_years", "education", "certifications",
            "matched_keywords"
        ]
        
        st.dataframe(
            scores_df[display_cols]
            .sort_values("rank")
            .style.format({
                "total_score": "{:.3f}",
                "similarity": "{:.3f}",
                "keyword_coverage": "{:.3f}",
                "experience_score": "{:.3f}",
                "education_score": "{:.3f}",
                "certification_score": "{:.3f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

        # Visualization
        st.subheader("Score Visualization")
        
        # Main scores chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Overall Scores**")
            chart_df = scores_df[["filename", "similarity", "keyword_coverage", "total_score"]]
            st.bar_chart(chart_df.set_index("filename"))
        
        with col2:
            st.write("**Feature Scores**")
            feature_chart_df = scores_df[["filename", "experience_score", "education_score", "certification_score"]]
            st.bar_chart(feature_chart_df.set_index("filename"))
        
        # Detailed metrics
        with st.expander("📊 Detailed Metrics"):
            metrics_df = scores_df[["filename", "experience_years", "education", "certifications"]]
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        # Download results
        csv_bytes = scores_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Results (CSV)",
            data=csv_bytes,
            file_name="resume_scores.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()


