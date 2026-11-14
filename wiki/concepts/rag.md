---
title: RAG（檢索增強生成）
aliases: [RAG, 檢索增強生成, Retrieval-Augmented Generation]
sources: [S1, S2, S3, S4, S6]
summary: 讓大型語言模型回答前，先從外部資料找出相關內容，再根據這些內容回答。
---

## 是什麼

RAG 是 Retrieval-Augmented Generation 的縮寫，中文常譯為「檢索增強生成」。它讓 LLM 在回答之前，先去參考訓練資料以外、具權威性的知識庫。[S2]

IBM 的定義是：從外部知識庫取得事實，讓回答建立在最新、正確的資訊上，也讓使用者看得到回答的依據。[S4]

課堂上的說法是：寫 prompt 本來就要提供「正確的資訊」，RAG 只是把找資料這件事交給電腦自己做，所以它其實就是 Context Engineering。[S6]

## 名稱由來

這個名詞來自 2020 年 Patrick Lewis 等人的論文。論文把模型參數裡的知識稱為參數記憶，把可以查詢的外部向量索引稱為非參數記憶，RAG 就是把兩者結合起來。[S1]

Lewis 曾為這個不太好聽的縮寫道歉，說如果早知道會這麼普及，會取個更好的名字。[S3]

## 為什麼重要

- 不用重新訓練模型，就能讓 LLM 使用特定領域或公司內部的知識。[S2]
- 情況改變時，只要更新資料，不用重新訓練。[S4]
- 回答可以附上來源，使用者能自己查證。[S2][S3]

## 相關概念

- [[llm-limitations]]：RAG 要解決的問題
- [[rag-workflow]]：RAG 的運作步驟
- [[analogies]]：開書考、法院書記官等比喻
- [[rag-limitations]]：RAG 做不到的事
