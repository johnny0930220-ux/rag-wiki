"""N6：把 raw、wiki 和執行紀錄轉成可以瀏覽的網頁。用法：python3 tools/build_site.py"""
import html
import json
import os
import re
from collections import Counter
from common import ROOT, RAW, WIKI, CONCEPTS, SOURCES, LOG, parse
from md import markdown_to_html

SITE = "RAG Wiki"

# 每個頁面 id 對應的檔案（相對於專案根目錄）
paths = {}
for p in CONCEPTS.glob("*.md"):
    paths[p.stem] = f"wiki/concepts/{p.stem}.html"
for p in SOURCES.glob("*.md"):
    paths[p.stem] = f"wiki/sources/{p.stem}.html"
titles = {pid: parse(ROOT / (path[:-5] + ".md"))[0].get("title", pid) for pid, path in paths.items()}
raw_by_id = {}
for p in RAW.glob("s*.md"):
    m, _ = parse(p)
    raw_by_id[m["id"]] = f"raw/{p.stem}.html"


def rel(target, here):
    return os.path.relpath(target, os.path.dirname(here) or ".").replace(os.sep, "/")


def prepare(md_text, here):
    """把 [[頁面]] 和 [S2] 換成一般連結。"""
    md_text = re.sub(r"\[\[([^\]]+)\]\]",
                     lambda m: f"[{titles.get(m.group(1), m.group(1))}]({rel(paths.get(m.group(1), ''), here)})", md_text)
    md_text = re.sub(r"\[(S\d+)\](?!\()",
                     lambda m: f"[{m.group(1)}]({rel(paths.get('s' + m.group(1)[1:], ''), here)})", md_text)
    return md_text


CSS = """
:root{--bg:#fbfaf7;--paper:#fff;--ink:#22252a;--muted:#61656d;--line:#e2ded5;--accent:#0f6e6a;--soft:#e2f0ee;--warm:#c2410c;--warm-soft:#fbe7da;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15171a;--paper:#1c1f23;--ink:#e7e5e0;--muted:#a2a5ab;--line:#2d3137;--accent:#5ec4bc;--soft:#1d3533;--warm:#f0a35b;--warm-soft:#3a2a1d;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#15171a;--paper:#1c1f23;--ink:#e7e5e0;--muted:#a2a5ab;--line:#2d3137;--accent:#5ec4bc;--soft:#1d3533;--warm:#f0a35b;--warm-soft:#3a2a1d;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.8 "Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif}
a{color:var(--accent);text-underline-offset:3px}
header.top{border-bottom:1px solid var(--line);background:var(--paper)}
.bar{max-width:880px;margin:0 auto;padding:12px 16px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}
.bar .brand{font-weight:700;color:var(--ink);text-decoration:none;margin-right:auto}
.bar a{text-decoration:none}
main{max-width:880px;margin:0 auto;padding:28px 16px 80px}
h1{font-size:32px;line-height:1.3;margin:4px 0 10px}h2{font-size:23px;margin:36px 0 10px}h3{font-size:19px;margin:24px 0 6px}
.eyebrow{font-size:13px;color:var(--accent);font-weight:700;letter-spacing:.06em;margin:0}
.summary{color:var(--muted);font-size:18px;margin:0 0 12px}
.meta{font-size:14px;color:var(--muted);border-left:3px solid var(--line);padding-left:12px;margin:12px 0 24px}
code{font-family:Consolas,monospace;background:var(--soft);padding:1px 5px;border-radius:5px;font-size:.9em}
pre{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:12px 14px;overflow-x:auto;line-height:1.6}pre code{background:none;padding:0}
blockquote{margin:16px 0;padding:10px 16px;background:var(--soft);border-left:4px solid var(--accent);border-radius:0 8px 8px 0}blockquote p{margin:0}
.cards{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
.card{display:block;height:100%;padding:16px 18px;background:var(--paper);border:1px solid var(--line);border-radius:12px;color:var(--ink);text-decoration:none;line-height:1.6}
.card:hover{border-color:var(--accent)}.card strong{display:block;font-size:18px;margin-bottom:4px}.card span{color:var(--muted);font-size:15px}
.flow{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0 4px;padding:0;list-style:none}
.flow li{margin:0;padding:6px 12px;border-radius:999px;background:var(--paper);border:1px solid var(--line);font-size:14px}
.flow li.c{background:var(--soft);border-color:var(--accent);color:var(--accent)}.flow li.r{background:var(--warm-soft);border-color:var(--warm);color:var(--warm)}
.flow .to{border:0;background:none;padding:0;color:var(--muted)}
.run{list-style:none;padding:0;margin:0;border-left:2px solid var(--line)}
.run>li{position:relative;padding:8px 0 12px 22px;margin:0}
.run>li::before{content:"";position:absolute;left:-7px;top:16px;width:12px;height:12px;border-radius:50%;background:var(--accent)}
.run>li.fail::before{background:var(--warm)}.run>li.gen::before{background:var(--line)}
.run .t{font-size:13px;color:var(--muted);font-family:Consolas,monospace}.run .n{font-weight:700}
.run .ok{color:var(--accent);font-weight:700}.run .bad{color:var(--warm);font-weight:700}
.run ul{margin:4px 0 0;padding-left:18px;font-size:15px}.run .d{font-size:15px;color:var(--muted)}
.stat{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0 20px}.stat span{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:8px 14px;font-size:15px}
.stat b{font-size:20px;margin-right:4px}
footer{max-width:880px;margin:0 auto;padding:0 16px 40px;font-size:13px;color:var(--muted)}
@media (max-width:600px){body{font-size:16px}h1{font-size:26px}}
"""


