import re

def clean_text(text):
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def process_sections(parsed_docs):
    sections = []
    for doc in parsed_docs:
        for sec in doc['sections']:
            cleaned = clean_text(sec['text'])
            if cleaned:
                sections.append({
                    "document": doc['document'],
                    "title": sec['title'],
                    "text": cleaned,
                    "page_number": sec['page_number']
                })
    return sections




