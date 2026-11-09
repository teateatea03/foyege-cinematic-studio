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