def page(here, title, content, desc=""):
    nav = [("index.html", "首頁"), ("wiki/index.html", "Wiki"), ("slides/index.html", "教學簡報"), ("runs.html", "流程與檢查紀錄")]
    links = "".join(f'<a href="{rel(h, here)}">{t}</a>' for h, t in nav[1:])
    return f"""<!doctype html>
<html lang="zh-Hant-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc or title)}">
<style>{CSS}</style></head><body>
<header class="top"><div class="bar"><a class="brand" href="{rel('index.html', here)}">{SITE}</a>{links}</div></header>
<main>{content}</main>
<footer>RAG 主題的 LLM Wiki。raw/ 只放改寫後的擷取筆記，原文請見各來源網址。</footer>
</body></html>
"""


def write(here, title, content, desc=""):
    out = ROOT / here
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(here, title, content, desc), encoding="utf-8")


def md_page(src, here, kind):
    m, body = parse(src)
    body_html = markdown_to_html(prepare(body, here))[0]
    head = f'<p class="eyebrow">{kind}</p><h1>{html.escape(m.get("title", src.stem))}</h1>'
    if m.get("summary"):
        head += f'<p class="summary">{html.escape(m["summary"])}</p>'
    if m.get("sources"):
        srcs = "、".join(f'<a href="{rel(paths["s" + s[1:]], here)}">{s}</a>' for s in m["sources"])
        head += f'<p class="meta">來源：{srcs}</p>'
    if m.get("url"):
        u = m["url"]
        link = f'<a href="{u}" target="_blank" rel="noopener">{html.escape(u)}</a>' if u.startswith("http") else html.escape(u)
        head += f'<p class="meta">{html.escape(m.get("author", ""))}｜{html.escape(m.get("date", ""))}｜{link}<br>擷取日期：{m.get("fetched", "")}</p>'
    if m.get("source"):
        head += f'<p class="meta">原始擷取筆記：<a href="{rel(raw_by_id[m["source"]], here)}">{m["source"]}</a></p>'
    write(here, m.get("title", src.stem), head + body_html, m.get("summary", ""))


for p in CONCEPTS.glob("*.md"):
    md_page(p, f"wiki/concepts/{p.stem}.html", "概念頁")
for p in SOURCES.glob("*.md"):
    md_page(p, f"wiki/sources/{p.stem}.html", "來源頁")
for p in RAW.glob("s*.md"):
    md_page(p, f"raw/{p.stem}.html", "raw 擷取筆記")
for name, title in [("index", "Wiki 索引"), ("log", "Ingest 紀錄")]:
    body = (WIKI / f"{name}.md").read_text(encoding="utf-8")
    write(f"wiki/{name}.html", title, markdown_to_html(prepare(body, f"wiki/{name}.html"))[0])

