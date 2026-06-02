import json
import yaml
from pypdf import PdfReader
import pandas as pd
from llama_index.core.node_parser import SentenceSplitter

def read_file(filepath):
    if filepath.endswith(".pdf"):
        reader = PdfReader(filepath)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif filepath.endswith(".xlsx") or filepath.endswith(".xls"):
        df = pd.read_excel(filepath)
        return df.to_string(index=False)
    else:
        with open(filepath, "r") as f:
            return f.read()

# Load whitelist
with open("config/whitelist.yaml") as f:
    whitelist = yaml.safe_load(f)

chunks = []

for filepath in whitelist["allowed_files"]:
    tags = whitelist["tags"].get(filepath, {})

    # Read the file
    try:
        text = read_file(filepath)
    except Exception as e:
        print(f"Could not read {filepath}: {e}")
        continue

    # Chunk the text
    splitter = SentenceSplitter(chunk_size=512)
    text_chunks = splitter.split_text(text)

    for i, chunk in enumerate(text_chunks):
        chunks.append({
            "id": f"{filepath}_chunk_{i}",
            "source": filepath,
            "content": chunk,
            "embedding": None,        # placeholder for when you add AI later
            "role_required": tags.get("role_required", "admin"),
            "category": tags.get("category", "general")
        })

    print(f"Ingested {len(text_chunks)} chunks from {filepath}")

# Write to JSON
with open("transformed-data/chunks.json", "w") as f:
    json.dump(chunks, f, indent=2)

print(f"\nDone. Total chunks saved: {len(chunks)}")