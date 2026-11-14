# RAG Wiki：從知識庫到教學簡報

生成式 AI 課程 HW10。先把 6 篇關於 RAG（檢索增強生成）的資料整理成 LLM Wiki，再只用這個 wiki 做一份給一般人看的教學 HTML 簡報。

- 網站首頁：`index.html`
- 教學簡報：`slides/index.html`
- Wiki 入口：`wiki/index.md`（網頁版 `wiki/index.html`）
- 流程規則：[AGENTS.md](AGENTS.md)
- 執行紀錄：`runs/log.jsonl`（網頁版 `runs.html`）

## 重新跑一次流程

```bash
python3 tools/check_wiki.py      # C1
python3 tools/check_outline.py   # C2
python3 tools/check_slides.py    # C3（版面檢查需要 Playwright）
python3 tools/build_site.py      # N6
```
