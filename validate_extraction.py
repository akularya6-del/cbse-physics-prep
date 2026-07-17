import os
import fitz
import re
import json
import boto3
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed

os.environ['AWS_BEARER_TOKEN_BEDROCK'] = 'bedrock-api-key-YmVkcm9jay5hbWF6b25hd3MuY29tLz9BY3Rpb249Q2FsbFdpdGhCZWFyZXJUb2tlbiZYLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFTSUEyMlhBNVJYR1lYVVJTSkJVJTJGMjAyNjA3MTclMkZ1cy1lYXN0LTElMkZiZWRyb2NrJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA3MTdUMjE1OTU1WiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPUlRb0piM0pwWjJsdVgyVmpFSjclMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkZ3RWFDWFZ6TFdWaGMzUXRNU0pJTUVZQ0lRREs4d0hsbWo1RWx5dFZmYkhheGM4TVZrVlpudTJZVDY5eHdmRHB6cm9hRlFJaEFPRjY3R0FDa0RBcDNiQ3REYkRaJTJCSGlRbzVCUEVaOUkwOHhGMzhXTEZLdDhLcWtEQ0djUUFCb01OelEwTlRjME56Z3lPVEkxSWd5bmMyaW4xbldhWWVjWkZzUXFoZ043b25GdHMxbTRBUDRJeDNnS2pJJTJGZ1Y2MzNLMHNEcVJtaiUyRno3SEFFWUxKM29SanEwQU1xeEUzbnM4b0Fyb3ZhWkpzRUd5NzE2UmNTcTNQRHJKdGtlUFolMkYxTkRPTXIlMkJ2c3NlbFg4ZFNTWnZKV3l5VlBCcTNUQmlHeGdZZ2ZKNGJTQ1FFcVVjT1NXUTUwOXBCUW42M1Zwd2RxTDBCM1NMMmR6JTJCeldDQVYzeGFma1JOU3FFdWk2a1pWOWlNYndnOWFWWlJZVWRmUVpZaEJMdThTTG5WQzU4RUIycDFleVNpdHBkekZvY2ZnRnRTQmY4YXBRdGNXZE1uYzFpWktjdjBWUnJENWJYNlZuU21jUjJEUHJab1NrNzZ2Q0dZYmk5cFVDUGQyZEJYTjJ1OHNyVkN2dFh4a3cwanFsb3NrS1hBQnFyNlg3MG5CTGR5OHU1UWsxYVFnTXFMcHhOMW1KcHRUSiUyRjlvd3RYaTBrcEI3RWszNk1XdXZUJTJCblRnaSUyRktwdG5pVkl0cFVZS0ZkdzhEZ25YbngyaWNpdDlRWGhQTk4yZGp3TWFnOFZSR245bnFZZXZSc0JyRzVBTyUyQm1wWTFERGRrR01xNTJIbUk2VE5lNWZuRFlOcmVFTlZ2ZGhIaE5ZaE5JMW42Mm1PWFJoVWU3cXBJTmUzcGNOV1hRRjliV0hRdDFHd3Z1Q1Fzd21zanEwZ1k2M1FJMW05RmtCM0RGenl3dGR5cFh2cU1tbzRFY3NRJTJGUGwlMkZqUVVMbjBnSVZ2ZmlVOCUyRjI2OXd4U3h0WXVDNjJvS1ZlZ2NlZWhibXQ4V1NseUhwTU5kQ3pKcG1XWVNzM1phME0yOHloeFdDeWNBVSUyRmpzJTJCNW9ubXNZU2Z4SGF2ZHY5RzVLc1JVc2VZU2VHTXJKZDZJcUZtYXpvSzVvZ3ZybkVpaXZPZmxZMmFMWXU4TnhReTZNYklUQnBiNnhUaUpKM01DOTdCM1BJemRoTUxVelZXWGx2NmlLRmVTQ0lNZVlkamNKTVlUWUVJQm1pZG00N000RGJhWDQ3b2V3VXhsb1Q1alN4d1hMN2lIS2pUWjgyUmM4S1FFN2ZnaGUwYVZiTHM0cG1LbEFSN01MNkxOeUFMWSUyQjBEZ3hSMGtLcDRaU09IZEVMMjd6OUNjdm1oMkZKcTAzcGhkQnJNdG9VSURCbjN6JTJCTExYN1pFam9ZTTBDbTFNJTJGRHNuU2toSkhxVEN0akFMJTJCUHpMTzIwbkdSVVJKQmdZOVBtRjFpbHdxakN4VWdadHViamR6Z3QydFYyS29JYUVqSzF4cDRDcm55aVZMZ2Z5RDF3QSUyQnJabUxpcnBUcW16Y0kmWC1BbXotU2lnbmF0dXJlPTFlMmMzMWE2ODU1YWY2NGE0YWU5NTBmZjQxZGViODlhMTM1N2VkZTU2ZGM1NDRhNTIxMjYzMzEzZjE5YTQzMDEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JlZlcnNpb249MQ=='
os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

MODEL_ID = 'mistral.mistral-large-2402-v1:0'
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

