---
title: RAG 的限制
aliases: [RAG 的限制]
sources: [S4, S5]
summary: RAG 不完美：仍可能幻覺、不會自己承認不知道，而且找不找得到資料也是問題。
---

## 仍然可能出錯

- IBM 的文章直說 RAG 並不完美，要做好還有很多挑戰。[S4]
- RAG 能降低幻覺，但不能消除；它也不會讓模型自動承認不知道。要讓模型辨認答不出來的問題，需要特別訓練。[S4]

## 找不到對的資料

檢索本身也會失敗。Anthropic 的實驗用「前 20 名沒找到相關段落的比例」衡量，一般做法的失敗率是 5.7%。[S5]

## 資料很少時不一定需要

知識庫小於 20 萬個 token（大約 500 頁）時，可以直接整個放進 prompt，不需要 RAG。[S5]

## 相關概念

- [[hallucination]]
- [[long-context]]
- [[contextual-retrieval]]
