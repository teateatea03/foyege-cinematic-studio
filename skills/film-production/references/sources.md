# 來源、採用方式與證據範圍

基礎研究：2026-11-07，閱讀下列 S1–S8 的相關內文並整合既有 Foyege 研究；未觀看其中嵌入的完整成片／示範，也未在本機重現效果或成本。2026-11-09 增補 S9–S11 的對白短劇、官方 H3 與節點查核；證據範圍分列於各來源，不以文字演練或 JSON 可解析宣稱實際出片通過。

來源支持的是具體方法或案例經驗。表單、事件定義、返工決策與權限對接是本技能的設計，不宣稱作者使用過相同表單。

## 已讀內文

### S1｜The Bends 製作團隊：About

[原頁](https://www.thebendsfilm.com/about)。讀取影片與 Tech & Workflow 全段；日期未標。

- 團隊自述以導演 animatic 引導製作，並經傳統 VFX、調色與聲音處理。

- 採用：前期先看節奏，生成與後期需要交接。

- 限制：製作方介紹，不是獨立效能評測；不照搬其規模、成本或客製工具。

### S2｜Sahil Lulla、Rachel Jobin：The Bends 製作流程

[原頁](https://www.thebendsfilm.com/media/how-generative-ai-is-rewriting-key-aspects-of-production-workflows)。已讀文章內文；頁面僅標 Oct 20，未據此推定年份。

- 團隊描述低位元來源的修復／後期問題，強調生成運動並非可靠的物理模擬。

- 採用：品質問題分層處理，動作先查因果，後期保留原生／衍生版本。

- 限制：有 Topaz 支持及工具案例；不把升位元當成恢復真實資訊，不新增 LoRA、付費修復或模型訓練依賴。

### S3｜ScreenSkills：Script supervisor skills

[原頁](https://www.screenskills.com/skills-checklists/scripted-film-and-tv/script-supervisor-department/script-supervisor-skills/)。讀取職責概述與責任範圍，未下載另附 PDF。

- 機構說明場記從前期拆解／時間估計連到現場的實體、情緒連續性與剪輯交接。

- 採用：連續性不只比對道具，也記表演與切點狀態。

- 限制：一般專業職責，AI 工單欄位與權限映射由本專案另定。

### S4｜Evandro Miguel Jr.：Making ISA

[原頁](https://evandro-miguel.com/articles/isa-short-film-production/)，2026-10-15。讀取製作規劃、參考分工、Blender、失敗修訂、剪接、字幕及歸檔等段落；未宣稱完整觀看媒體。

- 作者自述的失敗／修訂紀錄，將參考、實際輸出及選片決定分開；談及中央互動失敗與最終匯出檢查。

- 採用：先完成故事關鍵小段落，按失敗層修正，工程交付與播放檔分開。

- 限制：個人自述，作者也提供商業服務；未獨立審計其成片、統計或費用，不拿其數字估算本機成本。

### S5｜Chad Nelson 原始訪談：Critterz

[AWN 訪談](https://www.awn.com/animationworld/chad-nelson-talks-critterz-and-future-role-ai)，2023-07-14。讀取實際製作／animatic 相關問答。

- 導演談到用 stills 做 animatic，以及由動畫、表演與剪輯完成作品。

- 採用：先用低成本節奏樣片檢查故事，不把生成一張圖當成完成一鏡。

- 限制：較早期、偏圖像設計加傳統動畫的案例，不是 H3 測試；不外推工期／工具效果。

### S6｜Runway：Gen-4 Video Prompting Guide

[官方指引](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide)。讀取 Prompting Basics、Best Practices、Image prompts 與主要動作類型段落。

- 該版建議簡潔正向、聚焦動作，漸次加入變項。

- 採用：完整導演卡與模型執行 prompt 分開，避免一條通用長模板。

- 限制：Gen-4 的規則與輸入條件不能當成本機 H3 的規格；不是啟用 Runway 或付費路線的建議。

### S7｜Cassidy Curtis、Sarah Rumbley：Dear Upstairs Neighbors

[Google 製作團隊原文](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/dear-upstairs-neighbors/)，2026-01-26。讀取正文的設計、微調、Show don't type、逐鏡修訂段落；非頁面自動摘要。

- 團隊以手作動畫傳達精確表演與運鏡，再用客製模型處理風格，逐鏡檢查修訂。

- 採用：遇到精確節奏瓶頸，評估可用視覺控制／預演，不無限加形容詞。

- 限制：客製研發流程；不表示本機 H3 接受相同控制，也不授權微調、雲端或新下載。

### S8｜Adobe：Changing clip speed and duration

[官方說明](https://helpx.adobe.com/premiere/desktop/edit-projects/change-clip-speed/different-ways-to-change-clip-speed-and-duration.html)，更新 2026-01-07。讀取速度／長度與可用處理方式正文。

- 速度改變與片段長度相關，存在整段及變速處理方式。

- 採用：先量有效動作再計算速度，保護音軌並驗修後結果。

- 限制：時間換算及本專案的修復判準是本技能推導；未採用通用倍速上限，不以此要求購買 Premiere。

### S9｜Miller：Claude＋H3 短劇教程、技能包與光影速查

[原文](https://x.com/TuyetloanP81840/status/2119326884505043274)、[資料庫](https://miliagent.com/library/)、[光影教材](https://miliagent.com/light/)。2026-11-08 至 11-09 直接讀取原始 X 網頁、完整解碼三個 SKILL.md 與先讀我，抽取 PDF 全部 25 頁文字、渲染全頁並視覺抽查 12 頁。

- 採用：資產用途與穩定 ID、先驗證小段交流、對白與反應鏡頭交接、出片／問題時間窗紀錄、先評估裁切再局部補拍。
- 修正後採用：反打由空間與機位推導，光源固定在世界中；內心獨白閉嘴但有聲；生成段與剪輯鏡分列。
- 未採用：固定五分鐘／字數／每鏡秒數、硬性切鏡數、對白運鏡必敗、字面 @ 標記的通用性、固定人民幣套餐與扣幣、每步等待確認或綁定某雲端平台。
- 限制：原文仍有工作流、費用確認、機器扣費及成片示例占位；下載只有文字指南，沒有作者工作流 JSON。未驗證作者成片、實際扣費或品質比較，未把下載技能原封安裝。
- 本機研究另有保存，未隨公開包附原始媒體；來源連結與閱讀範圍保留，私人研究目錄不是技能運作依賴。

### S10｜MiniMax：H3 官方開放範圍與規格

[官方公告](https://www.minimax.io/news/minimax-h3-open-source)、[官方程式庫](https://github.com/MiniMax-AI/MiniMax-H3)、[原始授權](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE)。本次讀取公告、README、API 文件／價格、FAQ 與授權原文。

- 採用：區分 Base、Context-IR、Regenerate-2K；角色聲線參考、實際台詞與聲音驅動分開；不同模式的參考數量及限制需逐項核對。
- 限制：官方規格不能證明本機量化配方、雲端費率、跨段身份或口型成功率。社群二採／超分不稱官方 2K 同等效果；授權和價格可能變更，使用時核對當前版本，不將研究時數字寫成執行預設。

### S11｜nkxx188：ComfyUI-MiniMaxH3-Easy

本次查到並固定為 [4b496eedeff944b2f1266c8c92df1b6c89758de0](https://github.com/nkxx188/ComfyUI-MiniMaxH3-Easy/tree/4b496eedeff944b2f1266c8c92df1b6c89758de0)，閱讀中英文說明、工作流說明、相關模型載入／參考／數字人／採樣程式，下載並解析基本工作流 JSON。

- 採用：參考用途要對應實際槽位與 Picture／Audio 標籤；區分聲線參考與驅動音訊；基本生成、精修與分段工作流不能當作同一配置。
- 限制：上游基本樣例預設 360P、五秒、八步及 randomize，並非作者 640P 固定 seed 配方；需要外部模型與素材。只確認源碼和 JSON，不表示已安裝、相容、推論成功或能重現作者扣費。

新增表格、聲音意圖欄位、生成段對照及成本口徑是本技能的整合設計；未經完整短劇實作驗證，也不冒稱來源作者使用同一套表單。

## Foyege24：既有原始研究 F1–F5

以下為 2026-11-02 研究留下的讀取範圍；此次重讀本機 sources、production、microacting、spatial-previs，沒有冒稱新看完全部影片。本文的 Foyege 整合見 [導演與提示詞](directing-and-prompts.md)。

| ID | 原始來源 | 既有證據／可採用內容 |
|---|---|---|
| F1 | [提示詞生成器](https://x.com/Foyege24/status/2046140862577430578) | 既有研究標為全文閱讀；美學、參考責任、時間段與約束。15 秒、字數、無 BGM 是該範例條件 |
| F2 | [多人空間](https://x.com/Foyege24/status/2092127885708718278) | 既有全文閱讀；俯視拓撲、ID、機位與眼線分層 |
| F3 | [Blender 白模流程](https://x.com/Foyege24/status/2098289393912156369) | 既有抽樣畫面＋CPU ASR；包括約 09:00 的微表演投影片，不等同完整連續播放／聽審 |
| F4 | [動作主串](https://x.com/Foyege24/status/2098630949223428407)／[示例](https://x.com/Foyege24/status/2098630954122437038) | 既有全文閱讀；發力、接觸、反作用、恢復與殘留 |
| F5 | [白模與文字分工](https://x.com/Foyege24/status/2104381577476067796) | 既有全文閱讀；預演處理空間／運動，文字補表演與質感 |

原創表演卡、MV 音軌對位、連續性帳及驗收方式是本機延伸，不全數歸給作者，也不宣稱還原其未公開製程。相關細節可按需讀已安裝的 foyege-cinematic-direction；本共用技能已保留必要方法，不依賴對方機器必須有相同安裝路徑。

## 本專案自己的證據


- [T01 技術交付](https://github.com/teateatea03/HitomiVideoStudio/issues/36#issuecomment-6692509475)：14 支原生輸出、設定、時間與技術校驗。

- [Claude 的 T01 檢查](https://github.com/teateatea03/HitomiVideoStudio/issues/36#issuecomment-6700748567)：抽格方法、首圖／首尾圖結果、時機問題及 25／35 步比較。這是該次小樣本，不能當通用成功率。

- [Owner 看後意見及原技能工單](https://github.com/teateatea03/HitomiVideoStudio/issues/36#issuecomment-6701312366)：自然度、快速握腕與臉頰凹陷仍需改善。

- M01 動作、L01 對嘴紀錄仍以原 #36 工單與不可變交付為準。本次未重跑。

- 來源一致、文件合規與文字演練不能代替本機推論、連續看片或 Owner 接受。v0.2 的整片成效尚待首部實作驗證。

## 保留但未提升證據等級的來源

原 v0.1 的 Higgsfield、Frameo、invideo、人人都是產品經理及 Dreamina 連結只讀過搜尋摘要，這次不把它們當作已讀正文或獨立創作者經驗：


- [Higgsfield](https://higgsfield.ai/blog/ai-short-film-pipeline)

- [Frameo](https://frameo.ai/blog/ai-film-production-workflow-guide)

- [invideo storyboard-first](https://invideo.io/faq/what-is-a-storyboard-first-ai-filmmaking-workflow-and/)

- [invideo 一致性](https://invideo.io/faq/how-do-you-keep-ai-generated-video-shots-visually/)

- [人人都是產品經理](https://www.woshipm.com/ai/6348309.html)

- [Dreamina](https://dreamina.capcut.com/zh-tw/resource/how-to-make-ai-short-film)

本次 [ETCentric 一致性文章](https://www.etcentric.org/consistency-is-key-lessons-on-generative-ai-via-the-bends/) 抓取逾時，仍只列既有摘要；另讀的是 S1、S2，不能混稱同一篇全文。

Blender Studio Project Gold 文章回覆 402、公開 editorial 路徑無法讀取、Toon Boom pre-production 回覆 403：記為未取得，不拿摘要補作正文，也未繞過付費／存取限制。
