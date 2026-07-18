import re

def clean_garbage_text(text):
    # Remove footers and common non-question artifacts
    text = re.sub(r'P\.T\.O\.', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\.?\d{2,}/[A-Z\d]+/\d+', '', text)
    text = re.sub(r'Page\s+\d+\s+of\s+\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\]\s*\d+', '', text)
    text = re.sub(r'\*[A-Z0-9]+\*', '', text)
    
    words = text.split()
    cleaned_words = []
    garbage_patterns = [
        r'H\$', r'\{', r'\}', r'~', r'\^', r'\u00a1', r'\u00a9', r'\u00a2', 
        r'\u00e1', r'\u00e2', r'§', r'¢', r'£', r'¤', r'¥', r'¦', r'¨', r'ª', r'«', r'¬', r'\u00bb', r'\u00ab',
        r'moB', r'm¡a', r'm\|', r'eH\$', r'Zamo', r'hmo', r'm`'
    ]
    
    for word in words:
        is_garbage = False
        for pat in garbage_patterns:
            if re.search(pat, word):
                is_garbage = True
                break
        if not is_garbage:
            cleaned_words.append(word)
            
    return ' '.join(cleaned_words)
