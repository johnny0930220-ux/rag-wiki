---
id: S1
title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
author: Patrick Lewis 等 12 人
date: 2020-05-22（arXiv 初版）；v4 為 2021-04-12
url: https://arxiv.org/abs/2005.11401
type: 論文
fetched: 2026-11-14
---

# 擷取筆記：RAG 原始論文（Lewis et al., 2020）

> 本檔是讀原文後整理的擷取筆記，不是全文轉貼。重點以中文改寫，只保留必要的英文術語。

## 基本資料

- 作者：Patrick Lewis、Ethan Perez、Aleksandra Piktus、Fabio Petroni、Vladimir Karpukhin、Naman Goyal、Heinrich Küttler、Mike Lewis、Wen-tau Yih、Tim Rocktäschel、Sebastian Riedel、Douwe Kiela。
- arXiv 編號 2005.11401，分類 cs.CL、cs.LG。2020-05-22 送出，第 4 版 2021-04-12。

## 摘要重點（改寫）

1. 大型預訓練語言模型把事實知識存在**參數**裡，微調後表現不錯，但很難精準存取和操作這些知識，所以在知識密集型任務上輸給專門設計的架構。
2. 「替模型的決定提供出處（provenance）」和「更新模型的世界知識」仍是尚未解決的問題。
3. 論文提出一套通用的微調方法，稱為 retrieval-augmented generation（RAG），結合兩種記憶：
   - **參數記憶（parametric memory）**：預訓練的 seq2seq 模型。
   - **非參數記憶（non-parametric memory）**：Wikipedia 的稠密向量索引（dense vector index），用預訓練的神經檢索器（neural retriever）存取。
4. 兩種做法：一種是整段生成都用同一批檢索到的段落；另一種是每個 token 可以用不同的段落。
5. 在三個開放領域問答（open-domain QA）任務上達到當時最佳，勝過只用參數的 seq2seq 模型和「先檢索再擷取」的專門架構。
6. 在語言生成任務上，RAG 產生的文字比只用參數的 seq2seq 基準更具體、更多樣、更符合事實。
