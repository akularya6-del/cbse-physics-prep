import re

texts = [
    "55/C/1 Page 9 of 27 P.T.O.",
    "55/S/1 Page 2 of 27",
    ".55/4/3 9 P.T.O.",
    "55/5/2 *R5QPS* *R5QPS55* ] 2",
    "] 23 P.T.O."
]

for t in texts:
    # Match P.T.O.
    cleaned = re.sub(r'P\.T\.O\.', '', t, flags=re.IGNORECASE)
    # Match 55/C/1 or similar paper codes
    cleaned = re.sub(r'\.?\d{2,}/[A-Z\d]+/\d+', '', cleaned)
    # Match Page X of Y or just page numbers
    cleaned = re.sub(r'Page\s+\d+\s+of\s+\d+', '', cleaned, flags=re.IGNORECASE)
    # Match random brackets and numbers at the end
    cleaned = re.sub(r'\]\s*\d+', '', cleaned)
    # Match barcode text
    cleaned = re.sub(r'\*[A-Z0-9]+\*', '', cleaned)
    print("Original:", t)
    print("Cleaned:", cleaned.strip())
    print()

