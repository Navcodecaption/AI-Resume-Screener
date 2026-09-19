"""Extract structured information from resume text: experience, education, certifications, roles."""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from src.utils.keyword_mapping import EDUCATION_KEYWORDS, CERTIFICATION_PATTERNS


def extract_experience_years(text: str) -> Optional[float]:
    """Extract total years of experience from resume text.
    
    Looks for patterns like:
    - "5 years of experience"
    - "3+ years"
    - "Experience: 7 years"
    - Date ranges in work history
    """
    text_lower = text.lower()
    
    # Pattern 1: Direct mentions like "5 years of experience"
    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s*(?:of\s*)?(?:experience|exp|work)",
        r"(?:experience|exp|work)\s*(?::|-)?\s*(\d+(?:\.\d+)?)\+?\s*years?",
        r"(\d+(?:\.\d+)?)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)",
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            try:
                years = float(matches[0])
                if 0 <= years <= 50:  # Sanity check
                    return years
            except (ValueError, IndexError):
                continue
    
    # Pattern 2: Calculate from date ranges (e.g., "Jan 2020 - Present" or "2020-2023")
    date_patterns = [
        r"(\d{4})\s*[-–—]\s*(?:present|current|now|\d{4})",
        r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})\s*[-–—]\s*(?:present|current|now|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4})",
    ]
    
    years_list = []
    current_year = datetime.now().year
    
    for pattern in date_patterns:
        matches = re.finditer(pattern, text_lower)
        for match in matches:
            try:
                start_year = int(match.group(1))
                end_text = text_lower[match.end():match.end()+20]
                if "present" in end_text or "current" in end_text or "now" in end_text:
                    end_year = current_year
                else:
                    end_match = re.search(r"(\d{4})", end_text)
                    if end_match:
                        end_year = int(end_match.group(1))
                    else:
                        end_year = current_year
                
                if 1950 <= start_year <= current_year and start_year <= end_year:
                    years_list.append(end_year - start_year)
            except (ValueError, IndexError):
                continue
    
    if years_list:
        # Sum all date ranges or take max
        total_years = sum(years_list)
        if total_years > 0 and total_years <= 50:
            return float(total_years)
    
    return None


def extract_education(text: str) -> Dict[str, bool]:
    """Extract education degrees mentioned in resume.
    
    Returns dict with keys: phd, masters, bachelors, diploma
    """
    text_lower = text.lower()
    education = {
        "phd": False,
        "masters": False,
        "bachelors": False,
        "diploma": False,
    }
    
    for degree_type, keywords in EDUCATION_KEYWORDS.items():
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, text_lower):
                education[degree_type] = True
                break
    
    return education


def extract_certifications(text: str) -> List[str]:
    """Extract certifications mentioned in resume."""
    certifications = []
    text_lower = text.lower()
    
    # Use predefined patterns
    for pattern in CERTIFICATION_PATTERNS:
        matches = re.finditer(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            cert = match.group(0).strip()
            if cert and cert not in certifications:
                certifications.append(cert)
    
    # Additional pattern: "Certified in X" or "X Certification"
    additional_patterns = [
        r"certified\s+in\s+([a-z\s]+?)(?:\s|$|,|\.)",
        r"([a-z\s]+?)\s+certification",
    ]
    
    for pattern in additional_patterns:
        matches = re.finditer(pattern, text_lower)
        for match in matches:
            cert = match.group(1).strip()
            if len(cert) > 3 and cert not in certifications:
                certifications.append(cert)
    
    return certifications[:10]  # Limit to top 10


def extract_recent_roles(text: str, top_n: int = 3) -> List[str]:
    """Extract recent job titles/roles from resume.
    
    Looks for patterns like:
    - "Senior Software Engineer"
    - "Position: Data Scientist"
    - "Role: Backend Developer"
    """
    roles = []
    text_lines = text.split('\n')
    
    # Common job title keywords
    title_keywords = [
        "engineer", "developer", "analyst", "manager", "lead", "architect",
        "scientist", "specialist", "consultant", "director", "executive",
        "designer", "administrator", "coordinator", "assistant"
    ]
    
    # Look for lines that might contain job titles
    for line in text_lines:
        line_lower = line.lower().strip()
        if len(line) < 5 or len(line) > 100:
            continue
        
        # Skip if line looks like contact info or dates
        if re.search(r"@|phone|email|linkedin|github|http", line_lower):
            continue
        
        # Check if line contains job title keywords
        has_title_keyword = any(kw in line_lower for kw in title_keywords)
        
        # Check for patterns like "Position:", "Role:", "Title:"
        has_role_prefix = re.search(r"^(position|role|title|designation)\s*:?\s*", line_lower)
        
        if has_title_keyword or has_role_prefix:
            # Clean the line
            cleaned = re.sub(r"^(position|role|title|designation)\s*:?\s*", "", line_lower, flags=re.IGNORECASE)
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            if cleaned and cleaned not in roles:
                roles.append(cleaned)
    
    return roles[:top_n]


def extract_all_resume_features(text: str) -> Dict:
    """Extract all structured features from resume text."""
    return {
        "experience_years": extract_experience_years(text),
        "education": extract_education(text),
        "certifications": extract_certifications(text),
        "recent_roles": extract_recent_roles(text),
    }

