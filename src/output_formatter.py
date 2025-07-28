import json
from datetime import datetime
import re

def extract_sub_sections(text):
    """
    Extracts sub-sections from bullet-point style text.
    Returns a list of {title, text} dictionaries.
    """
    sub_sections = []
    
    # Regex pattern to find bullet-like points (• or - or numbered)
    pattern = re.compile(r"•\s*(.+?):\s*(.+?)(?=(?:•|$))", re.DOTALL)

    for match in pattern.finditer(text):
        title = match.group(1).strip()
        content = match.group(2).strip()
        sub_sections.append({
            "title": title,
            "text": content
        })

    return sub_sections if sub_sections else None

def build_output_json(top_sections, input_data, out_path="data/output/output.json"):
    """
    Create output JSON with metadata, results, and extracted sub-sections.
    """

    results = []
    for rank, (sec, score) in enumerate(top_sections, start=1):
        refined_text = sec.get('text', '')
        sub_sections = extract_sub_sections(refined_text)

        result = {
            "document": sec.get("document", ""),
            "section_title": sec.get("title", ""),
            "importance_rank": rank,
            "page_number": sec.get("page_number", -1),
            "refined_text": refined_text
        }

        if sub_sections:
            result["sub_sections"] = sub_sections

        results.append(result)

    output = {
        "metadata": {
            "documents": input_data.get('documents', []),
            "persona": input_data.get('persona', ""),
            "job": input_data.get('job', ""),
            "processed_at": datetime.utcnow().isoformat() + 'Z'
        },
        "results": results
    }

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Output JSON saved to {out_path}")


