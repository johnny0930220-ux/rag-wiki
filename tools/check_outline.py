"""C2：檢查簡報大綱。規則見 AGENTS.md 第 5 節。"""
import re
from common import CONCEPTS, SOURCES, SLIDES, parse, report

errors = []
concepts = {p.stem: parse(p)[0] for p in CONCEPTS.glob("*.md")}
wiki_ids = set(concepts) | {p.stem for p in SOURCES.glob("*.md")}


def load_outline():
    text = (SLIDES / "outline.md").read_text(encoding="utf-8")
    slides = []
    for m in re.finditer(r"^## 第 (\d+) 頁：(.+?)\n(.*?)(?=^## 第 |\Z)", text, re.M | re.S):
        body = m.group(3)
        field = lambda k: re.search(rf"^- {k}:\s*(.*)$", body, re.M)
        wiki = field("wiki")
        new = field("新名詞")
        slides.append({
            "n": int(m.group(1)), "title": m.group(2).strip(), "body": body,
            "wiki": [w.strip() for w in re.split(r"[,、]", wiki.group(1)) if w.strip()] if wiki else [],
            "new": [w.strip() for w in re.split(r"[,、]", new.group(1)) if w.strip() and w.strip() != "無"] if new else None,
            "claims": re.findall(r"^  - (.+)$", body, re.M),
        })
    return slides


if __name__ == "__main__":
    slides = load_outline()
    if not 12 <= len(slides) <= 15:
        errors.append(f"簡報要 12～15 頁，大綱有 {len(slides)} 頁")
    for i, s in enumerate(slides, 1):
        if s["n"] != i:
            errors.append(f"頁碼不連續：第 {i} 個段落寫成第 {s['n']} 頁")
        if not s["wiki"]:
            errors.append(f"第 {s['n']} 頁沒有 wiki: 欄位")
        for w in s["wiki"]:
            if w not in wiki_ids:
                errors.append(f"第 {s['n']} 頁的 wiki 頁 {w} 不存在")
        if s["new"] is None:
            errors.append(f"第 {s['n']} 頁沒有 新名詞: 欄位（沒有就寫「無」）")

    # 名詞要先解釋才能用：用概念頁的 aliases 找出每頁提到的概念
    introduced = set()
    for s in slides:
        new = s["new"] or []
        for cid, m in concepts.items():
            if any(a.lower() == n.lower() for a in m.get("aliases", []) for n in new):
                introduced.add(cid)
        text = s["title"] + "\n" + re.sub(r"^- (wiki|新名詞):.*$", "", s["body"], flags=re.M)
        text = re.sub(r"〔[^〕]+〕", " ", text)
        # 先遮掉已解釋概念的別名（長的先遮），避免「檢索增強生成」被誤判成「檢索」
        for a in sorted((a for c in introduced for a in concepts[c].get("aliases", [])), key=len, reverse=True):
            text = re.sub(re.escape(a), "□", text, flags=re.I)
        for cid, m in concepts.items():
            hit = [a for a in m.get("aliases", []) if re.search(re.escape(a), text, re.I)]
            if hit and cid not in introduced:
                errors.append(f"第 {s['n']} 頁用到「{hit[0]}」，但前面還沒在 新名詞: 解釋過")
                introduced.add(cid)  # 同一個名詞只報一次

    # 第 2 版新增：每個重點句都要標出處，數字要出現在標的 wiki 頁裡（原本只在 C3 檢查）
    from common import WIKI, numbers, norm
    page_text = {p.stem: norm(p.read_text(encoding="utf-8")) for p in WIKI.rglob("*.md")}
    n_claims = 0
    for s in slides:
        if not s["claims"]:
            errors.append(f"第 {s['n']} 頁沒有重點句")
        for c in s["claims"]:
            n_claims += 1
            refs = re.findall(r"〔([^〕]+)〕", c)
            if not refs:
                errors.append(f"第 {s['n']} 頁的重點沒有標出處 →「{c[:24]}…」")
                continue
            for r in refs:
                if r not in s["wiki"]:
                    errors.append(f"第 {s['n']} 頁的重點標了〔{r}〕，但 wiki: 沒有列這一頁")
            pool = " ".join(page_text.get(r, "") for r in refs)
            for n in numbers(re.sub(r"〔[^〕]+〕", " ", c)):
                if n not in pool:
                    errors.append(f"第 {s['n']} 頁的數字 {n} 不在〔{'、'.join(refs)}〕裡")

    # 討論決定的三個範圍都要有
    used = {w for s in slides for w in s["wiki"]}
    for need, label in [("llm-limitations", "為什麼需要 RAG"), ("rag-workflow", "RAG 怎麼運作"),
                        ("rag-limitations", "RAG 的限制與替代做法")]:
        if need not in used:
            errors.append(f"缺少討論範圍「{label}」（沒有任何一頁用到 {need}）")
    if not any("測驗" in s["title"] for s in slides):
        errors.append("最後要有小測驗頁")

    report("C2 檢查大綱", errors, {"頁數": len(slides), "引用 wiki 頁": len(used), "重點句": n_claims})
