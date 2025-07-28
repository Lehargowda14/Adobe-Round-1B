import os
import json

def create_input_json(pdf_folder='data/input', persona='', job='', output_path='data/input/input.json'):
    """
    Create input.json by scanning PDF files in the given folder,
    and setting persona and job strings.

    Args:
        pdf_folder (str): Path to folder containing PDF files.
        persona (str): Persona description string.
        job (str): Job-to-be-done description string.
        output_path (str): Path to save generated input.json.
    """
    # List PDF files in the given folder
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in {pdf_folder}. Please add some PDFs before running.")
        return

    documents = [{"filename": f, "title": os.path.splitext(f)[0]} for f in pdf_files]

    data = {
        "documents": documents,
        "persona": persona,
        "job": job
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"input.json created with {len(documents)} document(s) at: {output_path}")


if __name__ == '__main__':
    # You can customize these strings or extend to get input from command-line/interactive input.
    persona_input = "Travel Planner"
    job_input = "Plan a trip of 4 days for a group of 10 college friends."

    create_input_json(persona=persona_input, job=job_input)
