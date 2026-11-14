---
id: S4
title: What is retrieval-augmented generation?
author: Kim Martineau（IBM Research Blog）
date: 2023-08-22
url: https://research.ibm.com/blog/retrieval-augmented-generation-RAG
type: 研究機構部落格
fetched: 2026-11-14
---

# 擷取筆記：IBM Research〈What is retrieval-augmented generation?〉

> 本檔是讀原文後整理的擷取筆記，不是全文轉貼。

## 定義

- RAG 是一種 AI 框架：從外部知識庫取得事實，讓 LLM 的回答建立在最新、正確的資訊上，也讓使用者看得到模型回答的依據。
- 文章指出 LLM 知道詞和詞之間的統計關係，但不知道它們的意思（原文："know how words relate statistically, but not what they mean"）。

## 開書考的比喻

- IBM Research 的 Lastras 說，差別就像「開書考和閉書考」（原文："the difference between an open-book and a closed-book exam"）。
- 有 RAG 的模型可以翻資料作答，不只靠記憶。

## 兩個階段

1. **檢索（retrieval）**：用演算法找出和提問相關的片段。開放領域可以用網路文件；企業通常用範圍較小、較安全的來源。
2. **生成（content generation）**：把找到的資料附加到 prompt 裡，LLM 結合這些資料和自己訓練學到的知識產生回答，回答可以連回來源。

## 好處

- 能取得最新、可靠的事實，情況改變時不用重新訓練模型。
- 使用者可以拿來源核對模型的說法，比較能信任。
- 回答建立在可查證的外部事實上，模型比較少依賴參數裡記住的內容，降低洩漏敏感資料或產生幻覺的風險。
- 企業聊天機器人的運算和金錢成本較低。

## 限制

- 文章直說 RAG 並不完美，要做好還有很多挑戰。
- RAG 能**降低**幻覺風險，但不能消除；它本身也不會讓模型承認自己不知道。
- 要讓模型辨認自己答不出來的問題，需要特別訓練，可能要上千個「答得出來」和「答不出來」的例子。
- RAG 依賴向量表示和向量資料庫來找資料。

## 例子

- **成功例子（請假）**：員工問能不能請半天假、假還夠不夠。系統查她的人資紀錄和公司半天假規定，LLM 再用這些事實寫出個人化回答，並附上來源連結。
- **失敗例子（產假）**：沒有 RAG 的聊天機器人回答產假問題時說「想請多久就請多久」。實際上產假規定依州或國家而不同，模型應該說不知道或追問細節。
