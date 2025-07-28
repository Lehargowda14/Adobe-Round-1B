# File: src/filters/general.py

import re

def filter_sections(sections, whitelist=None, blacklist=None):
    """
    Generic domain-agnostic filter:
    - whitelist: list of keywords/phrases ALL must appear in the section text
    - blacklist: list of keywords/phrases NONE should appear in the section text
    sections: list of tuples (section_dict, score)

    Returns: filtered list of tuples (section_dict, score)
    """
    whitelist = whitelist or []
    blacklist = blacklist or []

    filtered = []
    for sec, score in sections:
        text = sec['text'].lower()

        # Check all whitelist keywords exist in text
        if any(w.lower() not in text for w in whitelist):
            continue

        # Check no blacklist keywords exist in text
        if any(b.lower() in text for b in blacklist):
            continue

        filtered.append((sec, score))

    return filtered


def job_to_filters(job_str):
    """
    Extract whitelist and blacklist from job string, using heuristic rules.
    - Whitelist: meaningful keywords in job
    - Blacklist: expressions after 'no', 'without', 'exclude'.

    Returns dict with keys 'whitelist' and 'blacklist' to pass into filter_sections.
    """

    job_lower = job_str.lower()

    # Extract blacklist phrases appearing after "no", "without", "exclude" (simple heuristic)
    blacklist = re.findall(r'(?:no|without|exclude)\s([\w\s\-]+)', job_lower)

    # Basic tokenization for whitelist, excluding common stopwords and negatives
    stopwords = {
        'a', 'an', 'the', 'and', 'or', 'for', 'to', 'of', 'in', 'on',
        'at', 'by', 'with', 'as', 'from', 'including', 'include',
        'no', 'without', 'exclude', 'not', 'but', 'be', 'is', 'are', 'was',
    }
    words = re.findall(r'\b\w+\b', job_lower)
    whitelist = [w for w in words if w not in stopwords and w not in blacklist]

    return {'whitelist': whitelist, 'blacklist': blacklist}
