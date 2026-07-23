import os
import sys
import boto3
import re
import time

os.environ['AWS_BEARER_TOKEN_BEDROCK'] = os.environ.get('AWS_BEARER_TOKEN_BEDROCK', '')
os.environ['AWS_ACCESS_KEY_ID'] = os.environ.get('AWS_ACCESS_KEY_ID', '')
os.environ['AWS_SECRET_ACCESS_KEY'] = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
os.environ['AWS_DEFAULT_REGION'] = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
MODEL_ID = 'mistral.mistral-large-2402-v1:0'

def invoke_bedrock(prompt):
    try:
        response = bedrock_client.converse(
            modelId=MODEL_ID,
            messages=[{'role': 'user', 'content': [{'text': prompt}]}]
        )
        return response['output']['message']['content'][0]['text']
    except Exception as e:
        print(f"Bedrock Error: {e}", flush=True)
        return ""

print("Reading multi-year practice sheet...", flush=True)
with open('docs/multi_year_practice_sheet.md', 'r') as f:
    text = f.read()

parts = re.split(r'(## Chapter \d+.*?\n)', text)
header = parts[0]
chapters = []
for i in range(1, len(parts), 2):
    chapters.append(parts[i] + parts[i+1])

print(f"Found {len(chapters)} chapters to process.", flush=True)
verified_chapters = []

for idx, chapter_text in enumerate(chapters):
    print(f"Validating chapter {idx+1}/{len(chapters)}...", flush=True)
    prompt = f"""You are a master physics professor and an AI reviewer. 
The following text is a section from a CBSE Class 12 Physics practice sheet. It was automatically generated from OCR-extracted past papers.
Some questions might contain OCR noise (e.g., garbled characters like "5 V [ - (emf ) 2 3 \\ 9 , 9L", missing subscripts, or random Hindi characters mistaken as symbols).

Your task:
1. Proofread and CORRECT any obvious OCR errors to make the physics questions readable and technically accurate.
2. If a question is absolute nonsense or unrecoverable garbage, replace the question text with "[This question was flagged by AI as unrecoverable OCR garbage]".
3. PRESERVE the exact markdown formatting, question numbering (e.g. **Q1. [3.0M]**), and the repetition badges (e.g. 🔥 **Extremely Important...**).
4. Do NOT change the core meaning or solve the questions. Just clean the text.

Here is the chapter text to clean:
{chapter_text}

Output ONLY the cleaned markdown text for this chapter, nothing else. No preamble, no markdown backticks at the start/end unless it's part of the text."""
    
    clean_text = invoke_bedrock(prompt)
    if clean_text:
        if clean_text.startswith("```markdown"):
            clean_text = clean_text[len("```markdown"):].strip()
        elif clean_text.startswith("```"):
            clean_text = clean_text[len("```"):].strip()
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3].strip()
            
        verified_chapters.append(clean_text)
        print(f"Chapter {idx+1} successfully validated.", flush=True)
    else:
        print(f"Failed to process chapter {idx+1}, keeping original.", flush=True)
        verified_chapters.append(chapter_text.strip())
    
    time.sleep(2)

final_markdown = "# 🧠 AI-Verified CBSE Physics Practice Sheet\n\n"
final_markdown += "This sheet has been ranked by **Multi-Year Repetition** to highlight fundamental concepts, and then **Verified by AI (Mistral Large)** to clean up OCR errors and ensure the questions are accurate and readable.\n\n"
final_markdown += "---\n\n"
final_markdown += "\n\n---\n\n".join(verified_chapters)

with open('docs/ai_verified_practice_sheet.md', 'w') as f:
    f.write(final_markdown)

print("Created docs/ai_verified_practice_sheet.md successfully!", flush=True)
