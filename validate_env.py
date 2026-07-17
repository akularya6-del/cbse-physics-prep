import sys
import os

print(f"Python Version: {sys.version}")

try:
    import fitz
    print("PyMuPDF: OK")
except ImportError:
    print("PyMuPDF: FAILED")

try:
    from sentence_transformers import SentenceTransformer
    print("sentence-transformers: OK")
except ImportError:
    print("sentence-transformers: FAILED")

if os.path.exists("./papers/") and os.path.isdir("./papers/"):
    print("./papers/ directory: OK")
else:
    print("./papers/ directory: FAILED - Please create ./papers/")
