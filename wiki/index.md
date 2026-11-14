# RAG Wiki 索引

這個 wiki 整理 6 篇關於 RAG（檢索增強生成）的資料。每個概念一頁，內文都標了來源 [S1]～[S6]。

## 入門

- [[rag]] RAG（檢索增強生成）：讓大型語言模型回答前，先從外部資料找出相關內容，再根據這些內容回答。
- [[llm]] 大型語言模型（LLM）：用大量文字訓練、把知識存在參數裡的模型，例如 ChatGPT 背後的模型。
- [[llm-limitations]] LLM 的限制：LLM 的知識有截止日期、可能過時或錯誤，也很難說出知識的出處。
- [[hallucination]] 幻覺（hallucination）：模型給出聽起來合理、但其實是錯誤的答案。RAG 能降低，但不能消除。
- [[analogies]] 理解 RAG 的比喻：開書考、法院書記官、過度熱心的新員工，三個幫助理解 RAG 的比喻。

## RAG 怎麼運作

- [[rag-workflow]] RAG 的運作流程：準備資料、把問題轉成向量去找資料、把資料放進 prompt、讓 LLM 回答。
- [[chunking]] 切塊（chunking）：把長文件切成一小塊一小塊再做 embedding；切法會影響找不找得到。
- [[embedding]] Embedding（向量表示）：把一段文字轉成一串數字（向量），意思相近的文字，向量也會靠近。
- [[vector-database]] 向量資料庫：存放大量文字向量、能快速找出和問題最接近的資料庫。
- [[retrieval]] 檢索（retrieval）：根據使用者的問題，從資料庫找出最相關的幾段資料。
- [[augmented-prompt]] 擴增 prompt：把找到的資料和使用者的問題一起放進新的 prompt，交給 LLM 回答。
- [[citations-trust]] 附來源與信任：RAG 的回答可以附上資料來源，讓使用者自己查證。

## 限制與替代做法

- [[rag-limitations]] RAG 的限制：RAG 不完美：仍可能幻覺、不會自己承認不知道，而且找不找得到資料也是問題。
- [[long-context]] 直接放進 prompt（長上下文與 CAG）：資料不多時，不必檢索，直接把全部資料放進 prompt。
- [[llm-wiki]] LLM Wiki：讓 LLM 自己把來源整理成 Markdown 知識庫，再用這個知識庫回答問題。

## 進階檢索技巧

- [[bm25-hybrid-search]] BM25 與混合搜尋：用字詞比對找精確字串，和 embedding 的語意搜尋互補。
- [[contextual-retrieval]] Contextual Retrieval：替每個文字塊補上一段上下文，再做 embedding 和 BM25，降低找不到的機率。
- [[reranking]] Reranking（重新排序）：先多找一些候選資料，再用另一個模型重新評分，只留最相關的。

## 來源

- [[s1]] S1｜RAG 原始論文（Lewis et al., 2020）：提出 RAG 這個名稱：把預訓練模型的參數記憶，接上 Wikipedia 向量索引的非參數記憶。
- [[s2]] S2｜AWS〈What is RAG?〉：企業角度的 RAG 入門：LLM 的四個問題、RAG 的四個好處和四個步驟。
- [[s3]] S3｜NVIDIA〈What Is Retrieval-Augmented Generation〉：用「法院書記官」比喻 RAG，說明名稱由來、運作流程和應用例子。
- [[s4]] S4｜IBM Research〈What is retrieval-augmented generation?〉：用「開書考」比喻 RAG，並清楚說明 RAG 只能降低、不能消除幻覺。
- [[s5]] S5｜Anthropic〈Contextual Retrieval〉：切塊會讓文字失去上下文；加上上下文、混合 BM25 和 reranking，可讓檢索失敗率降低 67%。
- [[s6]] S6｜課程第 7 週投影片《讓 AI 看懂你的世界》：課堂上的 RAG：embedding 模型、切塊、流程，以及 CAG 和 LLM Wiki 兩種替代思路。
