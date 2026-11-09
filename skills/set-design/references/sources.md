# 來源

2026-11-07 查的。「讀過全文」是我把整頁或整個檔案讀完；「只看過摘要」是只看到搜尋結果的片段，沒有讀原文，只能當線索。

## 讀過全文

| 來源 | 類型 | 用在哪裡 | 限制 |
|---|---|---|---|
| filmlocal〈film floor plan〉 https://filmlocal.com/filmmaking/film-floor-plan/ | 拍片教學文章 | 平面圖的畫法：比例尺和尺寸、牆畫粗、門畫開門弧線、窗的符號、指北針、攝影機畫成圓加箭頭、立面圖標記、虛線表示頭頂上的東西、可拆的牆（wild wall）、為鏡頭和視線設計、白卡模型 | 立面標記和虛線還沒做進 `plan_check.py` |
| SketchUp 部落格：Marvel 和 Disney 美術指導用 SketchUp 做場景 https://sketchup.trimble.com/sv/blog/article/how-a-marvel-and-disney-art-director-streamlines-set-production-with-sketchup | 廠商文章（Trimble） | 一個 3D 模型當母本，平面圖、立面圖和視角圖都從同一個模型出 | 廠商推自家軟體；這裡只採用「一個模型」的做法 |
| fal.ai〈From clay 3D render to a real action short〉 https://blog.fal.ai/from-clay-3d-render-to-a-real-action-short-a-3d-to-ai-pipeline-with-total-control/ | 廠商教學 | 白模負責幾何、第一格放齊關鍵物件、一個鏡頭一件事、視線射線檢查、機位離物件 0.5 m、改圖時「第一張圖是幾何唯一依據」、裁成同比例、空間描述、風格段落逐字重複、50% 疊圖、輪廓分數、每鏡 20 到 40 張 | 廠商教學，用的是自家雲端模型；輪廓 PSNR 的門檻在範例房間裡分不出對錯，沒有採用。機位距離我改成 0.3 m 警告，因為小房間常放不下 0.5 m |
| ai-muninn〈Blender blocking to H3 Ref2VA on RTX 5090〉 https://ai-muninn.com/en/blog/blender-blocking-h3-ref2va-rtx5090 | 一位作者的實測 | 白模影片當參考、替身用膠囊和方塊加不對稱記號、解析度和格數要對齊 17k+5、守得住左右和遮擋、守不住距離和小轉身、全身遠景臉會糊、每支約 90 秒 | 只有一位作者，一張 RTX 5090；本機還沒重現 |
| curiositech/some_claude_skills 的 `interior-design-expert`（SKILL.md、references/space-planning.md、references/lighting-design.md） https://github.com/curiositech/some_claude_skills | 別人寫的 Claude 技能，MIT 授權 | 人體尺寸、走道和家具間距、照明分層、照度、各時段的燈光色溫 | 人體尺寸取高個子男性；它的版面求解器要 OR-Tools，沒有採用 |
| mlolson/blender-orchestrator（README、docs/SCENE_BUILDING_GUIDE.md） https://github.com/mlolson/blender-orchestrator | 別人寫的 Blender 工具 | 擺放順序（牆、大件、配合的、小東西、燈、機位）、用一半高度定位物件、靠牆的算法、0.9 m 走道和 0.8 m 門口、常見錯誤（浮空、比例錯）、常用家具和房間尺寸 | 沒有授權條款，所以只採用做法，沒有複製程式碼 |
| foyege-cinematic-direction 的 `scripts/build_previs.py` | 本機技能 | 白模和正交俯視圖的做法、預演的輸入格式（`to_previs.py` 照它的格式輸出） | 它的替身只會站、固定 1.6 m |

## 本專案實測

| 來源 | 用在哪裡 |
|---|---|
| T01 戳臉和握手腕測試（Issue #36 留言 `6700748567`） | 首尾圖讓接觸動作 4/4 成功；沒有場景設計時，每張首圖會各自發明一個房間 |
| 這份技能的範例房間（2026-11-07） | 腳本的時間、檢查抓得到的錯、疊圖分數的範圍、時段光的調法 |

## 只看過摘要

這些沒有讀原文，內容只當線索：

- Vectorworks〈Beginner's guide to set design〉：場景設計從平面圖、立面圖到 3D 模型的流程。
- studiomatrx 的場景設計教材（set design history、stage and space、set design and concept）。
- Fiveable〈Creating ground plans and elevations〉：舞台平面圖和立面圖的慣例。
- PremiumBeat〈What production designers do〉：美術指導的職責。
- invideo 常見問答：為什麼拍片會先用低面數的 Blender 白模。

## 我自己推的

- 站姿眼高約身高的 93%，坐姿頭頂約座面加身高的 52%、眼睛約加 45%：估計值，沒有直接出處，在 [space-planning.md](space-planning.md) 和 [set-json.md](set-json.md) 都有標。
- 天光的色溫（日出日落、中午、陰影）：一般攝影常識，不是來自上面的來源。
- `must_see` 用面上取樣、`overlay_check.py` 分垂直和水平輪廓來比：這兩個做法是我在範例房間測出問題之後改的，見 [blender-blockout.md](blender-blockout.md) 和 [ai-handoff.md](ai-handoff.md)。
