# AGENTS.md：RAG 主題 LLM Wiki 與教學簡報

> 給 AI 的工作手冊。開始前先讀完整份文件，照第 3 節的流程（graph）一步一步做。
> 每個檢查節點沒有通過，就不能往下走。

## 1. 專案目的

- 依 Karpathy 的 LLM Wiki 做法，建立一個「RAG（檢索增強生成）」主題的知識庫。
- 再**只用這個 wiki 當知識來源**，做一份給一般人看的教學 HTML 簡報。
- 讀者：用過 ChatGPT、但不懂程式和向量的一般人（見 `discussion.md`）。

## 2. 資料夾結構

```text
rag-wiki/
├── AGENTS.md            這份手冊
├── discussion.md        先討論的紀錄：讀者、範圍、長度（N2 的產出）
├── raw/                 N1：每篇來源一個擷取筆記（s1-xxx.md），只放改寫後的重點
├── wiki/
│   ├── index.md         wiki 入口：列出所有頁面和一句話摘要
│   ├── log.md           ingest 紀錄：每次處理哪篇來源、新增或修改了哪些頁
│   ├── sources/         每篇來源一頁摘要（s1.md…）
│   └── concepts/        概念頁（rag.md、embedding.md…）
├── slides/
│   ├── outline.md       N4：簡報大綱，每頁註明用到哪些 wiki 頁
│   └── index.html       N5：教學簡報（單一 HTML 檔）
├── tools/               檢查和建置腳本（只用 Python 標準庫，簡報檢查另用 Playwright）
└── runs/log.jsonl       每次執行檢查的紀錄（自動寫入）
```

## 3. 流程（graph）

```text
N1 取得資料 → N2 先討論 → N3 Ingest（每篇來源一輪）→ C1 檢查 wiki
   → N4 查詢 wiki、整理大綱 → C2 檢查大綱（含出處和數字）
   → N5 產生簡報 → C3 檢查簡報 → R 對照審查 → N6 發布
```

失敗時回到哪裡：C1 → N3；C2 → N4（wiki 缺內容就回 N3）；C3 → N5；R → N5（大綱本身有錯就回 N4）。

- **N1 取得資料**：每篇來源寫成 `raw/sN-短名.md`，front matter 要有 id、title、author、date、url、type、fetched。只寫改寫後的重點，英文原句最多引用一句。
- **N2 先討論**：生成前先和我討論讀者、範圍、長度，結果寫進 `discussion.md`。沒有討論紀錄不能進 N3。
- **N3 Ingest**：一次處理一篇來源，這是會重複的 loop：
  1. 寫 `wiki/sources/sN.md`：這篇來源的重點摘要。
  2. 新增或更新相關的概念頁。同一個概念只能有一頁，已經有就補充，不要另開新頁。
  3. 更新 `wiki/index.md` 和 `wiki/log.md`。
- **C1 檢查 wiki**：`python3 tools/check_wiki.py`。沒過就回 N3 修正。
- **N4 整理大綱**：只讀 wiki（不讀 raw），依 `discussion.md` 的範圍寫 `slides/outline.md`。**每一個重點句後面都要標〔wiki 頁〕**，簡報上會出現的句子都要先出現在大綱裡。
- **C2 檢查大綱**：`python3 tools/check_outline.py`。檢查頁數、名詞有沒有先解釋、每個重點句的〔出處〕、數字是否在出處頁裡。沒過就回 N4；如果是 wiki 缺內容，回 N3 補。
- **N5 產生簡報**：照大綱寫 `slides/index.html`。
- **C3 檢查簡報**：`python3 tools/check_slides.py`。檢查和大綱一一對應、數字、1280×720 是否超出、手機是否有水平捲軸。沒過就回 N5。
- **R 對照審查**：AI 逐頁把簡報和大綱、wiki 對照，找出程式檢查抓不到的問題：大綱沒有的句子、超出 wiki 的說法、把不同來源的例子混在一起。結果用 `tools/log_node.py` 記錄。
- **N6 發布**：`python3 tools/build_site.py` 產生 wiki 的瀏覽網頁。

## 4. Wiki 頁面格式

### 概念頁 `wiki/concepts/英文短名.md`

```markdown
---
title: 向量資料庫
aliases: [向量資料庫, vector database]
sources: [S2, S3]
summary: 存放大量向量、能快速找出最相近向量的資料庫。
---

## 是什麼
內文，每段結尾標來源 [S2]。

## 相關概念
- [[embedding]]：…
```

- `aliases`：這個概念在文章裡可能出現的寫法，C2 會用它檢查簡報有沒有先解釋名詞。**不要放太常見的詞**（例如「來源」「資料」），否則每一頁都會被誤判。
- **每一段內文、每一個條列，都要至少標一個來源**，格式 `[S2]`，可以多個 `[S2][S4]`。
- **數字一定要出現在標註的來源裡**（例如 67%、20 萬個 token），C1 會逐一比對。
- 頁面之間用 `[[頁面短名]]` 連結，每個概念頁至少連到一個其他概念頁。

### 來源頁 `wiki/sources/sN.md`

front matter 有 `title`、`source: SN`、`summary`，內文寫這篇的重點，以及它被用在哪些概念頁。

## 5. 簡報規則

- 大綱每頁格式：

```markdown
## 第 3 頁：RAG 是什麼
- wiki: rag, open-book-analogy
- 新名詞: RAG
- 重點:
  - 一個重點一句，後面標出處。〔rag〕
```

- 每一頁只能用 `wiki:` 列出的 wiki 頁內容；數字也只能用那些頁面裡有的。
- 讀者不懂技術，所以**名詞第一次出現的那頁，要在 `新名詞:` 列出並解釋**。
- 簡報 HTML 裡每頁是一個 `<section data-wiki="rag open-book-analogy">`，和大綱一一對應。
- 版面 1280×720，文字不能超出畫面；手機也要能看。

## 6. 不能做的事

- 不能用 wiki 以外的知識寫簡報。wiki 沒有的，就回 N3 從來源補進 wiki。
- 不能編造數字、日期、人名或引文。
- 不能把來源全文貼進 `raw/`，只放改寫後的重點。
- 不能放 API key 或個資。

## 7. 更新紀錄

- 2026-11-14：第一版流程（v1）。
- 2026-11-14：第二版流程（v2），依第一次實際執行的結果修改：
  - 數字檢查從 C3 往前移到 C2：大綱每個重點句都要標〔wiki 頁〕，數字在大綱階段就比對。
  - 新增 R 對照審查：第一次執行時，C3 全部通過後人工審查仍找到 3 個「超出 wiki」的句子，程式檢查抓不到。
  - aliases 不能放太常見的詞（「來源」造成誤判）。
