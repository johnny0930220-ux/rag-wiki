---
id: S3
title: What Is Retrieval-Augmented Generation, aka RAG?
author: Rick Merritt（NVIDIA Blog）
date: 2023-11-15 初版；2025-01-31 更新
url: https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/
type: 企業部落格
fetched: 2026-11-14
---

# 擷取筆記：NVIDIA〈What Is Retrieval-Augmented Generation〉

> 本檔是讀原文後整理的擷取筆記，不是全文轉貼。

## 法院書記官的比喻

- 法官靠一般法律知識判案；遇到特殊案件，會請書記官去法律圖書館找判例。
- LLM 能回答各種問題，但要給出有根據的權威答案，就得把特定資料提供給模型。
- 文章稱 RAG 是「AI 的法院書記官」（原文："The court clerk of AI"）。

## 名稱由來

- 2020 年提出這個名詞的論文，第一作者是 Patrick Lewis。
- Lewis 曾為這個縮寫道歉，說如果早知道會這麼普及，會取個更好的名字。
- 論文把 RAG 描述成「通用的微調方法」，幾乎任何 LLM 都能用它連接外部資源。
- 研究在 Meta AI 位於倫敦的實驗室完成，共同作者來自 Meta AI、倫敦大學學院（UCL）和紐約大學。Lewis 後來在 Cohere 帶領 RAG 團隊。

## RAG 怎麼運作

1. 使用者的問題送進 embedding 模型，轉成數字形式，稱為 embedding 或向量。
2. 把這個向量和知識庫索引裡的向量比對。
3. 找到相符的資料後取出來，轉回人看得懂的文字，交給 LLM。
4. LLM 結合取回的文字和自己的回答，產生最後答案，並可以附上來源。

背景中，embedding 模型會隨著知識庫變動，持續建立和更新向量資料庫。開源函式庫 LangChain 常被用來把 LLM、embedding 模型和知識庫串起來。

## 好處

- **可以附引用**：像論文的註腳一樣，使用者能自己查證，建立信任。
- **釐清模糊問題**：可以幫模型釐清不清楚的提問。
- **降低幻覺**：減少模型給出「聽起來合理但錯誤」答案的機會。
- **容易導入**：最少大約五行程式碼就能實作，比用新資料重新訓練模型更快、更便宜，資料來源也能隨時更換。

## 應用例子

- 連接醫療索引的模型可以協助醫師和護理師。
- 連接市場資料的助理可以協助金融分析師。
- 企業可以把技術手冊、政策手冊、影片或紀錄變成知識庫，用在客服、員工訓練和開發。
- 在個人電腦上，RAG 可以把本機模型接到自己的 email、筆記或文章，資料和對話都留在本機。
