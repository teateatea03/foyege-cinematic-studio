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

## 方法整合與差異

- 表演先寫刺激與變化，再選本機能承載的控制方式。攝影機需要看見重要細節。
- 同一份導演卡可產生不同長度的模型提示詞。Gen-4 與 LTX-2.3 的建議依版本分開保留。
- 頭像驅動、全身表演轉移、姿態控制與白模預演各自處理不同資訊。先指定每個輸入的責任，再檢查衝突。
- 教學品質、已下載檔案、本機推論成功與觀眾能讀懂表演，分屬不同證據。

本次 Blender 線上手冊頁存取失敗，未將該頁列為新教材依據。Blender 使用沿用現有技能、已驗證代理腳本與實際資產能力。後續新增教學保留作者、網址、閱讀／觀看範圍、適用版本、採用規則和測試結果，避免將宣傳展示當成本機品質測試。
