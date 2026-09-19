import re
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from src.utils.resume_extractor import extract_experience_years, extract_education, extract_certifications
from src.utils.keyword_mapping import EDUCATION_KEYWORDS


def _keyword_coverage(jd_keywords: List[str], resume_keywords: List[str]) -> float:
    if not jd_keywords:
        return 0.0
    if not resume_keywords:
        return 0.0
    jd_set = set(jd_keywords)
    res_set = set(resume_keywords)
    return len(jd_set.intersection(res_set)) / float(len(jd_set))


def _experience_match(jd_text: str, resume_exp_years: Optional[float]) -> float:
    """Match experience years from JD requirement with resume experience."""
    if resume_exp_years is None:
        return 0.5  # Neutral score if not found
    
    # Extract experience requirement from JD
    jd_lower = jd_text.lower()
    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)",
        r"(?:minimum|min|at least|required)\s+(\d+(?:\.\d+)?)\+?\s*years?",
    ]
    
    jd_required_years = None
    for pattern in patterns:
        matches = re.findall(pattern, jd_lower)
        if matches:
            try:
                jd_required_years = float(matches[0])
                break
            except (ValueError, IndexError):
                continue
    
    if jd_required_years is None:
        return 0.5  # No requirement specified, neutral
    
    # Score: 1.0 if meets or exceeds, decreasing if below
    if resume_exp_years >= jd_required_years:
        return 1.0
    elif resume_exp_years >= jd_required_years * 0.8:  # Within 20%
        return 0.8
    elif resume_exp_years >= jd_required_years * 0.6:  # Within 40%
        return 0.6
    else:
        return max(0.0, resume_exp_years / jd_required_years)


def _education_match(jd_text: str, resume_education: Dict[str, bool]) -> float:
    """Match education requirements from JD with resume education."""
    jd_lower = jd_text.lower()
    
    # Check what education JD requires
    jd_requires = {
        "phd": False,
        "masters": False,
        "bachelors": False,
        "diploma": False,
    }
    
    for degree_type, keywords in EDUCATION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in jd_lower:
                jd_requires[degree_type] = True
                break
    
    # If no education requirement, return neutral
    if not any(jd_requires.values()):
        return 0.5
    
    # Score based on highest degree match
    # Priority: PhD > Masters > Bachelors > Diploma
    if jd_requires["phd"] and resume_education.get("phd", False):
        return 1.0
    elif jd_requires["masters"] and resume_education.get("masters", False):
        return 1.0
    elif jd_requires["bachelors"] and resume_education.get("bachelors", False):
        return 1.0
    elif jd_requires["diploma"] and resume_education.get("diploma", False):
        return 1.0
    
    # Partial credit for higher degree than required
    if resume_education.get("phd", False):
        return 0.9
    elif resume_education.get("masters", False) and (jd_requires["bachelors"] or jd_requires["diploma"]):
        return 0.9
    elif resume_education.get("bachelors", False) and jd_requires["diploma"]:
        return 0.9
    
    return 0.0


def _certification_match(jd_text: str, resume_certs: List[str]) -> float:
    """Match certifications mentioned in JD with resume certifications."""
    if not resume_certs:
        return 0.5  # Neutral if no certs found
    
    jd_lower = jd_text.lower()
    cert_keywords = ["certified", "certification", "cert", "certificate"]
    
    # Check if JD mentions certifications
    jd_has_cert_requirement = any(kw in jd_lower for kw in cert_keywords)
    
    if not jd_has_cert_requirement:
        return 0.5  # No requirement, neutral
    
    # Check if any resume cert matches JD keywords
    resume_certs_lower = [c.lower() for c in resume_certs]
    jd_words = set(re.findall(r"\b\w+\b", jd_lower))
    
    matches = 0
    for cert in resume_certs_lower:
        cert_words = set(re.findall(r"\b\w+\b", cert))
        if cert_words.intersection(jd_words):
            matches += 1
    
    if matches > 0:
        return min(1.0, 0.5 + (matches * 0.2))  # Bonus for each match
    
    return 0.3  # Has certs but no match


def compute_scores(
    jd_text: str,
    jd_keywords: List[str],
    resumes: List[Dict],
    sim_matrix: np.ndarray,
    weight_similarity: float,
    weight_keywords: float,
    weight_experience: float = 0.0,
    weight_education: float = 0.0,
    weight_certifications: float = 0.0,
) -> pd.DataFrame:
    """Compute per-resume scores and return a ranked DataFrame.

    sim_matrix is cosine similarities for [JD, resume1, resume2, ...].
    """
    # Extract similarities between JD (row 0) and each resume (cols 1..N)
    jd_to_res_sims: List[float] = sim_matrix[0, 1:].tolist()

    rows = []
    for idx, resume in enumerate(resumes):
        similarity = float(max(0.0, min(1.0, jd_to_res_sims[idx])))
        kw_cov = _keyword_coverage(jd_keywords, resume.get("keywords", []))
        
        # New features
        exp_score = _experience_match(jd_text, resume.get("experience_years"))
        edu_score = _education_match(jd_text, resume.get("education", {}))
        cert_score = _certification_match(jd_text, resume.get("certifications", []))
        
        # Weighted total score
        total_weight = max(1e-6, (
            weight_similarity + weight_keywords + 
            weight_experience + weight_education + weight_certifications
        ))
        
        total_score = (
            weight_similarity * similarity +
            weight_keywords * kw_cov +
            weight_experience * exp_score +
            weight_education * edu_score +
            weight_certifications * cert_score
        ) / total_weight

        matched = sorted(list(set(jd_keywords).intersection(set(resume.get("keywords", [])))))
        
        # Format experience years for display
        exp_years_str = f"{resume.get('experience_years', 0):.1f}" if resume.get('experience_years') else "N/A"
        
        # Format education for display
        edu_list = []
        edu_dict = resume.get("education", {})
        if edu_dict.get("phd"): edu_list.append("PhD")
        if edu_dict.get("masters"): edu_list.append("Masters")
        if edu_dict.get("bachelors"): edu_list.append("Bachelors")
        if edu_dict.get("diploma"): edu_list.append("Diploma")
        edu_str = ", ".join(edu_list) if edu_list else "Not specified"
        
        rows.append({
            "filename": resume["filename"],
            "similarity": similarity,
            "keyword_coverage": kw_cov,
            "experience_score": exp_score,
            "education_score": edu_score,
            "certification_score": cert_score,
            "total_score": total_score,
            "experience_years": exp_years_str,
            "education": edu_str,
            "certifications": len(resume.get("certifications", [])),
            "matched_keywords": ", ".join(matched[:20]),
        })

    df = pd.DataFrame(rows)
    df = df.sort_values(["total_score", "similarity"], ascending=False).reset_index(drop=True)
    df.insert(0, "rank", df.index + 1)
    return df


