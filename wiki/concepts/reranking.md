---
title: Reranking（重新排序）
aliases: [reranking, 重新排序, reranker]
sources: [S5, S6]
summary: 先多找一些候選資料，再用另一個模型重新評分，只留最相關的。
---

## 是什麼

課堂上提到，找出來的資料通常不只一筆，可能需要重新排序。[S6]

Anthropic 的做法：先檢索出前 150 塊，用 reranker 依問題重新評分，只留前 20 塊交給模型。[S5]

## 取捨

reranking 會增加一些延遲，要在「多排一些、效果較好」和「少排一些、較快較便宜」之間取捨。[S5]

## 相關概念

- [[retrieval]]
- [[contextual-retrieval]]
