import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re

def keyword_bonus(section_text, keywords, bonus_weight=0.1):
    """
    Compute a bonus score based on keyword occurrences in section_text.
    """
    count = 0
    for kw in keywords:
        # Case-insensitive exact word match count
        count += len(re.findall(fr'\b{re.escape(kw)}\b', section_text, flags=re.I))
    # Simple bonus: proportional to count scaled by bonus_weight
    return count * bonus_weight

def compute_scores(query_embedding, section_embeddings, sections, keywords=None, keyword_bonus_weight=0.15):
    """
    Compute combined scores (cosine similarity + keyword bonus).

    Returns list of (section, score) tuples.
    """
    scores = []
    # cosine_similarity expects 2D arrays
    query_emb = np.array(query_embedding).reshape(1, -1)
    section_embs = np.array(section_embeddings)
    cos_sims = cosine_similarity(query_emb, section_embs).flatten()

    keywords = keywords or []

    for sec, sim in zip(sections, cos_sims):
        bonus = 0.0
        if keywords:
            bonus = keyword_bonus(sec['text'], keywords, bonus_weight=keyword_bonus_weight)
        final_score = sim + bonus
        scores.append((sec, final_score))
    # Sort descending by score
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores
