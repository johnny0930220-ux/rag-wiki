"""檢查腳本共用的小工具：讀 front matter、寫執行紀錄。"""
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
WIKI = ROOT / "wiki"
CONCEPTS = WIKI / "concepts"
SOURCES = WIKI / "sources"
SLIDES = ROOT / "slides"
LOG = ROOT / "runs" / "log.jsonl"
TPE = timezone(timedelta(hours=8))


def parse(path):
    """回傳 (meta, body)。front matter 只支援 key: value 和 [a, b] 清單。"""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            meta[k.strip()] = v
    return meta, text[end + 5:]


def blocks(body):
    """把內文切成段落或條列項目（略過標題、程式碼區塊、引言框）。"""
    out, in_code = [], False
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not s or s.startswith("#") or s.startswith(">"):
            continue
        out.append(s)
    return out


NUM_RE = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?: ?%|％)?")


def numbers(text):
    """抓出文字裡的數字。略過 10 以下的單獨整數（多半是步驟編號或數量詞）和 [S1] 這類標記。"""
    text = re.sub(r"\[S\d+\]|\[\[[^\]]+\]\]|p\.\d+(?:[–-]\d+)?", " ", text)
    found = []
    for m in NUM_RE.finditer(text):
        n = m.group(0).replace(",", "").replace(" ", "").replace("％", "%")
        if not n.endswith("%") and "." not in n and int(n) <= 10:
            continue
        found.append(n)
    return found


def norm(text):
    return text.replace(",", "").replace("％", "%").replace(" %", "%")


def log(node, ok, errors, stats=None):
    LOG.parent.mkdir(exist_ok=True)
    rec = {"time": datetime.now(TPE).strftime("%Y-%m-%d %H:%M:%S"), "node": node,
           "ok": ok, "errors": errors, "stats": stats or {}}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def report(node, errors, stats):
    log(node, not errors, errors, stats)
    if errors:
        print(f"✗ {node} 沒有通過，{len(errors)} 個問題：")
        for e in errors:
            print("  -", e)
        raise SystemExit(1)
    print(f"✓ {node} 通過：" + "、".join(f"{k} {v}" for k, v in stats.items()))
