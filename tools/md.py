"""精簡的 Markdown 轉 HTML（沿用 HW9 genai-notes 的 build.py）。"""
import html
import re


def slugify(text):
    s = re.sub(r"[^\w一-鿿-]+", "-", text.strip().lower())
    return s.strip("-") or "section"


def inline(text):
    """處理行內語法：數學式、程式碼、粗體、連結。"""
    keep = []

    def stash(s):
        keep.append(s)
        return f"\x00{len(keep) - 1}\x00"

    text = re.sub(r"`([^`]+)`", lambda m: stash(f"<code>{html.escape(m.group(1))}</code>"), text)
    text = re.sub(r"\$([^$\n]+)\$", lambda m: stash(f'<span class="math">\\({html.escape(m.group(1))}\\)</span>'), text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

    def link(m):
        label, url = m.group(1), m.group(2)
        ext = url.startswith("http")
        if url.endswith(".md") and not ext:
            url = url.rsplit("/", 1)[-1][:-3] + ".html"
        attrs = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a href="{url}"{attrs}>{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"（(p\.[^）]+)）", r'<span class="cite">\1</span>', text)
    return re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], text)


def markdown_to_html(md):
    """支援 AGENTS.md 列出的 Markdown 子集，回傳 (html, 目錄)。"""
    lines = md.splitlines()
    out, toc = [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            lang = line[3:].strip()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{lang}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(buf))}</code></pre>")
            continue
        if line.strip().startswith("$$"):
            buf = [line.strip()[2:]]
            if not (line.strip().endswith("$$") and len(line.strip()) > 2):
                i += 1
                while i < len(lines) and "$$" not in lines[i]:
                    buf.append(lines[i])
                    i += 1
                buf.append(lines[i].replace("$$", "") if i < len(lines) else "")
            else:
                buf = [line.strip()[2:-2]]
            i += 1
            out.append(f'<div class="math-block">\\[{html.escape(" ".join(buf).strip())}\\]</div>')
            continue
        m = re.match(r"^(#{2,4})\s+(.*)$", line)
        if m:
            level, title = len(m.group(1)), m.group(2).strip()
            anchor = slugify(title)
            if level <= 3:
                toc.append((level, title, anchor))
            out.append(f'<h{level} id="{anchor}">{inline(title)}</h{level}>')
            i += 1
            continue
        if line.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip())
                i += 1
            out.append(f'<blockquote class="callout"><p>{inline(" ".join(buf))}</p></blockquote>')
            continue
        if re.match(r"^\s*(-|\d+\.)\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.", line))
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines) and re.match(r"^\s*(-|\d+\.)\s+", lines[i]):
                item = re.sub(r"^\s*(-|\d+\.)\s+", "", lines[i])
                i += 1
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip() \
                        and not re.match(r"^\s*(-|\d+\.)\s+", lines[i]):
                    item += " " + lines[i].strip()
                    i += 1
                items.append(f"<li>{inline(item)}</li>")
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{2,4}\s|```|>|\s*(-|\d+\.)\s+|\s*\$\$)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out), toc
