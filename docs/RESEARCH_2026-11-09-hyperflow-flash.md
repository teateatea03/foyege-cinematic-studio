# HyperFlow H3 Flash 教學：可採用方法與未驗證項

使用者提供 [零度解說影片](https://www.youtube.com/watch?v=n6MeunOm980)，2026-11-09，10:09。本輪把本機路線的能力核對與試產方法補進 [Foyege 適配](../skills/foyege-cinematic-direction/references/hyperflow-flash.md)，並接到 [製作測試](../skills/film-production/references/testing-and-review.md)。Foyege24 的微表演、空間、動作因果與接鏡仍是核心。

## 影片與第一方來源交叉核對

| 位置／證據 | 觀察 | 對技能的影響 |
| --- | --- | --- |
| 字幕 00:35–00:58，模型頁 00:38 | 介紹壓縮 H3，字幕誤寫成 2.3 | 型號用畫面和第一方文件核對；不把舊 H3 LoRA 配方當 Flash |
| 畫面 02:02、02:35 | 桌面客戶端 V0.14.2；管理器展示官方／社群兩包 | 分記桌面、核心、節點版本；官方新 loader 已含 INT8，不照舊教學強制加社群包 |
| 字幕 03:19–05:50，畫面 04:45／05:25 | 主模型以外仍需編碼器與兩種 VAE | 優先查既有配套，不把小主模型等同低全流程需求 |
| 字幕 05:56–06:18、08:58 | 作者推薦低顯存 GGUF，但其自述測試卡是 24GB | 上游明示 16GB GPU 尚未量測；5080 保留待測，不承諾成功或速度 |
| 字幕 07:46–08:20 | ref2v 工作流缺另一份主權重 | 明確分開 fl2va／ref2va，參考生成不是把同一模型換一張圖 |
| 抽幀 09:34–09:44 | 雙人近景中先後出現嘴部動作、景別改變，之後抬手靠近臉部 | 嘴部話輪、聽者目光、切點及接觸分項驗收；稀疏圖不證明精確眼頭延遲 |
| 字幕 09:44 | 作者指出聲音有問題 | 原生音訊獨立檢查；本輪未親聽，不能將作者評語當成本機聲音診斷 |

## 第一方核對與本機盤點

固定閱讀兩個來源：Flash runtime [703747e](https://github.com/Video-Rebirth/hyperflow-h3-flash/tree/703747ee414f895985a4c3b87e59f4fd03fc9f14)，官方節點 [c807a89](https://github.com/Video-Rebirth/ComfyUI-HyperFlow-Flash/tree/c807a89653569531b5c61ef691060acf467c552c)。閱讀架構、runtime／輸入差異、記憶體、benchmark 條件、loader、sigmas、README 及八份 API graph。

靜態核對八份 graph 的模型分支、量化、副檔名、6 步 sigmas、Euler／BasicGuider、節點引用及適用格數；四份 loader／patch 檔通過 Python AST。這不是 ComfyUI 可載入或推論測試，亦未重發 GPL 節點／工作流。

本機核心原始碼 git describe 回報 v0.44.2，ComfyUI-GGUF 目錄與官方 NVFP4 文字編碼器、影音 VAE 檔案存在；只檢查名稱與非零大小。此安裝的 diffusion_models 未見 Flash 權重、custom_nodes 未見官方 Flash 包，既有 pruned H3 不算 Flash。沒有安裝新節點、下載權重、更新 ComfyUI、重啟服務或載入模型。5080 當時 99% 負載，沒有本輪推論／效能／微表情結論。

## 已落地的改善

1. Foyege 新增按需適配：模型分流、圖序責任、正向保持狀態、專用採樣、圖尺寸成本與原生聲音邊界。
2. 製作統籌增加單人反應→雙人接觸→對白的分層試產，沿用授權候選上限和可用秒數成本。
3. Codex／Claude 核心入口、製作模板、資源路由及來源索引補同一參考，保留各自既有內容與規則。
4. 實際要測 5080 時，先修缺件、隔離工作流，固定參考／尺寸／格數後測 6 步基準，再按結果選擇步數比較；本輪沒有自動排入 GPU 任務。

可核對的媒體 hash、43 個取樣時間及靜態 graph 結果見 [證據摘要](experiments/2026-11-09-hyperflow-flash/evidence.json)。

## 分析範圍

讀取全片 296 條 YouTube 自動字幕；已看 16 張分散樣本，另看 08:48–08:53 每 0.5 秒的 10 張、09:28–09:45 每秒的 17 張，共 43 張時間取樣，非逐幀連續播放。未做獨立音訊聽審、ASR 或外部 VLM。REA 整片 decompose 在本輪觀察期間未產出分鏡／breakdown，自動拆解作業已停止，沒有完成全片機器分類或 apply-review。REA 的加密抽幀成功，用於局部複核；以上結論來自已讀字幕、已看樣本及原始碼，不以未產出的工具分類作證。原影片、字幕、靜幀與完整研究輸出留在本機研究目錄，公開只放原創分析及不含媒體的證據摘要。
