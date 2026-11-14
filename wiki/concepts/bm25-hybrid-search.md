---
title: BM25 與混合搜尋
aliases: [BM25, 混合搜尋, hybrid search, 關鍵字搜尋]
sources: [S5]
summary: 用字詞比對找精確字串，和 embedding 的語意搜尋互補。
---

## BM25 是什麼

BM25 是以字詞比對為主的排名方法，擅長找精確的字詞，建立在 TF-IDF 上。[S5]

## 為什麼要混合

embedding 抓得到意思，但可能漏掉精確比對。例如查「Error code TS-999」時，BM25 能找到完全相同的字串。[S5]

混合做法：同時用 BM25 和 embedding 各找出前幾名，合併去重複後，把前 K 塊加進 prompt。[S5]

## 相關概念

- [[retrieval]]
- [[contextual-retrieval]]
