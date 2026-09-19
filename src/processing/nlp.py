import re
from typing import List, Set

import spacy

from src.utils.keyword_mapping import expand_keywords_with_synonyms, map_keyword_to_group


_NLP = None


def _load_spacy_model():
    global _NLP
    if _NLP is not None:
        return _NLP
    try:
        _NLP = spacy.load("en_core_web_sm")
    except OSError:
        # Lazy download if model missing
        from spacy.cli import download

        download("en_core_web_sm")
        _NLP = spacy.load("en_core_web_sm")
    return _NLP


def normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_keywords(text: str, top_k: int = 15, use_synonyms: bool = True) -> List[str]:
    """Extract keywords with optional synonym expansion."""
    nlp = _load_spacy_model()
    doc = nlp(text)
    # Candidate phrases: noun chunks + entities; lowercase, dedupe, length filter
    candidates: List[str] = []
    candidates.extend([chunk.text.strip() for chunk in doc.noun_chunks])
    candidates.extend([ent.text.strip() for ent in doc.ents])

    clean: List[str] = []
    for c in candidates:
        c_norm = c.lower()
        c_norm = re.sub(r"[^a-z0-9\+\-#\. ]", "", c_norm)
        c_norm = c_norm.strip()
        if len(c_norm) < 3:
            continue
        if c_norm in ("the", "and", "for", "with", "from"):
            continue
        clean.append(c_norm)

    # Frequency-based top-k as a simple baseline extractor
    freq = {}
    for c in clean:
        freq[c] = freq.get(c, 0) + 1
    ranked = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
    base_keywords = [k for k, _ in ranked[:top_k]]
    
    if use_synonyms:
        # Expand with synonyms for better matching
        expanded = expand_keywords_with_synonyms(base_keywords)
        # Map to canonical groups where possible
        mapped = set()
        for kw in expanded:
            mapped.add(map_keyword_to_group(kw))
        return sorted(list(mapped))[:top_k * 2]  # Return more after expansion
    
    return base_keywords


