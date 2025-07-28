import spacy
import json
import os

nlp = spacy.load("en_core_web_sm")

def extract_constraints(job_str):
    doc = nlp(job_str.lower())
    noun_phrases = set(chunk.text.strip() for chunk in doc.noun_chunks if len(chunk.text.strip()) > 2)
    blacklist = set()
    negation_cues = {'no', 'not', 'without', 'exclude', 'except', 'avoid'}
    for token in doc:
        if token.lower_ in negation_cues:
            blacklist_tokens = []
            for right in token.rights:
                if right.is_punct: break
                blacklist_tokens.append(right.text)
            phrase = ' '.join(blacklist_tokens).strip()
            if phrase:
                blacklist.add(phrase)
    whitelist = noun_phrases - blacklist
    whitelist = [w for w in whitelist if len(w) > 2]
    blacklist = [b for b in blacklist if len(b) > 2]
    return whitelist, blacklist

def expand_constraints(whitelist, blacklist, config_path):
    expanded_blacklist = set(blacklist)
    # Load constraint expansions (if present)
    if os.path.isfile(config_path):
        with open(config_path, "r") as f:
            expansions = json.load(f)
        for word in whitelist:
            for key, add_list in expansions.items():
                if key in word:
                    expanded_blacklist.update(add_list)
    return list(expanded_blacklist)

def filter_sections_auto(sections, whitelist, blacklist):
    wl_lower = [w.lower() for w in whitelist]
    bl_lower = [b.lower() for b in blacklist]
    filtered = []
    for sec, score in sections:
        text = sec['text'].lower()
        if wl_lower and not all(w in text for w in wl_lower):
            continue
        if bl_lower and any(b in text for b in bl_lower):
            continue
        filtered.append((sec, score))
    return filtered