def invoke_bedrock(prompt):
    try:
        response = bedrock_client.converse(
            modelId=MODEL_ID,
            messages=[{'role': 'user', 'content': [{'text': prompt}]}],
            system=[{'text': 'Output ONLY valid JSON. No markdown backticks. No preamble.'}]
        )
        return response['output']['message']['content'][0]['text']
    except Exception as e:
        print(f"Bedrock Error: {e}")
        return "{}"

from extract_papers import extract_questions_from_text, classify_question, clean_garbage_text, parse_metadata

test_pdfs = [
    './papers/Physics 4/55_C_1 Physics.pdf',
    './papers/PHYSICS 3/55-1-1_Physics.pdf',
    './papers/Physics 2/55-S-1-Physics.pdf',
    './papers/PHYSICS 5/55_1_2_Physics.pdf',
    './papers/Physics 8/55-4-3 Physics.pdf',
    './papers/Physics/55-5-2.pdf'
]

def is_hindi_page(text):
    hindi_score = text.count('{') + text.count('}') + text.count('$') + text.count('©') + text.count('~')
    return hindi_score > 50

def validate_q(filename, q, valid_pages_text):
    topic_code, topic_name, _, _ = classify_question(q['text'])
    q_page_text = ""
    for pnum, ptext in valid_pages_text:
        if q['text'][:30] in ptext:
            q_page_text = ptext
            break
    if not q_page_text and len(valid_pages_text) > 0:
        q_page_text = valid_pages_text[0][1] # fallback
        
    val_prompt = f"""You are a precise data extraction validator.
Original Page Text:
```
{q_page_text}
```

Extracted Question:
Text: {q['text']}
Marks: {q.get('marks')}
Topic: {topic_name}

Task: Validate this extraction. Is the text complete? Is the mark value correct? Is the topic accurate?
Output ONLY a JSON object:
{{
  "is_perfect": true/false,
  "discrepancy_type": "None" | "False Marks" | "Wrong Topic" | "Incomplete Text" | "Merged Question" | "Other",
  "explanation": "..."
}}"""
    res = invoke_bedrock(val_prompt)
    try:
        j = json.loads(res.strip().replace('```json','').replace('```',''))
        if not j.get('is_perfect', True):
            return f"### Discrepancy in {filename} - Q{q['q_num']}\n- **Type**: {j.get('discrepancy_type')}\n- **Explanation**: {j.get('explanation')}\n- **Extracted Text**: {q['text']}\n"
    except:
        pass
    return None

def check_missed(filename, pnum, ptext, extracted_q_nums):
    miss_prompt = f"""You are a precise data extraction validator.
Original Page Text:
```
{ptext}
```
Extracted Question Numbers for the document: {extracted_q_nums}

Task: Are there any numbered CBSE Physics questions ON THIS SPECIFIC PAGE not in the 'Extracted Question Numbers' list?
Output ONLY a JSON object:
{{
  "missed_questions_exist": true/false,
  "missed_question_numbers": [1, 2],
  "explanation": "..."
}}"""
    res = invoke_bedrock(miss_prompt)
    try:
        j = json.loads(res.strip().replace('```json','').replace('```',''))
        if j.get('missed_questions_exist', False) and len(j.get('missed_question_numbers', [])) > 0:
            return f"### Missed Questions in {filename} on Page {pnum}\n- **Missed**: {j.get('missed_question_numbers')}\n- **Explanation**: {j.get('explanation')}\n"
    except:
        pass
    return None

report_lines = ["# Extraction Validation Report", ""]
total_discrepancies = 0
total_extracted = 0

with ThreadPoolExecutor(max_workers=5) as executor:
    for pdf_path in test_pdfs:
        filename = os.path.basename(pdf_path)
        print(f"Validating {filename}...")
        report_lines.append(f"## File: {filename}")
        
        try:
            doc = fitz.open(pdf_path)
            kept_count = 0
            skipped_count = 0
            
            valid_pages_text = []
            full_text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                raw_text = page.get_text()
                if not raw_text: continue
                
                if is_hindi_page(raw_text):
                    skipped_count += 1
                    continue
                
                kept_count += 1
                valid_pages_text.append((page_num + 1, raw_text))
                full_text += raw_text + "\n"
                
            year, ptype, set_num = parse_metadata(filename)
            extracted = extract_questions_from_text(full_text, filename, year, ptype, set_num)
            total_extracted += len(extracted)
            extracted_q_nums = [q['q_num'] for q in extracted]
            
            # Submit tasks
            futures = []
            for q in extracted:
                futures.append(executor.submit(validate_q, filename, q, valid_pages_text))
            
            for pnum, ptext in valid_pages_text:
                futures.append(executor.submit(check_missed, filename, pnum, ptext, extracted_q_nums))
                
            for future in as_completed(futures):
                res = future.result()
                if res:
                    total_discrepancies += 1
                    report_lines.append(res)
            
            report_lines.append(f"**Pages Kept (English)**: {kept_count} | **Pages Skipped (Hindi)**: {skipped_count}\n")
        except Exception as e:
            report_lines.append(f"Error processing {filename}: {e}\n")

report_lines.insert(2, f"**Total Questions Extracted**: {total_extracted}")
report_lines.insert(3, f"**Total Discrepancies Found**: {total_discrepancies}\n")

with open('validation_report.md', 'w') as f:
    f.write('\n'.join(report_lines))

print(f"Validation complete. Found {total_discrepancies} discrepancies out of {total_extracted} questions.")
