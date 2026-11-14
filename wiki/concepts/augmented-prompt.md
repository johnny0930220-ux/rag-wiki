---
title: 擴增 prompt
aliases: [擴增 prompt, prompt]
sources: [S2, S4, S6]
summary: 把找到的資料和使用者的問題一起放進新的 prompt，交給 LLM 回答。
---

## 是什麼

把檢索到的資料當作上下文，加進使用者的 prompt，讓 LLM 能根據這些資料正確回答。[S2]

LLM 會結合找到的資料和自己訓練學到的知識產生回答，回答可以連回來源。[S4]

## Prompt 範例

課堂上的範例：「請根據 {retrieved_chunks} 裡的資訊，回應使用者的問題：{question}」。[S6]

## 相關概念

- [[rag-workflow]]
- [[citations-trust]]
