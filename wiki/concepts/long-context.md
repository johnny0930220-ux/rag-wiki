---
title: 直接放進 prompt（長上下文與 CAG）
aliases: [CAG, 長上下文, KV-Cache, prompt caching]
sources: [S5, S6]
summary: 資料不多時，不必檢索，直接把全部資料放進 prompt。
---

## 是什麼

模型能讀的上下文越來越長，所以也可以不做檢索，把資料全部放進 prompt。[S6]

課堂上介紹的 CAG，是用 KV-Cache 技術先把資料的鍵值存起來，直接交給 LLM。[S6]

## 什麼時候適合

Anthropic 建議：知識庫小於 20 萬個 token（大約 500 頁）時，可以整個放進 prompt。搭配 prompt caching，延遲可降低超過 2 倍，成本最多降低 90%。[S5]

## 相關概念

- [[rag-limitations]]
- [[llm-wiki]]
