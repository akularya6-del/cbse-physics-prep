import json
import re

with open("physics_questions_database.json") as f:
    db = json.load(f)

questions = db["questions"]

def get_words(text):
    return set(re.findall(r'\w+', text.lower()))

seen_texts_words = []
unique_questions = []

duplicates = 0
for q in questions:
    new_words = get_words(q["questionText"])
    if len(new_words) < 5:
        unique_questions.append(q)
        continue
        
    is_dup = False
    for seen_words in seen_texts_words:
        intersection = new_words.intersection(seen_words)
        union = new_words.union(seen_words)
        if len(union) == 0: continue
        jaccard = len(intersection) / len(union)
        if jaccard > 0.85:
            is_dup = True
            break
            
    if is_dup:
        duplicates += 1
    else:
        seen_texts_words.append(new_words)
        unique_questions.append(q)

print(f"Total questions: {len(questions)}, Fuzzy Duplicates: {duplicates}, Unique: {len(unique_questions)}")
