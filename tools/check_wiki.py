"""C1：檢查 wiki。規則見 AGENTS.md 第 4 節。"""
import re
from common import RAW, CONCEPTS, SOURCES, WIKI, parse, blocks, numbers, norm, report

errors = []
raw = {}
for p in sorted(RAW.glob("s*.md")):
    m, body = parse(p)
    for k in ["id", "title", "author", "date", "url", "type", "fetched"]:
        if not m.get(k):
            errors.append(f"raw/{p.name}：front matter 缺少 {k}")
    raw[m.get("id")] = norm(body)

src_pages = {}
for p in sorted(SOURCES.glob("*.md")):
    m, body = parse(p)
    sid = m.get("source")
    if sid not in raw:
        errors.append(f"sources/{p.name}：source: {sid} 在 raw/ 找不到")
    src_pages[p.stem] = (m, body)
for sid in raw:
    if not any(m.get("source") == sid for m, _ in src_pages.values()):
        errors.append(f"{sid} 還沒有 ingest：wiki/sources/ 沒有它的來源頁")
if len(src_pages) < 5:
    errors.append(f"至少要 ingest 5 篇資料，目前只有 {len(src_pages)} 篇")

concepts = {p.stem: parse(p) for p in sorted(CONCEPTS.glob("*.md"))}
all_ids = set(concepts) | set(src_pages)
n_claims = n_nums = 0
for cid, (m, body) in concepts.items():
    for k in ["title", "aliases", "sources", "summary"]:
        if not m.get(k):
            errors.append(f"concepts/{cid}.md：front matter 缺少 {k}")
    declared = set(m.get("sources") or [])
    for b in blocks(body):
        cites = re.findall(r"\[(S\d+)\]", b)
        if b.startswith("- [[") and not cites:
            continue  # 「相關概念」清單只放連結，不需要來源
        n_claims += 1
        if not cites:
            errors.append(f"concepts/{cid}.md：這段沒有標來源 →「{b[:30]}…」")
            continue
        for c in cites:
            if c not in raw:
                errors.append(f"concepts/{cid}.md：引用了不存在的來源 {c}")
            elif c not in declared:
                errors.append(f"concepts/{cid}.md：內文引用 {c}，但 front matter 的 sources 沒有列")
        for n in numbers(b):
            n_nums += 1
            if not any(n in raw.get(c, "") for c in cites):
                errors.append(f"concepts/{cid}.md：數字 {n} 在標註的來源 {'、'.join(cites)} 裡找不到")
    links = set(re.findall(r"\[\[([^\]]+)\]\]", body))
    for l in links:
        if l not in all_ids:
            errors.append(f"concepts/{cid}.md：連結 [[{l}]] 找不到頁面")
    if not (links & set(concepts)):
        errors.append(f"concepts/{cid}.md：至少要連到一個其他概念頁")

for sid, (m, body) in src_pages.items():
    for l in set(re.findall(r"\[\[([^\]]+)\]\]", body)):
        if l not in all_ids:
            errors.append(f"sources/{sid}.md：連結 [[{l}]] 找不到頁面")

index = (WIKI / "index.md").read_text(encoding="utf-8") if (WIKI / "index.md").exists() else ""
log_md = (WIKI / "log.md").read_text(encoding="utf-8") if (WIKI / "log.md").exists() else ""
for pid in all_ids:
    if f"[[{pid}]]" not in index:
        errors.append(f"index.md 沒有列出 [[{pid}]]")
for sid in raw:
    if sid not in log_md:
        errors.append(f"log.md 沒有 {sid} 的 ingest 紀錄")

report("C1 檢查 wiki", errors, {"來源": len(src_pages), "概念頁": len(concepts),
                               "檢查段落": n_claims, "比對數字": n_nums})
