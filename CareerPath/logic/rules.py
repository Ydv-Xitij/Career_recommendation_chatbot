import pandas as pd
import os

file_path = "data/careers.csv"

if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
    raise FileNotFoundError(f"{file_path} is missing or empty. Please add data.")

df = pd.read_csv(file_path)

SYNONYMS = {
    "ml": ["machine learning", "ai"],
    "excel": ["spreadsheet", "ms excel"],
    "js": ["javascript"],
    "python": ["py"]
}

def normalize_terms(terms):
    normalized = []
    for term in terms:
        term = term.strip().lower()
        if term:
            normalized.append(term)
            for key, syns in SYNONYMS.items():
                if term == key or term in syns:
                    normalized.extend([key] + syns)
    return list(set(normalized))

def recommend(profile):
    skills = normalize_terms(profile.get("skills", "").split(","))
    interests = normalize_terms(profile.get("interests", "").split(","))
    style = profile.get("style", "").lower()

    scores = []
    for _, row in df.iterrows():
        score = 0
        matched = []  # to store matching terms for explanation

        for s in skills:
           if s.strip() and s.strip() in row["skills"].lower():
                score += 3
                matched.append(s.strip())

        for i in interests:
            if i.strip() and i.strip() in row["interests"].lower():
                score += 2
                matched.append(i.strip())

        if style and style in row["style"].lower():
            score += 1
            matched.append(style)

        explanation = ", ".join(matched[:2]) if matched else "General match"
        scores.append((row["role"], row["description"], score, explanation, row.get("roadmap", "No roadmap available")))


    scores = sorted(scores, key=lambda x: x[2], reverse=True)[:5]
    return scores



