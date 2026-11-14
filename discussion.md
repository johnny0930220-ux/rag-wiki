# 先討論：範圍與讀者（N2）

> 生成 wiki 和簡報之前，先和 AI 討論，把決定記在這裡。日期：2026-11-14。

## 主題

RAG（Retrieval-Augmented Generation，檢索增強生成）。接續課程第 7 週，也和我在 HW7 做過的 RAG 聊天機器人有關。

## 來源（N1 取得的 6 篇）

- S1：RAG 原始論文（Lewis et al., 2020）
- S2：AWS〈What is RAG?〉
- S3：NVIDIA 部落格〈What Is Retrieval-Augmented Generation〉
- S4：IBM Research〈What is retrieval-augmented generation?〉
- S5：Anthropic〈Contextual Retrieval〉
- S6：課程第 7 週投影片《讓 AI 看懂你的世界》

## 討論結果

- **讀者**：用過 ChatGPT 的一般人。不懂程式、不知道什麼是向量，所以要用生活比喻，少用公式。
- **簡報範圍**（我選了三項）：
  1. 為什麼需要 RAG：LLM 的限制。
  2. RAG 怎麼運作：切塊、embedding、向量資料庫、檢索、放進 prompt。
  3. RAG 的限制與替代做法：仍可能幻覺、資料不多時直接全放進 prompt、和 LLM Wiki 的差別。
- **不放進簡報**：BM25、Contextual Retrieval、reranking 這些進階檢索技巧。wiki 裡仍然保留，因為它們是來源的一部分。
- **長度**：12～15 頁，最後有小測驗。
