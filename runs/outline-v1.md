# 簡報大綱：RAG——讓 AI 先查資料再回答

> N4 產出。只根據 wiki 撰寫，每頁的 wiki: 列出用到的頁面。讀者：用過 ChatGPT 的一般人。

## 第 1 頁：RAG：讓 AI 先查資料再回答
- wiki: rag
- 新名詞: RAG
- 重點: 標題頁。副標「檢索增強生成（Retrieval-Augmented Generation）」，一句話：讓 AI 回答前先去翻資料。

## 第 2 頁：ChatGPT 背後的大型語言模型
- wiki: llm
- 新名詞: LLM
- 重點: LLM 用大量文字訓練，知識存在模型的參數裡；訓練資料有截止日期；它懂詞和詞的統計關係，不一定懂意思。

## 第 3 頁：LLM 常見的四個問題
- wiki: llm-limitations
- 新名詞: 無
- 重點: 不知道時亂答、資訊過時、來源不可靠、同詞不同義。也很難說出知識的出處。

## 第 4 頁：幻覺：聽起來對，其實是錯的
- wiki: hallucination, llm-limitations
- 新名詞: 幻覺
- 重點: 幻覺的定義；產假例子：機器人回答「想請多久就請多久」，但規定其實依地區不同。

## 第 5 頁：RAG 就像開書考
- wiki: rag, analogies
- 新名詞: 開書考
- 重點: 閉書考只能靠記憶；開書考可以翻資料。RAG 讓模型回答前先參考外部的權威資料，不用重新訓練模型。

## 第 6 頁：另外兩個比喻
- wiki: analogies
- 新名詞: 法院書記官, 新員工
- 重點: 法官請書記官去圖書館找判例；沒有 RAG 的 LLM 像過度熱心的新員工，什麼都很有自信地回答。

## 第 7 頁：RAG 的四個步驟
- wiki: rag-workflow
- 新名詞: 無
- 重點: 先看全貌：準備資料 → 找出相關資料 → 把資料交給 AI 回答 → 定期更新資料。後面四頁一步一步講，每一步再介紹它的正式名稱。

## 第 8 頁：步驟一之前：把資料切成小塊
- wiki: chunking
- 新名詞: 切塊
- 重點: 長文件要先切成文字塊，例如每塊 500 字、重疊 50 字；切太碎會失去上下文（ACME 營收的例子）。

## 第 9 頁：把文字變成一串數字
- wiki: embedding, vector-database
- 新名詞: embedding, 向量資料庫
- 重點: embedding 把文字變成向量，意思相近就靠近（圖書館關門時間的例子）；所有向量存進向量資料庫。

## 第 10 頁：找出最相關的資料
- wiki: retrieval
- 新名詞: 檢索
- 重點: 問題也變成向量，找出最接近的幾塊；它比對的是意思，不只是字面上一樣的字。

## 第 11 頁：把資料放進 prompt，再回答
- wiki: augmented-prompt, citations-trust
- 新名詞: 擴增 prompt, 附上來源
- 重點: prompt 範例「請根據 {retrieved_chunks} 裡的資訊，回應使用者的問題：{question}」；回答可以附上來源，讓人查證。

## 第 12 頁：實際例子：問年假的 HR 機器人
- wiki: rag-workflow, citations-trust
- 新名詞: 無
- 重點: 員工問「我還有多少年假？」→ 找出年假政策和請假紀錄 → LLM 回答並附上來源連結。

## 第 13 頁：RAG 也不是萬能
- wiki: rag-limitations, hallucination
- 新名詞: 無
- 重點: 只能降低、不能消除幻覺；不會自己承認不知道；檢索本身也可能找不到對的資料。

## 第 14 頁：資料不多時，可以直接全部放進去
- wiki: long-context, llm-wiki
- 新名詞: CAG, LLM Wiki
- 重點: 知識庫小於 20 萬個 token（約 500 頁）可以整個放進 prompt；CAG 用 KV-Cache 先存起來；LLM Wiki 讓 LLM 自己整理知識庫。

## 第 15 頁：小測驗與總結
- wiki: rag, rag-workflow, rag-limitations
- 新名詞: 無
- 重點: 三題選擇題：RAG 解決什麼問題？四個步驟的順序？RAG 能不能消除幻覺？最後一句總結。
