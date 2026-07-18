import re

with open("extract_papers.py", "r") as f:
    text = f.read()

old_clean = """def clean_garbage_text(text):
    import re
    # Remove words with common Kruti Dev symbols mapped to English ASCII
    # Kruti Dev uses characters like H$, {, }, ~, ^, |, etc., extensively
    words = text.split()
    cleaned_words = []
    
    # Exclude words that have specific garbage markers or are non-ascii
    garbage_patterns = [
        r'H\\$', r'\\{', r'\\}', r'~', r'\\^', r'\\u00a1', r'\\u00a9', r'\\u00a2', 
        r'\\u00e1', r'\\u00e2', r'§', r'¢', r'£', r'¤', r'¥', r'¦', r'¨', r'ª', r'«', r'¬', r'\\u00bb', r'\\u00ab',
        r'moB', r'm¡a', r'm\\|', r'eH\\$', r'Zamo', r'hmo', r'm`'
    ]
    
    for word in words:
        is_garbage = False
        for pat in garbage_patterns:
            if re.search(pat, word):
                is_garbage = True
                break
        if not is_garbage:
            cleaned_words.append(word)
            
    return ' '.join(cleaned_words)"""

new_clean = """def clean_garbage_text(text):
    import re
    # Remove footers and common non-question artifacts
    text = re.sub(r'P\\.T\\.O\\.', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\\.?\\d{2,}/[A-Z\\d]+/\\d+', '', text)
    text = re.sub(r'Page\\s+\\d+\\s+of\\s+\\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\\]\\s*\\d+', '', text)
    text = re.sub(r'\\*[A-Z0-9]+\\*', '', text)
    text = re.sub(r'^\\d+\\s*$', '', text, flags=re.MULTILINE) # stray digits on empty lines
    
    # Remove words with common Kruti Dev symbols mapped to English ASCII
    # Kruti Dev uses characters like H$, {, }, ~, ^, |, etc., extensively
    words = text.split()
    cleaned_words = []
    
    # Exclude words that have specific garbage markers or are non-ascii
    garbage_patterns = [
        r'H\\$', r'\\{', r'\\}', r'~', r'\\^', r'\\u00a1', r'\\u00a9', r'\\u00a2', 
        r'\\u00e1', r'\\u00e2', r'§', r'¢', r'£', r'¤', r'¥', r'¦', r'¨', r'ª', r'«', r'¬', r'\\u00bb', r'\\u00ab',
        r'moB', r'm¡a', r'm\\|', r'eH\\$', r'Zamo', r'hmo', r'm`'
    ]
    
    for word in words:
        is_garbage = False
        for pat in garbage_patterns:
            if re.search(pat, word):
                is_garbage = True
                break
        if not is_garbage:
            cleaned_words.append(word)
            
    return ' '.join(cleaned_words)"""

text = text.replace(old_clean, new_clean)

with open("extract_papers.py", "w") as f:
    f.write(text)

