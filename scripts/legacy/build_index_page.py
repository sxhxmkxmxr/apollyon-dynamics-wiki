import json

# Ensure dependency_corpus_data.js exists and is valid
with open('wiki/assets/dependency_corpus.json') as f:
    corpus = json.load(f)

print(f"Loaded {len(corpus)} dependency corpus episodes.")

