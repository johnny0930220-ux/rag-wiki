# 簡報大綱：RAG——讓 AI 先查資料再回答

> N4 產出（第 2 版流程）。只根據 wiki 撰寫。每一個重點句後面用〔頁面〕標出它來自哪個 wiki 頁，C2 會檢查。
> 讀者：用過 ChatGPT 的一般人。

## 第 1 頁：RAG：讓 AI 先查資料再回答
- wiki: rag
- 新名詞: RAG
- 重點:
  - RAG 是 Retrieval-Augmented Generation 的縮寫，中文叫「檢索增強生成」。〔rag〕
  - 一句話：讓 AI 回答之前，先去翻訓練資料以外的可靠資料。〔rag〕

## 第 2 頁：ChatGPT 背後的大型語言模型
- wiki: llm
- 新名詞: LLM
- 重點:
  - LLM 用大量文字訓練，學到的知識存在模型的參數裡。〔llm〕
  - 訓練資料是固定的，有截止日期。〔llm〕
  - 它知道詞和詞之間的統計關係，但不一定懂真正的意思。〔llm〕

## 第 3 頁：LLM 常見的四個問題
- wiki: llm-limitations
- 新名詞: 無
- 重點:
  - 不知道也照答、資訊過時、來源不可靠、同詞不同義。〔llm-limitations〕
  - 知識存在參數裡，模型很難說出出處，也很難更新。〔llm-limitations〕

## 第 4 頁：幻覺：聽起來對，其實是錯的
- wiki: hallucination, llm-limitations
- 新名詞: 幻覺
- 重點:
  - 幻覺：模型給出聽起來合理、但其實不正確的答案。〔hallucination〕
  - 產假例子：機器人回答「想請多久就請多久」，但規定依地區不同，應該說不知道或追問。〔llm-limitations〕

## 第 5 頁：RAG 就像開書考
- wiki: rag, analogies
- 新名詞: 開書考
- 重點:
  - 閉書考只能靠記憶；開書考可以翻資料再作答。〔analogies〕
  - RAG 讓 LLM 回答前先參考訓練資料以外的權威資料。〔rag〕
  - 要加新知識時不用重新訓練模型，更新資料就好。〔rag〕

## 第 6 頁：另外兩個比喻
- wiki: analogies
- 新名詞: 法院書記官, 新員工
- 重點:
  - 法官遇到特殊案件，請書記官去法律圖書館找判例；RAG 就是 AI 的書記官。〔analogies〕
  - 沒有 RAG 的 LLM 像過度熱心的新員工，不看最新消息卻很有自信地回答。〔analogies〕

## 第 7 頁：RAG 的四個步驟
- wiki: rag-workflow
- 新名詞: 無
- 重點:
  - 先看全貌：準備資料 → 找出相關資料 → 把資料交給 AI 回答 → 定期更新資料。〔rag-workflow〕
  - 後面四頁一步一步講，每一步再介紹正式名稱。〔rag-workflow〕

## 第 8 頁：步驟一之前：把資料切成小塊
- wiki: chunking
- 新名詞: 切塊
- 重點:
  - 長文件先切成文字塊，例如每塊 500 字、重疊 50 字。〔chunking〕
  - 切開後可能看不懂：財報的一塊只寫「公司營收比上一季成長 3%」，看不出是哪家公司、2023 年哪一季。〔chunking〕
  - 切多大、要不要重疊，會影響找不找得到。〔chunking〕

## 第 9 頁：把文字變成一串數字
- wiki: embedding, vector-database
- 新名詞: embedding, 向量資料庫
- 重點:
  - embedding 把文字轉成一串數字（向量），代表它的意思，意思相近就靠近。〔embedding〕
  - 例子：「圖書館星期日幾點關門？」靠近「本館週日開放至下午五點」，遠離「本館借書期限為三十天」。〔embedding〕
  - 所有向量存進向量資料庫，之後拿來比對。〔vector-database〕

## 第 10 頁：找出最相關的資料
- wiki: retrieval, reranking
- 新名詞: 檢索, 重新排序
- 重點:
  - 問題也轉成向量，找出最接近的幾塊；比對的是意思，不只是字面。〔retrieval〕
  - 找到的通常不只一塊，有時要重新排序（把最相關的排前面），或把前後文一起拿進來。〔retrieval〕〔reranking〕
  - 開放領域可以搜尋網路文件；公司內部通常只用範圍較小、較安全的資料。〔retrieval〕

## 第 11 頁：把資料放進 prompt，再回答
- wiki: augmented-prompt, citations-trust
- 新名詞: 擴增 prompt, 附上來源
- 重點:
  - 把找到的資料和問題放在一起交給 LLM。〔augmented-prompt〕
  - 課堂範例：「請根據 {retrieved_chunks} 裡的資訊，回應使用者的問題：{question}」。〔augmented-prompt〕
  - 回答可以附上來源，像論文的註腳，讓人自己查證。〔citations-trust〕

## 第 12 頁：實際例子：問年假的 HR 機器人
- wiki: rag-workflow, citations-trust
- 新名詞: 無
- 重點:
  - 員工問「我還有多少年假？」，系統找出年假政策文件和請假紀錄。〔rag-workflow〕
  - 把資料和問題交給 LLM 回答。〔rag-workflow〕
  - 回答也可以附上資料來源讓人查證。〔citations-trust〕

## 第 13 頁：RAG 也不是萬能
- wiki: rag-limitations, hallucination
- 新名詞: 無
- 重點:
  - RAG 只能降低幻覺，不能消除。〔hallucination〕
  - RAG 不會讓模型自動承認不知道，這需要另外訓練。〔rag-limitations〕
  - 檢索本身也會失敗，找不到對的段落就答不好。〔rag-limitations〕

## 第 14 頁：資料不多時，可以直接全部放進去
- wiki: long-context, llm-wiki
- 新名詞: CAG, LLM Wiki
- 重點:
  - 資料小於 20 萬個 token（大約 500 頁）時，可以不檢索，整份放進 prompt。〔long-context〕
  - CAG 先用 KV-Cache 把資料存起來再交給 LLM。〔long-context〕
  - LLM Wiki 讓 LLM 自己把資料整理成筆記和索引，資料量不大時不一定要複雜的 RAG。〔llm-wiki〕

## 第 15 頁：小測驗與總結
- wiki: rag, rag-workflow, rag-limitations
- 新名詞: 無
- 重點:
  - 三題選擇題：RAG 解決什麼問題？流程順序？能不能消除幻覺？〔rag〕〔rag-workflow〕〔rag-limitations〕
  - 總結：RAG 讓 AI 先查資料再回答，但看到答案還是要查來源。〔rag〕
