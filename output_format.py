import sys
from io import StringIO
import textwrap

def format_source_documents(source_docs):
    print("\nSource Documents:")
    print("-" * 80)
    
    for i, doc in enumerate(source_docs, 1):
        # Extract the filename and page number from the metadata
        filename = doc.metadata['source'].split('/')[-1]
        page = doc.metadata['page']
        
        print(f"\n{i}. Source: {filename} (Page {page})")
        print("   " + "-" * 76)
        # Print the first few characters of the content
        content = doc.page_content.replace('\n', '\n    ')
        print(f"    {content}\n")

def print_ww(*args, width: int = 100, **kwargs):
    """Like print(), but wraps output to `width` characters (default 100)"""
    buffer = StringIO()
    try:
        _stdout = sys.stdout
        sys.stdout = buffer
        print(*args, **kwargs)
        output = buffer.getvalue()
    finally:
        sys.stdout = _stdout
    for line in output.splitlines():
        print("\n".join(textwrap.wrap(line, width=width)))