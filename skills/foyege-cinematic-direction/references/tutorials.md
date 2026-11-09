# 補充教學與採用範圍

2026-11-03 核對以下八份第一方文字教材／文件的相關正文。內嵌示範影片未在本次連續觀看，供應商宣稱的表現仍需本機短測。Foyege 原始資料保留於 [sources.md](sources.md)，本頁屬新增來源。教學中的方法整理與本技能設計的工作卡分別標示。

## T1 有動機的眨眼

Shawn Kelly，Animation Mentor，〈Blinks Revisited〉，2007 年 6 月。取得原始 newsletter 正文。作者以注意力／想法轉換、表達或隱藏情緒、快速轉頭討論眨眼時機，反對固定每兩秒一次。採用為角色動畫設計線索，具體頻率由角色與場景決定。原文部分情緒解讀屬作者表演經驗，技能只用於虛構角色導演設定。[原文](https://newsletters.animationmentor.com/newsletter/0607/feature_geek.html)

落地至 [microacting.md](microacting.md) 的眨眼目的與視線停留。2019 年重刊頁兩次取得逾時，因此以可讀原始頁為本次證據。

## T2 臉部表演與處理停頓

Dana Boadway-Masson，Animation Mentor，〈Facial Animation 101〉，2016-09-02。教材把刺激、反應前的處理時間、臉部姿態、身體後續動作分開，並要求從最終攝影機檢查眼線。採用為反應節拍及鏡頭可讀性檢查。臉先身後是可選的表演安排，依具體動作調整。[原文](https://www.animationmentor.com/blog/facial-animation-101/)

落地至 [microacting.md](microacting.md) 的處理停頓、近景節奏與實拍參考。其 Maya 操作與英文語音示例需依本機工具及實際音軌適配。

## T3 Runway Gen-4 提示詞

Runway 官方〈Gen-4 Video Prompting Guide〉。指南建議從簡潔動作開始，逐次增加變化，圖生影片讓輸入圖承擔外觀，Gen-4 採正向描述。採用其動作可見性與單變量迭代方法。正向限定與該頁時長屬 Gen-4 適配資訊。[原文](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide)

落地至 [production.md](production.md) 的模型編譯。參考這份教學不要求訂閱或上傳至 Runway。

## T4 LTX-2.3 提示詞

LTX 官方〈LTX-2.3 Prompt Guide〉，2026-03-10。該版鼓勵與時長相稱的具體敘述、可見身體線索與分段對話，同時提醒避免過載與矛盾。I2V 側重首圖之後的動作。採用為本機 LTX-2.3 的候選提示詞結構；上游主張的遵循度仍待實測。[原文](https://ltx.io/blog/ltx-2-3-prompt-guide)

落地至 [production.md](production.md)。保留完整但精簡的因果鏈。該版本教學與新版 LTX 文件分開，節點實際提供的輸入能力優先。

## T5 Wan Animate 2

Comfy Org，〈Wan Animate 2 is now available in ComfyUI〉，2026-08-08。文件說明直接讀取驅動影片、角色參考圖、視角文字控制，以及 `WanAnimate2ToVideo` 與選配 `WanAnimate2Cache`。本機有同名節點的工作流及蒸餾量化權重，可列為表演轉移候選。速度、記憶體與身份品質皆需按本機設定驗證。[原文](https://blog.comfy.org/p/wan-animate-2-is-now-available-in)

落地至 [本機路由](local-resources.md)。同頁的 Lite 與快取效能宣稱分別對待，本機蒸餾檔名不構成 Lite 即時執行能力證據。

## T6 Wan2.2 Animate

ComfyUI 官方舊版 native workflow 教學。採用其角色圖、驅動影片、姿態／臉部控制及 Mix／Move 輸入分工說明。此頁對應 Wan2.2 Animate 節點與權重，與本機 Wan Animate 2 直接影片路線分流。[原文](https://docs.comfy.org/tutorials/video/wan/wan2-2-animate)

落地至版本辨識與前處理檢查。只有使用對應舊工作流時才套用該頁的分辨率與延長規則。

## T7 LivePortrait

KlingAIResearch／LivePortrait 官方 README，原 KwaiVGI 連結現轉址至此。文件列出來源影像／影片、驅動影片、裁切及眼嘴重定向相關入口。其驅動素材建議聚焦頭部、減少肩部移動，起始採正面中性表情。採用於近景表演參考準備與候選工具能力辨識。[原文](https://github.com/KlingAIResearch/LivePortrait)

落地至本機路由與實拍參考卡。已下載原始碼的環境、權重和節點可用狀態另查。本文沒有執行作者示例。

## T8 聲畫錯位剪接

Adobe 官方〈Add J cuts and L cuts to your filmmaking toolkit〉。J-cut 讓下一鏡聲音先進入，L-cut 讓前一鏡聲音延續到下一畫面，適合對話與反應鏡頭。採用聲畫分軌及反應保留的方法，可在本機既有剪輯工具實作。[原文](https://www.adobe.com/creativecloud/video/post-production/cuts-in-film/l-and-j-cut.html)

落地至 [production.md](production.md) 的接鏡卡。剪接餘量及 C1 的示例為本技能延伸，不是教材的固定秒數或案例。


## 2026-11-07 追加研究

以下讀取第一方文章的相關正文／文字稿；未完整觀看內嵌影片或聽完節目，沒有新增本機推論證據。

### T9 目光切換與局部錯峰

Natasha Krinsky／Animation Mentor，2025-09-22，〈How to Animate Blinks and Eye Movements for Subtlety〉。閱讀眼動、眨眼及分層動作段。採用有目的的視線切換與局部錯峰；依角色及參考表演調整。[原文](https://www.animationmentor.com/blog/tutorial-animate-blinks-eye-movement/)

教材的影格數與情緒示例不作通用規則。持續注視可以成立，不為增加活力而自動添加眼球抖動、眨眼或瞳孔變化。落地至 [目光與情緒承接](microacting.md#目光與情緒承接)。

### T10 重量、阻力與接觸

Natasha Krinsky／Animation Mentor，2026-01-08，〈How to Animate Sword Fights and Battle Sequences〉。閱讀重量、spacing、接觸與 polish 段。採用物件阻力、動作速度變化與握持接觸檢查。落地為一般持物與受力驗收，未採用該文的具體戰鬥示範。[原文](https://www.animationmentor.com/blog/tutorial-animate-sword-fights-battle-sequences/)

### T11 剪接注意力落點

Jonny Elwyn／Frame.io，2022-10-03，2023-12-14 更新。閱讀〈7 Simple, Yet Powerful, Video Editing Tricks〉的 Cross dissolve 段。採用暫時疊合切點兩側畫面，檢查觀眾注意力落點；檢查後移除疊合。實際剪法仍依故事選擇。[原文](https://blog.frame.io/2022/10/03/7-simple-video-editing-tricks/)

落地至 [注意力與受力檢查](production.md#注意力與受力檢查)。這是觀眾看畫面的落點，與角色看向何物的眼線分開。

### T12 情緒距離與可演行動

John August、Craig Mazin，Scriptnotes 624 文字稿，2024-01-30。閱讀 POV 與 Emotional States 段，採用當下觀眾視角、情緒起因及距刺激的時間、可演行動。具體卡片由本技能設計。[原文](https://johnaugust.com/2024/scriptnotes-episode-624-creating-empathy-for-your-characters-transcript)

### T13 動作場景的空間與人物

John August、Christina Hodson，Scriptnotes 680 文字稿，2025-03-24。閱讀 action set piece 討論的空間、人物經驗及稿件用途段。採用必要空間資訊與人物選擇；細節程度依劇本或製作交接需求配置。[原文](https://johnaugust.com/2025/scriptnotes-episode-680-writing-action-set-pieces-transcript)

### 未採用項目

本次 Foyege24 搜尋另見第三方轉貼線索，未取得新的作者原文，不列為新增作者方法。既有 S1–S11 仍是核心來源。Blender 4.5 手冊正文取得 402、官方 staging 原始文件取得 403，沒有據搜尋摘要新增插值或 rig 操作規則。Pixar 舊論文連結轉至技術首頁，未據此採用論文結論。

## 方法整合與差異

- 表演先寫刺激與變化，再選本機能承載的控制方式。攝影機需要看見重要細節。
- 同一份導演卡可產生不同長度的模型提示詞。Gen-4 與 LTX-2.3 的建議依版本分開保留。
- 頭像驅動、全身表演轉移、姿態控制與白模預演各自處理不同資訊。先指定每個輸入的責任，再檢查衝突。
- 教學品質、已下載檔案、本機推論成功與觀眾能讀懂表演，分屬不同證據。

本次 Blender 線上手冊頁存取失敗，未將該頁列為新教材依據。Blender 使用沿用現有技能、已驗證代理腳本與實際資產能力。後續新增教學保留作者、網址、閱讀／觀看範圍、適用版本、採用規則和測試結果，避免將宣傳展示當成本機品質測試。

## 2026-11-09 追加研究

### T14 觀眾資訊與延遲

John August、Craig Mazin，Scriptnotes 632，2024-04-01 文字稿。閱讀懸疑／期待、觀眾與角色資訊差、因果延遲及釋放段。採用可追溯的知情時機與延遲理由；節目中的類型示例、幕位置及個人偏好不作每片硬規則。未聽完整節目。[文字稿](https://johnaugust.com/2024/scriptnotes-episode-632-mystery-and-suspense-transcript)

### T15 覆蓋與補拍接點

ScreenSkills 開發的 UK National Occupational Standard `SKSC32`，2020 核准、版本 3，查閱頁面標示 Current。閱讀 performance criteria 6–15 與相關 knowledge：動作／對話／機位的計時、補拍重疊動作、必要內容覆蓋、眼線與速度匹配。將片場場記責任適配為生成 take 的事件覆蓋與補鏡檢查，不要求虛擬拍攝照搬整套劇組職位。[標準正文](https://www.ukstandards.org.uk/en/nos-finder/SKSC32/monitor-script-coverage,-continuity-and-technical-camera-details-during-shooting)

### T16 同框注意力交棒

Animation Mentor，2026-10-06，Nathaniel Seymour 的角色 staging 教材。閱讀正文的主要讀點、陪襯減少動作、剪影與最終相機檢查，以及 stepped／spline 節奏差異。採用注意力交棒與姿態可讀性，不複製其角色、笑料、Maya 參數或肢體控制設定；內嵌影片未連續觀看。[原文](https://www.animationmentor.com/blog/tutorial-use-character-staging-to-guide-viewer-focus/)

### T17 視點、聲音與景深

Columbia Film Language Glossary。閱讀 [POV](https://filmglossary.ccnmtl.columbia.edu/term/point-of-view/)、[Diegetic Sound](https://filmglossary.ccnmtl.columbia.edu/term/diegetic-sound/) 與 [Depth of Field](https://filmglossary.ccnmtl.columbia.edu/term/depth-of-field/) 的定義正文。採用角色主觀鏡頭、故事內聲音與清晰範圍的區分，落地為機位／接收者／焦點欄位。各頁電影片段未在本輪播放；未由術語頁推定器材、鏡頭焦距或角色心理。

### T18 色彩處理歷史

ACES 官方 [系統概覽](https://docs.acescentral.com/background/overview/) 與 [AMF implementation guide](https://docs.acescentral.com/amf/guides/implementation/)。閱讀 transform 分工、色彩處理歷史及 applied attribute 段。採用記錄已套用／待套用變換、避免重複套用的交接思路。這不是將本機專案改成 ACES 的部署指令；生成媒體未知編碼時不猜 Log、相機 IDT 或 ACES 空間，也不宣稱本機支援 AMF。

上述文件於 2026-11-09 核對。新增工作卡與原創案例是本技能整合，見 [場景覆蓋](scene-coverage.md) 及 [質感檢查](production.md#外觀質感與觀看條件)。

## 2026-11-09 第二輪表演研究

本輪補充四篇非 GitHub 第一方文章。讀取下列正文，未播放內嵌講課影片；來源原理與本技能的原創工作卡分開。與既有 T1／T9 重複的眨眼教學只作交叉核對，不列新增來源。

### T19 表情基準中的發音

AnimSchool，Scott McWhinnie 的〈The Basics of Facial Animation〉，2024-06-26。閱讀 Speed 下的 Eyes and Lids、Brows、Mouth 段；採用各分區可有不同動態、在表情傾向中處理發音的思路。文中影格數及示例不作跨 fps、語言、rig 或生成模型的固定參數。[正文](https://blog.animschool.edu/2024/06/26/the-basics-of-facial-animation/)

### T20 表演參考的選取與分析

AnimSchool，〈Reference Analysis: Capture Convincing Footage〉，網址日期 2025-07-25。正文整理講師 Scott McWhinnie 分析 Jeff Gabor 參考的方式。閱讀機位、道具、逐次回看與轉譯段，採用有目的的參考取捨；風格化改編仍需資產與成片驗證，不把手工動畫的演示轉成模型能力保證。[正文](https://blog.animschool.edu/2025/07/25/reference-analysis-capture-convincing-footage/)

### T21 從潛台詞到可演策略

New York Film Academy，〈The Importance Of Subtext For Actors〉，2016-03-25。閱讀 What is Subtext、Finding the Meaning、Examples 與結語，採用目的、阻力與策略來解讀台詞。將不確定解讀保留為創作選擇，工作卡與新例子由本技能設計；不使用原文的對話例。[正文](https://www.nyfa.edu/student-resources/the-importance-of-subtext-for-actors/)

### T22 以表演目的檢查覆蓋

Sundance Institute，Jessica Herndon 訪問 Affonso Gonçalves，2026-07-30。閱讀文章引言與「Is there a piece of advice…」問答，採用拍攝／生成前確認鏡頭要取得的反應、行動或話語效果。本文未把訪談延伸為固定剪接秒數或每句切反應鏡的規範。[訪談](https://www.sundance.org/blogs/affonso-goncalves-on-bringing-an-editors-eye-to-the-sundance-institute-directors-lab/)

落地至 [表演參考、發音與剪接選擇](performance-transfer.md)，由微表演與話輪頁按需引入。沒有新增平台依賴或本機生成品質主張。

## 2026-11-09 KakuDrop 案例適配

### T23 多視角表演與 AI 轉譯案例

[Kaku Drop 原貼文](https://x.com/KakuDrop/status/2118736576876531790/video/1) 由公開 yt-dlp description 取得：作者自述 4DGS × AI、15 台相機拍攝上半身、最後 Seedance 2.5 輸出；提及 Codex 協助資料管理，但未提供腳本。這些屬製作者主張，不是由成片驗出的管線。

本次取樣檢視約 11.7 秒成片：全片每 0.5 秒共 24 張；1.5–2.7 秒每 0.1 秒共 13 張；5.8–6.5 秒每 0.1 秒共 8 張，另看 Video Watch 四張及 REA 聯絡表，重疊時間不重複計覆蓋。可見推近、拉遠、側背視角、笑、單眼閉合與鼓腮，以及盤腿全身。沒有連續順播、ASR 或聽音，外部 VLM 關閉；不能驗證原始表演保留率、聲畫卡點或隱藏切點。

另讀 [4D-GS 作者頁](https://guanjunwu.github.io/4dgs/) 的動態表示與新視角說明，及 [MetaHuman 官方表演頁](https://www.metahuman.com/animate) 的臉部捕捉／rig 能力。兩者只作概念辨識，不證明本案例使用該篇 4D-GS、MetaHuman，或本機已有相同部署；不採用其效能宣稱。

採用的是本技能原創的「捕捉範圍、表演與機位分軌、各層事件對齊、最終 take 承接」工作卡，見 [分開驗收](performance-transfer.md#表演機位與生成分開驗收)。不將十五相機、4DGS 或 Seedance 設成依賴，也不把大表情展示等同克制微反應。沒有原始多機片、重建工程、生成輸入及提示詞，相關欄位維持未知。

## 2026-11-09 製作周邊研究

以下六組第一方正文於本日閱讀。採用範圍是素材、剪輯交接、聲音、字幕與交付，不改 Foyege 的人物目的、微表演或分鏡核心。工作卡由本技能設計，各平台規格只適用相應交付。

### T24 素材匯入與剪輯代理

Adobe Premiere 官方〈Ingest and Proxy workflow〉，頁面更新 2026-01-07。閱讀 ingest、proxy 及 unsupported features：保留原始素材、用工作副本改善剪輯、重新連回完整品質來源。採用身份映射與回連檢查，不要求安裝 Premiere，也不把其跨應用限制泛化成所有剪輯器的能力。[正文](https://helpx.adobe.com/premiere/desktop/organize-media/ingest-proxy-workflow/ingest-and-proxy-workflow.html)

### T25 時間線交換的能力邊界

OpenTimelineIO 官方 latest 文件，頁面標示 0.19.0.dev1。閱讀 [Adapters](https://opentimelineio.readthedocs.io/en/latest/tutorials/adapters.html) 及 [Feature Matrix](https://opentimelineio.readthedocs.io/en/latest/tutorials/feature-matrix.html)。採用先查 adapter／格式支援、以代表性片段驗證的思路，不假定效果、變速、轉場可完整往返。這不是本機 OTIO／插件已安裝的證據，亦未依開發版表格承諾任何剪輯器組合。

### T26 響度與真峰值

EBU R 128-2023，2023 年 11 月、V5。[PDF](https://tech.ebu.ch/docs/r/r128.pdf) 正文第 3–4 頁涉及節目整體量測、−23 LUFS、線性製作端 −1 dBTP、平台脈絡及短於一分鐘不建議以 LRA 描述的限制。採用先指定規格再量測，不把廣播目標當所有 MV 的預設，也不自動正規化鎖定主檔。未把規範中的量測容差轉成創作品質分數。

### T27 繁中字幕的交付脈絡

Netflix Partner Help〈Chinese (Traditional) Timed Text Style Guide〉。閱讀 I.1、I.10、I.14、I.16、I.18 及 II.1–4：一般字幕、SDH、成人與兒童的規格有差異，需匹配實際音軌。採用語言／版本與交付類型的區分；一般字幕 16 字／行、成人 9 字／秒僅作該平台例，不套到所有創作或歌詞。[正文](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215994807-Chinese-Traditional-Timed-Text-Style-Guide)

### T28 字幕準確性與可及性

W3C WAI〈Captions/Subtitles〉。閱讀定義、自動字幕不足、檔案與樣式段。採用字幕內容、必要非語言聲音、同步與人工校對，以及播放器呈現需實測。未觀看頁內示例影片，也不由本次文字檢查宣稱已符合整套 WCAG。[正文](https://www.w3.org/WAI/media/av/captions/)

### T29 YouTube 上傳規格

YouTube 官方〈Recommended upload encoding settings〉。閱讀容器、視音編碼、frame rate、畫幅及 SDR 色彩段。採用以平台交付 profile 核對、保留母版的思路；具體編碼候選按 SDR／HDR 與成片需求處理，不由該頁推定來源色彩或新增影格。[正文](https://support.google.com/youtube/answer/1722171?hl=en)

FFmpeg 官方網頁兩個入口逾時，未據搜尋摘要增加參數。另實查本機 ffprobe CLI 的 JSON／format／streams／frames 選項及 ffmpeg ebur128 的 true peak 選項；相關命令只是本機量測入口，不是表演、聲音可懂度或播放器驗收證據。新增內容見 [素材與成片交接](media-handoff.md)。

## 2026-11-09 專案維護研究

### T30 數位影片保存

美國國會圖書館〈Keeping Personal Digital Video〉。閱讀正文開頭的品質與描述資訊建議：保存最高品質版本及可理解的描述，不把網路發布副本當成唯一原始資產。由本技能延伸到工程、音軌、字幕與生成依賴的封存清單；沒有在本次遷移真實資產或建立定期任務。[正文](https://digitalpreservation.gov/personalarchiving/video.html)

### T31 校驗與完整性

Digital Preservation Coalition，Digital Preservation Handbook〈Fixity and checksums〉。閱讀 fixity、checksums 及 application 段：建立已知正確的校驗基線、檢查不同副本、合法格式遷移後建立新基線。採用保留版本與恢復驗證的方法，不把一致 hash 當作內容正確或獨立備份證明；未觀看內嵌影片，檢查頻率依實際系統安排。[正文](https://www.dpconline.org/handbook/technical-solutions-and-tools/fixity-and-checksums)

### T32 素材來源與署名

Creative Commons 官方〈Reusing CC-Licensed Content〉。閱讀 CC attribution、TASL 及 public domain 段，採用標題（有提供時）、作者／指定署名、原始來源與實際授權版本的紀錄。CC0／Public Domain Mark 的脈絡另分；不把 TASL 表格當作新增授權，不由參考影片公開可見推定可重用全部內容。[正文](https://creativecommons.org/reusing-cc-licensed-content/)

### T33 共享專案與寫入責任

Adobe Premiere 官方〈Collaborate efficiently with Productions〉。閱讀多工程組織、media referencing、Designed for collaboration 及 local storage 段。採用明確工程寫入責任與版本交回；project locking 只是 Premiere 的具體機制，不當成所有工具、二進位工程或 NAS 同步的共同能力，也不改既有帳號權限。[正文](https://helpx.adobe.com/premiere/desktop/collaborate-with-others/collaborate-using-productions/about-productions.html)

以上四份於 2026-11-09 讀取相關正文。Blender latest packed-data 手冊取得 402，未據舊版搜尋摘要新增「已打包全部依賴」或特定打包功能的規則。原創封存、用途與改稿工作卡見 [project-stewardship.md](project-stewardship.md)；它是按需製作支援，不改 Foyege 核心。

## 2026-11-09 運鏡研究

### T34 相機移動與變焦

Columbia Film Language Glossary。閱讀 Camera Movement 的定義及 Today、Pan Shot 定義、Zoom Shot 定義及 dolly zoom 段，區分實際移動、固定機位轉向與焦距變化。未連續觀看內嵌電影片段；不採用器材比較作本機模型能力證據。[Camera Movement](https://filmglossary.ccnmtl.columbia.edu/term/camera-movement/) · [Pan](https://filmglossary.ccnmtl.columbia.edu/term/pan-shot/) · [Zoom](https://filmglossary.ccnmtl.columbia.edu/term/zoom-shot/)

### T35 攝影師的運鏡選擇

M. David Mullen, ASC，StudentFilmmakers〈Notes on Camera Movement: When to Move the Camera and Why〉。閱讀 motivation、兩部作品案例、A Common Mistake、Other Reasons、Dolly Moves Add Dimension 段。採用敘事／情緒／空間目的與剪輯落點，不把作者個人焦距偏好或器材經驗定成所有媒材規則。[作者署名正文](https://studentfilmmakers.com/notes-on-camera-movement-when-to-move-the-camera-and-why-by-m-david-mullen-asc/)

### T36 移動後停步與反應

The Film Look，2018-06-26〈Coming to a Halt | Motivated Camera Moves〉。閱讀角色與相機同時落點、廣景行動轉近景反應、固定人物／相機變體及穩定器／手持段。採用變化與落點的思考，不複製其追逐場景或書籍內容；未連續觀看影片或 GIF。[作者教學正文](https://www.thefilmlook.com/thefilmlook-video/coming-to-a-halt-motivated-camera-moves)

### T37 靜止搖攝與跟拍

ACMI〈Exploring camera movement〉。閱讀 introduction、Static、Panning、Tilting、Tracking 段，採用靜止也是選擇、搖攝揭露與跟拍焦點的區分。未播放頁內示例，不把平順運動當成所有風格的必要條件。[博物館教學](https://www.acmi.net.au/education/school-program-and-resources/exploring-camera-movement/)

以上四組於 2026-11-09 查閱相關正文。新增 [運鏡與表情](camera-movement.md) 為原創選擇卡與本機適配。Blender 5.2／5.0 Follow Path、latest cameras／F-Curve 及 current API 網頁入口取得 402 或無法存取，未把搜尋摘要當作已讀手冊；本機另用 Blender 5.2.3 的投影與依賴圖實測核對距離／焦距及路徑／目標分離。這不是渲染、速度曲線或生成影片品質證據。
