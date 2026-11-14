---
title: Contextual Retrieval
aliases: [Contextual Retrieval, 上下文檢索]
sources: [S5]
summary: 替每個文字塊補上一段上下文，再做 embedding 和 BM25，降低找不到的機率。
---

## 做法

做 embedding 之前，先在每一塊前面加上一段說明這塊在講什麼的上下文，通常是 50～100 個 token，由 Claude 讀整份文件後產生；建立 BM25 索引時也用這個版本。[S5]

例子：ACME 那一塊前面會加上「這段來自 ACME 公司 2023 年第二季的 SEC 財報；上一季營收是 3.14 億美元」。[S5]

## 效果

用「前 20 名沒找到相關段落的比例」衡量：[S5]

- 只加上下文做 embedding：失敗率降低 35%（5.7% → 3.7%）。[S5]
- 再加上 BM25：降低 49%（5.7% → 2.9%）。[S5]
- 再加上 reranking：降低 67%（5.7% → 1.9%）。[S5]

## 成本

產生上下文是一次性成本，每一百萬個文件 token 約 1.02 美元。[S5]

## 相關概念

- [[chunking]]
- [[bm25-hybrid-search]]
- [[reranking]]
