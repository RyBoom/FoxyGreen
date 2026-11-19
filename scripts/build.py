#!/usr/bin/env python3
"""Inline assets/ images into src/index.html as data: URIs -> dist/foxygreen-concept.html.
The spec pitch deploy needs one self-contained HTML file."""
import base64, mimetypes, re
from pathlib import Path
root = Path(__file__).resolve().parent.parent
html = (root / "src/index.html").read_text()
def inline(m):
    path = root / "src" / m.group(2) if (root / "src" / m.group(2)).exists() else root / m.group(2)
    mime = mimetypes.guess_type(path.name)[0]
    return f'{m.group(1)}data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}{m.group(3)}'
html = re.sub(r'((?:src|href)="|url\(")(assets/[^"]+)(")', inline, html)
out = root / "dist/foxygreen-concept.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html)
print(out, f"{len(html)/1024:.0f} KB")
