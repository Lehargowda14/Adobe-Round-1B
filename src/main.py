import os
import re

from input_handler import load_input
from pdf_parser import parse_pdfs
from sectionizer import process_sections
from embedder import Embedder
from scorer import compute_scores
from ranker import select_top_sections
from output_formatter import build_output_json

def title_matches_job(section_title, section_text, job_text):
    """
    Returns True if any significant job keyword appears in section title or text.
    """
    job_keywords = [w.lower() for w in re.findall(r'\b\w+\b', job_text) if len(w) > 3]
    combined_text = (section_title + " " + section_text).lower()
    return any(k in combined_text for k in job_keywords)

def main():
    input_path = "data/input/input.json"
    pdf_dir = "data/input"
    model_path = "models/sentence_transformer"
    output_path = "data/output/output.json"
    top_n = 5

    input_data = load_input(input_path)

    print("Parsing PDFs...")
    raw_parsed = parse_pdfs(input_data['documents'], pdf_dir=pdf_dir)

    print("Processing sections...")
    structured_sections = process_sections(raw_parsed)
    print(f"Total sections: {len(structured_sections)}")

    job_text = input_data['job']
    filtered_sections = [sec for sec in structured_sections if title_matches_job(sec['title'], sec['text'], job_text)]
    print(f"Sections after job keyword filtering: {len(filtered_sections)}")

    if not filtered_sections:
        print("No sections matched job keywords; using all sections.")
        filtered_sections = structured_sections

    print("Loading embedding model...")
    embedder = Embedder(model_path=model_path)

    print("Embedding persona + job query...")
    query_text = (input_data['persona'] + " " + input_data['job']).strip()
    query_embedding = embedder.embed(query_text)

    print(f"Embedding {len(filtered_sections)} sections...")
    section_texts = [sec['text'] for sec in filtered_sections]
    section_embeddings = embedder.embed(section_texts)

    print("Computing scores...")
    keywords_for_scoring = re.findall(r'\b\w+\b', job_text.lower())
    scored_sections = compute_scores(query_embedding, section_embeddings, filtered_sections, keywords=keywords_for_scoring)

    top_sections = select_top_sections(scored_sections, N=top_n)
    print(f"Selected top {len(top_sections)} sections.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    build_output_json(top_sections, input_data, out_path=output_path)
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    main()




