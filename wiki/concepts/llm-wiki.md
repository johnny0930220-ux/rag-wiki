---
title: LLM Wiki
aliases: [LLM Wiki, Karpathy]
sources: [S6]
summary: 讓 LLM 自己把來源整理成 Markdown 知識庫，再用這個知識庫回答問題。
---

## 是什麼

Karpathy 在 2026 年 4 月分享的做法：把來源放進 raw 資料夾，讓 LLM 把它們「編譯」成一系列 Markdown 頁面，包含摘要、反向連結和概念文章。[S6]

## 和 RAG 的關係

wiki 夠大（約 100 篇、40 萬字）時可以拿來問複雜問題。Karpathy 原本以為需要複雜的 RAG，但 LLM 自己維護的索引和摘要就夠用了。[S6]

答案可以輸出成 Markdown 或投影片再歸檔回 wiki，也可以請 LLM 健檢，找出不一致或缺漏的地方。[S6]

## 相關概念

- [[rag]]
- [[long-context]]
