import json
import os

def load_input(json_path):
    """
    Load and validate input JSON file.

    Expected format:
    {
        "documents": [
            {"filename": "sample1.pdf", "title": "Sample Document 1"},
            ...
        ],
        "persona": "Food Contractor",
        "job": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering..."
    }
    """
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"Input JSON not found: {json_path}")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Basic validation
    assert 'documents' in data and isinstance(data['documents'], list), "'documents' list missing"
    for doc in data['documents']:
        assert 'filename' in doc, "Each document must have a filename"
        if not os.path.isfile(os.path.join('data/input', doc['filename'])):
            raise FileNotFoundError(f"PDF file not found: {doc['filename']}")
    assert 'persona' in data and isinstance(data['persona'], str), "'persona' missing or not string"
    assert 'job' in data and isinstance(data['job'], str), "'job' missing or not string"

    return data
