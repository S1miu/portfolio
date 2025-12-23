import sys
from pathlib import Path
import re
import html


def fix_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")

    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Stream through lines and capture the encoded inner HTML block only
    lines = text.split("\n")
    capturing = False
    buf: list[str] = []

    for ln in lines:
        if not capturing and "&lt;!DOCTYPE html" in ln.lower():
            capturing = True

        if capturing:
            # Strip Cocoa wrappers in both literal and encoded forms
            ln = re.sub(r'^\s*<p class="p[12]">', '', ln)
            ln = ln.replace('</p>', '')
            ln = ln.replace('&lt;p class="p1"&gt;', '')
            ln = ln.replace('&lt;p class="p2"&gt;', '')
            ln = ln.replace('&lt;/p&gt;', '')
            ln = re.sub(r'<span class="Apple-converted-space">([\s\S]*?)</span>', r'\1', ln)
            ln = ln.replace('<br>', '').replace('<br/>', '').replace('<br />', '')
            ln = ln.replace('&lt;br&gt;', '').replace('&lt;br/&gt;', '').replace('&lt;br /&gt;', '')

            buf.append(ln)

            if '&lt;/html&gt;' in ln:
                break

    if not buf:
        # Mixed/partially-decoded state: strip wrappers globally and unescape once
        tmp_lines = []
        for ln in lines:
            ln = re.sub(r'^\s*<p class="p[12]">', '', ln)
            ln = ln.replace('</p>', '')
            ln = ln.replace('<span class="Apple-converted-space">', '').replace('</span>', '')
            ln = ln.replace('<br>', '').replace('<br/>', '').replace('<br />', '')
            tmp_lines.append(ln)
        segment = "\n".join(tmp_lines)
        decoded = html.unescape(segment)
    else:
        segment = "\n".join(buf)
        decoded = html.unescape(segment)

    # Ensure we only keep the real HTML document
    s2 = decoded.lower().find('<!doctype html')
    e2 = decoded.lower().rfind('</html>')
    if s2 != -1 and e2 != -1:
        decoded = decoded[s2 : e2 + len('</html>')]

    path.write_text(decoded.strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("1.html")
    target = (Path(__file__).resolve().parent.parent / target).resolve()
    fix_file(target)
    print(f"Fixed: {target}")
