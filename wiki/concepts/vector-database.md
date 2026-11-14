---
title: 向量資料庫
aliases: [向量資料庫, vector database, 向量索引]
sources: [S1, S2, S3, S6]
summary: 存放大量文字向量、能快速找出和問題最接近的資料庫。
---

## 是什麼

RAG 會把外部資料轉成向量後存進向量資料庫，之後拿問題的向量來比對。[S2]

RAG 原始論文用的外部記憶，就是 Wikipedia 的稠密向量索引，透過神經檢索器存取。[S1]

## 需要持續更新

知識庫內容變動時，embedding 模型要持續建立和更新向量資料庫。[S3]

## 相關概念

- [[embedding]]
- [[retrieval]]
- [[chunking]]