# 執行紀錄
recs = [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
checks = [r for r in recs if r["node"].startswith("C")]
fails = Counter(r["node"] for r in checks if not r["ok"])
items = []
for r in recs:
    is_check = r["node"].startswith("C")
    cls = ("fail" if not r["ok"] else "") if is_check else "gen"
    status = (' <span class="ok">通過</span>' if r["ok"] else f' <span class="bad">沒通過（{len(r["errors"])} 個問題）</span>') if is_check else ""
    detail = ""
    if r["errors"]:
        detail = "<ul>" + "".join(f"<li>{html.escape(e)}</li>" for e in r["errors"]) + "</ul>"
    elif r["stats"]:
        detail = '<div class="d">' + html.escape("、".join(f"{k}：{v}" if k != "說明" else v for k, v in r["stats"].items())) + "</div>"
    items.append(f'<li class="{cls}"><span class="t">{r["time"]}</span> <span class="n">{html.escape(r["node"])}</span>{status}{detail}</li>')
stat = (f'<div class="stat"><span><b>{len(recs)}</b>筆紀錄</span><span><b>{len(checks)}</b>次檢查</span>'
        f'<span><b>{sum(fails.values())}</b>次沒通過</span>'
        + "".join(f'<span>{html.escape(k)}：沒通過 <b>{v}</b> 次</span>' for k, v in sorted(fails.items())) + "</div>")
flow = ('<ul class="flow"><li>N1 取得資料</li><li class="to">→</li><li>N2 先討論</li><li class="to">→</li><li>N3 Ingest（每篇一輪）</li>'
        '<li class="to">→</li><li class="c">C1 檢查 wiki</li><li class="to">→</li><li>N4 整理大綱</li><li class="to">→</li>'
        '<li class="c">C2 檢查大綱（含出處、數字）</li><li class="to">→</li><li>N5 產生簡報</li><li class="to">→</li>'
        '<li class="c">C3 檢查簡報</li><li class="to">→</li><li class="r">R 對照審查</li><li class="to">→</li><li>N6 發布</li></ul>')
write("runs.html", "流程與檢查紀錄",
      '<p class="eyebrow">Loop / Graph</p><h1>流程與檢查紀錄</h1>'
      '<p class="summary">這一頁由 runs/log.jsonl 自動產生，依時間列出每個節點的執行結果。灰點是生成節點，綠點是通過的檢查，橘點是沒通過的檢查。</p>'
      '<h2>目前的流程（第 2 版）</h2>' + flow +
      '<p class="d">規則全文見 <a href="https://github.com/johnny0930220-ux/rag-wiki/blob/main/AGENTS.md">AGENTS.md</a>。</p>'
      '<h2>統計</h2>' + stat + '<h2>完整紀錄</h2><ol class="run">' + "".join(items) + "</ol>")

# 首頁
n_c = len(list(CONCEPTS.glob("*.md")))
n_s = len(list(SOURCES.glob("*.md")))
home = f"""<p class="eyebrow">生成式 AI 課程 HW10</p><h1>RAG Wiki：從知識庫到教學簡報</h1>
<p class="summary">先把 {n_s} 篇關於 RAG（檢索增強生成）的資料整理成 LLM Wiki，再只用這個 wiki 做一份給一般人看的教學簡報。</p>
<ul class="cards">
<li><a class="card" href="slides/index.html"><strong>教學簡報</strong><span>15 頁，給用過 ChatGPT 的人。用方向鍵或下方按鈕翻頁。</span></a></li>
<li><a class="card" href="wiki/index.html"><strong>LLM Wiki</strong><span>{n_c} 個概念頁、{n_s} 個來源頁，每段都標了來源。</span></a></li>
<li><a class="card" href="runs.html"><strong>流程與檢查紀錄</strong><span>每個節點的執行結果，包含沒通過的檢查和修正。</span></a></li>
</ul>
<h2>流程</h2>{flow}
<h2>來源</h2><ul>""" + "".join(
    f'<li><a href="{raw_by_id[parse(p)[0]["id"]]}">{parse(p)[0]["id"]}</a>　{html.escape(parse(p)[0]["title"])}</li>'
    for p in sorted(RAW.glob("s*.md"))) + "</ul>"
write("index.html", SITE, home, "RAG 主題的 LLM Wiki 與教學簡報")
print(f"✓ N6 發布：首頁、wiki {n_c + n_s + 2} 頁、raw {len(raw_by_id)} 頁、流程紀錄 1 頁")
