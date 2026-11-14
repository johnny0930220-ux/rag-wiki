"""C3：檢查簡報 HTML。規則見 AGENTS.md 第 5 節。
需要 Playwright（python -m pip install playwright）才能檢查版面；沒有的話只做內容檢查。"""
import html
import re
from common import CONCEPTS, SOURCES, SLIDES, parse, numbers, norm, report
from check_outline import load_outline

errors = []
outline = load_outline()
page = (SLIDES / "index.html").read_text(encoding="utf-8")
wiki_text = {p.stem: norm(p.read_text(encoding="utf-8")) for p in list(CONCEPTS.glob("*.md")) + list(SOURCES.glob("*.md"))}


def plain(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", h))


sections = re.findall(r'<section[^>]*\bdata-wiki="([^"]*)"[^>]*>(.*?)</section>', page, re.S)
if len(sections) != len(outline):
    errors.append(f"簡報有 {len(sections)} 頁，大綱有 {len(outline)} 頁，要一一對應")
n_nums = 0
for i, (wiki, body) in enumerate(sections, 1):
    ids = wiki.split()
    o = outline[i - 1] if i <= len(outline) else None
    h = re.search(r"<h[12][^>]*>(.*?)</h[12]>", body, re.S)
    title = re.sub(r"\s+", "", plain(h.group(1))) if h else ""
    if o:
        if title != re.sub(r"\s+", "", o["title"]):
            errors.append(f"第 {i} 頁標題「{title}」和大綱「{o['title']}」不同")
        if set(ids) != set(o["wiki"]):
            errors.append(f"第 {i} 頁 data-wiki 是 {ids}，大綱是 {o['wiki']}")
    for w in ids:
        if w not in wiki_text:
            errors.append(f"第 {i} 頁的 data-wiki 有不存在的頁面 {w}")
    pool = " ".join(wiki_text.get(w, "") for w in ids)
    content = re.sub(r'<div class="foot">.*?</div>', " ", body, flags=re.S)  # 頁尾的頁碼不算內容
    for n in numbers(plain(content)):
        n_nums += 1
        if n not in pool:
            errors.append(f"第 {i} 頁的數字 {n} 不在它引用的 wiki 頁（{'、'.join(ids)}）裡")

layout = "未檢查"
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        p = b.new_page(viewport={"width": 1280, "height": 720})
        p.goto((SLIDES / "index.html").as_uri())
        p.wait_for_timeout(300)
        over = p.evaluate("""() => [...document.querySelectorAll('section.slide')].map((s, i) => {
            window.deck.go(i);
            const box = s.querySelector('.inner');
            return box.scrollHeight - box.clientHeight;
        })""")
        for i, d in enumerate(over, 1):
            if d > 2:
                errors.append(f"第 {i} 頁在 1280×720 下內容超出 {d}px")
        m = b.new_page(viewport={"width": 390, "height": 844})
        m.goto((SLIDES / "index.html").as_uri())
        m.wait_for_timeout(300)
        sw = m.evaluate("document.documentElement.scrollWidth")
        if sw > 392:
            errors.append(f"手機寬度 390px 時頁面寬 {sw}px，出現水平捲軸")
        b.close()
    layout = "已檢查"
except ImportError:
    pass

report("C3 檢查簡報", errors, {"頁數": len(sections), "比對數字": n_nums, "版面": layout})
