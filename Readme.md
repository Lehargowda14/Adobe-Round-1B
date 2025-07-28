CHALLENGE1B – Round 1B Solution README

Overview

This repository contains the solution for Round 1B of the "Connecting the Dots" challenge. Our system acts as an intelligent document analyst, automatically extracting and prioritizing the most relevant sections from a collection of PDFs based on a given persona and their job-to-be-done.
The pipeline is built to be modular, reproducible, and fully containerized using Docker.

Directory Structure

CHALLENGE1B/
│
├── data/
│   ├── input/      # Place your PDF documents and input.json here
│   └── output/     # Output .json files will be saved here
│
├── models/
│   └── sentence_transformer/   # Pre-downloaded models
│
├── src/
│   ├── filters/                # Custom filtering logic
│   ├── __init__.py
│   ├── auto_constraint.py
│   ├── config.py
│   ├── embedder.py
│   ├── input_handler.py
│   ├── main.py                 # Pipeline entrypoint
│   ├── output_formatter.py
│   ├── pdf_parser.py
│   ├── ranker.py
│   ├── scorer.py
│   └── sectionizer.py
│
├── tools/
│   └── create_input_json.py    # Tool to create input.json file
│
├── Dockerfile
├── Readme.md
└── requirements.txt

Solution Workflow 

1.Input Preparation
* Place all your input PDF files in the /data/input directory.
* Generating input.json using the create_input_json.py script in tools/ is optional:
    If you already have an input.json file prepared, you can skip this step.
    Otherwise, run the tool to create a new input.json by executing:
     python tools/create_input_json.py

* Follow the prompts to enter persona and job details. This generates an input.json file required for the main pipeline.
* Ensure the input.json file is in the /data/input directory alongside your PDFs.

2.Docker Build
Build the Docker image (ensuring you are in the repository root):
docker build -t mysolution:latest .

3.Running the Solution
Run the pipeline with your input and output folders mounted:

docker run --rm \
  -v "$(pwd)/data/input:/app/data/input" \
  -v "$(pwd)/data/output:/app/data/output" \
  --network none \
  mysolution:latest

The system will process all PDFs in /app/data/input, use the input.json for persona/job context, and generate output JSON(s) in /app/data/output.


Approach & Methodology

1.Document Parsing: Extracts full structural outlines (titles, headings, hierarchy, etc.) using robust PDF parsing and NLP segmentation.
2.Persona & Job Conditioning: Tailors section relevance ranking by using embeddings and semantic matching between the persona/job definition and document sections.
3.Ranking & Selection:
Each section (and sub-section) is embedded and scored for contextual relevance.
The most relevant sections are prioritized and refined, ensuring the output aligns closely with the persona's job-to-be-done.
4.Output Formatting: Results conform strictly to the specified JSON schema, including:
  Full metadata,
  Ranked relevant sections,
  Granular sub-section analysis.

Technical Notes

1.Offline & CPU Compliance:
All dependencies and models are pre-installed during image build.
No internet access is required or used during execution.
2.Efficiency:
The solution is optimized to process a collection of 3-10 PDFs within 60 seconds on CPU, per challenge requirements.
3.Modularity:
Major logic components such as parsing, embedding, ranking, and formatting are decoupled in src/ for maintainability and reuse.

Additional Tips

1.Test with various PDF types (research papers, reports, textbooks) to validate generalization.
2.The output.json in /data/output reflects the ranked and refined extraction, ready for downstream consumption.

Sample Test Example

We tested the solution using the following scenario that aligns with the Round 1B challenge:

Persona: Travel Planner
Job-to-be-Done: Plan a 4-day trip for a group of 10 college friends

Documents Used: 7 travel guides about the South of France:
South of France - Traditions and Culture.pdf
South of France - Cities.pdf
South of France - Things to Do.pdf
South of France - History.pdf
South of France - Restaurants and Hotels.pdf
South of France - Cuisine.pdf
South of France - Tips and Tricks.pdf

Details:
1.The input PDFs were placed in the /data/input directory.
2.The input.json file includes the persona and job to provide context for relevance ranking:

{
  "persona": "Travel Planner",
  "job": "Plan a trip of 4 days for a group of 10 college friends."
}

3.This input.json file was either created using the create_input_json.py tool or provided directly in the input folder (creating it is optional).
4.Running the Docker container processes these input documents and produces output JSON files that identify and rank the most relevant content aligned to planning a 4-day trip for the given persona and group.

This test demonstrated the capability of the system to semantically understand persona-specific tasks and context, and extract targeted information from multiple travel guides effectively.
