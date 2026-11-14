---
title: 幻覺（hallucination）
aliases: [幻覺, hallucination]
sources: [S3, S4]
summary: 模型給出聽起來合理、但其實是錯誤的答案。RAG 能降低，但不能消除。
---

## 是什麼

NVIDIA 的文章把「聽起來合理但不正確的答案」稱為幻覺。[S3]

## RAG 和幻覺

- RAG 讓回答建立在可查證的外部事實上，模型比較少依賴參數裡記住的內容，因此降低幻覺和洩漏敏感資料的風險。[S4]
- 但 RAG 只能降低、不能消除幻覺，也不會讓模型自動承認自己不知道。[S4]

## 相關概念

- [[llm-limitations]]
- [[rag-limitations]]
- [[citations-trust]]：附上來源讓人能查證
