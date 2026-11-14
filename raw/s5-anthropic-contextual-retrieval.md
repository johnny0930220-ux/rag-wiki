---
id: S5
title: Introducing Contextual Retrieval
author: Anthropic Engineering
date: 2024-09-19
url: https://www.anthropic.com/engineering/contextual-retrieval
type: 企業技術文章
fetched: 2026-11-14
---

# 擷取筆記：Anthropic〈Contextual Retrieval〉

> 本檔是讀原文後整理的擷取筆記，不是全文轉貼。數字照原文保留。

## 傳統 RAG 切塊的問題

- 文件被切成小塊（chunk）後，每一塊可能失去上下文，導致檢索失敗。
- 例子（美國證券交易委員會 SEC 的財報）：問題是「ACME 公司 2023 年第二季營收成長多少？」，相關的那一塊只寫「公司營收比上一季成長 3%」，沒寫是哪家公司、哪個時間。

## Contextual Retrieval 的兩個做法

- **Contextual Embeddings**：做 embedding 之前，先在每一塊前面加上一段說明這塊在講什麼的上下文。
- **Contextual BM25**：建立 BM25 索引時也用加了上下文的版本。
- 這段上下文通常是 50～100 個 token，由 Claude 讀整份文件後產生（實驗用 Claude 3 Haiku）。
- 例子：ACME 那一塊前面會加上「這段來自 ACME 公司 2023 年第二季的 SEC 財報；上一季營收是 3.14 億美元」。

## BM25 和混合搜尋

- BM25 是以字詞比對為主的排名方法，擅長找精確的字詞，建立在 TF-IDF 上。
- embedding 抓得到意思，但可能漏掉精確比對。例子：查「Error code TS-999」時，BM25 能找到完全相同的字串。
- 流程：切塊 → 同時建立 TF-IDF 編碼和 embedding → 分別用 BM25 和 embedding 找出前幾名 → 合併去重複 → 把前 K 塊加進 prompt。

## 實驗結果

衡量方式是「前 20 名沒找到相關段落的比例」（1 減 recall@20），以下稱檢索失敗率：

- 只用 Contextual Embeddings：失敗率降低 **35%**（5.7% → 3.7%）。
- Contextual Embeddings 加 Contextual BM25：降低 **49%**（5.7% → 2.9%）。
- 再加上 reranking：降低 **67%**（5.7% → 1.9%）。

## Reranking

- 先檢索出前 150 塊，用 reranker 依問題重新評分，只留前 20 塊交給模型。實驗用 Cohere 的 reranker。
- reranking 會增加一些延遲，所以要在「多排一些、效果較好」和「少排一些、較快較便宜」之間取捨。

## 知識庫很小時可以不用 RAG

- 如果知識庫小於 20 萬個 token（大約 500 頁），可以直接整個放進 prompt，不需要 RAG。
- 搭配 prompt caching，延遲可降低超過 2 倍，成本最多降低 90%。

## 成本

- 產生加上下文的切塊是一次性成本，每一百萬個文件 token 約 1.02 美元（假設每塊 800 token、每份文件 8k token、指令 50 token、每塊上下文 100 token）。
