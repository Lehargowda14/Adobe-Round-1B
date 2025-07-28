import os
import fitz  # PyMuPDF
import re

def split_sections_on_headings(page_text):
    """
    Splits text into blocks based on academic/technical PDF section heading patterns.
    Returns a list of dicts each with 'title' and 'text'.
    """
    sections = []
    heading_pattern = re.compile(
        r"^(?:\d{1,2}(?:\.\d{1,2}){0,3})?\s*[A-Z][A-Za-z0-9 &\-/()]+$", re.MULTILINE)
    matches = list(heading_pattern.finditer(page_text))

    if not matches:
        return []

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(page_text)
        section_title = re.sub(r"^\d+(\.\d+)*\s*", "", match.group().strip())
        section_text = page_text[start:end].strip()
        if len(section_text) > 40:
            sections.append({"title": section_title, "text": section_text})

    return sections

def extract_section_title(page_text):
    """
    Attempts to extract a plausible section title from the first few lines of a text page.
    Returns None if no heading found.
    """
    lines = page_text.strip().splitlines()
    for line in lines[:8]:
        clean_line = re.sub(r"^\d+(\.\d+)*\s*", "", line.strip())
        if (clean_line.isupper() and len(clean_line) > 5) or (
            clean_line.istitle() and 6 < len(clean_line) < 70 and len(clean_line.split()) <= 10):
            return clean_line
    return None

def parse_pdfs(documents, pdf_dir="data/input"):
    parsed_docs = []
    for doc in documents:
        file_path = os.path.join(pdf_dir, doc['filename'])
        doc_sections = []

        if not os.path.isfile(file_path):
            print(f"Warning: PDF file not found: {file_path}, skipping.")
            parsed_docs.append({"document": doc['filename'], "sections": []})
            continue

        try:
            doc_fitz = fitz.open(file_path)
            for page_num in range(len(doc_fitz)):
                page = doc_fitz[page_num]
                text = page.get_text("text")

                subsections = split_sections_on_headings(text)

                if subsections:
                    for subsec in subsections:
                        doc_sections.append({
                            "title": subsec["title"],
                            "text": subsec["text"],
                            "page_number": page_num + 1
                        })
                else:
                    title = extract_section_title(text)
                    if not title:
                        title = f"Page {page_num + 1}"
                    if text.strip():
                        doc_sections.append({
                            "title": title,
                            "text": text,
                            "page_number": page_num + 1
                        })
        except Exception as e:
            print(f"Error parsing PDF '{file_path}': {e}")
            doc_sections = []

        parsed_docs.append({
            "document": doc['filename'],
            "sections": doc_sections
        })

    return parsed_docs




