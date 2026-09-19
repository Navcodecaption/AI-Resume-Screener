"""Keyword mapping and synonym grouping for better skill matching."""

from typing import Dict, List, Set

# Tech skill groups - maps related keywords to a canonical form
SKILL_GROUPS: Dict[str, List[str]] = {
    # Python ecosystem
    "python": ["python", "python3", "python 3", "py", "django", "flask", "fastapi", "pandas", "numpy", "scipy", "scikit-learn", "tensorflow", "pytorch", "keras"],
    "data_science": ["data science", "machine learning", "ml", "deep learning", "ai", "artificial intelligence", "data analysis", "data analytics", "statistics"],
    
    # Web frameworks
    "javascript": ["javascript", "js", "node.js", "nodejs", "react", "vue", "angular", "express", "next.js", "typescript"],
    "java": ["java", "spring", "spring boot", "hibernate", "maven", "gradle"],
    "dotnet": [".net", "dotnet", "c#", "asp.net", "aspnet", "entity framework"],
    
    # Cloud & DevOps
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "cloudformation", "cloudwatch"],
    "azure": ["azure", "microsoft azure", "azure devops", "azure functions"],
    "gcp": ["gcp", "google cloud", "google cloud platform", "gce", "cloud storage"],
    "docker": ["docker", "containerization", "containers", "dockerfile"],
    "kubernetes": ["kubernetes", "k8s", "kube", "helm"],
    
    # Databases
    "sql": ["sql", "mysql", "postgresql", "postgres", "oracle", "sql server", "mssql", "database"],
    "nosql": ["nosql", "mongodb", "cassandra", "redis", "dynamodb", "elasticsearch"],
    
    # Tools & Others
    "git": ["git", "github", "gitlab", "bitbucket", "version control"],
    "ci_cd": ["ci/cd", "jenkins", "github actions", "gitlab ci", "azure pipelines", "circleci", "travis"],
    "agile": ["agile", "scrum", "kanban", "sprint", "jira"],
}

# Education degree keywords
EDUCATION_KEYWORDS: Dict[str, List[str]] = {
    "phd": ["phd", "ph.d", "doctorate", "doctoral"],
    "masters": ["masters", "master", "ms", "m.sc", "mba", "m.tech", "mca"],
    "bachelors": ["bachelor", "bachelors", "bs", "b.sc", "b.tech", "be", "b.e", "bca", "b.com", "ba"],
    "diploma": ["diploma", "certificate"],
}

# Certification patterns
CERTIFICATION_PATTERNS: List[str] = [
    r"\b(aws|azure|gcp|google cloud)\s+(certified|certification)",
    r"\b(certified|certification|cert)\s+(.*?)\s+(professional|associate|expert)",
    r"\b(pmp|scrum|agile|cisp|ceh|ccna|ccnp|ocp|oracle)\s+(certified|certification)",
    r"\b(microsoft|oracle|salesforce|adobe)\s+(certified|certification)",
]


def normalize_keyword(keyword: str) -> str:
    """Normalize keyword to lowercase and remove special chars."""
    return keyword.lower().strip()


def map_keyword_to_group(keyword: str) -> str:
    """Map a keyword to its canonical group name if it exists."""
    keyword_norm = normalize_keyword(keyword)
    
    for group_name, synonyms in SKILL_GROUPS.items():
        if keyword_norm in [normalize_keyword(s) for s in synonyms]:
            return group_name
    
    return keyword_norm


def expand_keywords_with_synonyms(keywords: List[str]) -> Set[str]:
    """Expand keywords with their synonyms for better matching."""
    expanded = set()
    
    for kw in keywords:
        kw_norm = normalize_keyword(kw)
        expanded.add(kw_norm)
        
        # Check if this keyword belongs to any group
        group = map_keyword_to_group(kw)
        if group != kw_norm:
            # Add all synonyms from the group
            if group in SKILL_GROUPS:
                for synonym in SKILL_GROUPS[group]:
                    expanded.add(normalize_keyword(synonym))
        else:
            # Check if any group contains this keyword
            for group_name, synonyms in SKILL_GROUPS.items():
                if kw_norm in [normalize_keyword(s) for s in synonyms]:
                    expanded.add(group_name)
                    for synonym in synonyms:
                        expanded.add(normalize_keyword(synonym))
    
    return expanded


def get_skill_groups() -> Dict[str, List[str]]:
    """Return the skill groups mapping."""
    return SKILL_GROUPS.copy()


def get_education_keywords() -> Dict[str, List[str]]:
    """Return education degree keywords."""
    return EDUCATION_KEYWORDS.copy()

