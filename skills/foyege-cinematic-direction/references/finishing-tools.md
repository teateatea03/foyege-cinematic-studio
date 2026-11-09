# 後製實作：來源核對、臉部保護與 MV 字卡

本頁供已選定後製工作的實際執行；只寫提示詞或單鏡表演時不用展開。新增腳本均為本專案原創，不安裝第三方節點、不下載權重、不啟動服務。H3 仍負責原生階段保存／恢復與合成；本工具只補核對和素材製作。

## 1. 把一次完成工作綁定到來源

使用 [finishing_job.example.json](../assets/finishing/finishing_job.example.json) 建立自己的 job。所有 artifact 路徑相對於自選工作根目錄；take ID、角色 ID、時間及審查節拍均須改成真實值。

- 原生 Full Save 成功後，列出當次 source、settings、reference、audio（有聲才列）、每角 Stage／Source manifest **及其全部 payload 檔**。工具不解析 manifest 指向的其他檔案，未列入的檔案不受保護。
- settings 須實際保存模型／節點 revision、權重 hash、提示詞、seed、步數、裁切／角色計畫、效果、時間窗及工作流。job 的時間是呼叫者聲明，工具不測媒體 PTS 或張量內容。
- 來源、模型權重可共用既有檔案；不為此複製大模型。工作根目錄要涵蓋所有明列檔案，拒絕越界或失效連結。模型 hash 若只寫在 settings，仍需自行核對目前檔案；要重新讀取實檔就把它明列為 reference。
- 僅在檔案已寫完且不再修改時凍結。多人各角 Stage／Source 分開命名；一個 job 可含多個 stage artifact。

在技能根目錄執行（Python 3.10+，stdlib）：

```powershell
python -X utf8 scripts/take_guard.py freeze --root "<work root>" --job "<job.json>" --receipt "<new receipt.json>"
python -X utf8 scripts/take_guard.py verify --root "<work root>" --job "<current job.json>" --receipt "<receipt.json>"
```

freeze 不覆蓋已存在檔案。verify 必須使用**這次想恢復的 current job**，不是為求通過而換回舊規格；job 任何位元組或明列 artifact 改變就拒絕重用。正常換工作根目錄可攜移，只要相對路徑及位元組一致。

通過只表示明列檔案相符。接著仍由原生 Stage／Source Load 驗證 schema、階段完整性及當前工具契約；本工具不反序列化、不恢復採樣、不接受 take。更換素材／配方時保留舊結果，另建版本；同一來源只改交付或可見遮罩的重用範圍由原生路線判定。

原生 67 外片續拍在固定來源版本有 Full Save／Cold Delivery 配對；其示例 124 render frames／22 context 是該配方，**不是所有專案的通用數值**。先填實際已接受 take，再明確裁上下文、檢查完整接點和原音軌。多人凍結來源及其他冷載入路線可能仍要 VAE、CLIP／MODEL 核對，勿一概當成無模型旁路。

## 2. 先限制候選影響，再驗表演

固定來源的原生 T8 節點契約：

| 節點／輸入 | 應接什麼 |
|---|---|
| H3 Face · Bind Visible MASK / source_images | 完整原片 RGB；不是臉部小裁切 |
| visible_mask | 同源、同幀、同完整幾何的可見臉 MASK；白允許已有變化，黑保留原片 |
| fps / source_start_frame | 該版只收聲明 24fps；offset 綁當次完整緩衝區 |
| broadcast_single_mask | 動態人物保持 false；固定單張遮罩須有明確幾何依據才開啟 |
| H3 Face · Visible MASK Composite / candidate_images | Stitch／Gate 已混合完成的完整候選 C |
| changed_alpha **或** multiface_composite | 二選一；前者接原 changed_mask，後者接最終多人 composite state；不是 fallback mask 或局部窗 |
| audio | 保留原音軌旁路；只測物件相同不能證明音訊內容／交付完整 |

B + (C − B) × V 不再乘一次舊 alpha。追蹤失去目標、遮擋或身份不明時回原片並列區間；若該安裝沒有這項能力，先拆鏡／人工指定可靠 ROI，不能假定其他版本的修正已存在。完整原生圖及節點可用性仍須按安裝核對。

### RGB8 PNG 交付核對

[audit_visible_face.py](../scripts/audit_visible_face.py) 需要 NumPy、Pillow。將同一**合成前後檢查點**的 B／C／V／R 匯出四個目錄，每個只放從 000000.png 起連號且數量相同的完整序列：B／C／R 為 RGB8，V 為 L8。時序不可由播放器補幀、縮放、變速或有損影片重新解碼冒充。實際 N 必須由媒體／節點另外核對，腳本只查明列序列。

```powershell
python -X utf8 scripts/audit_visible_face.py --source "<B>" --candidate "<C>" --mask "<V>" --result "<R>" --frame-count 124 --report "<new audit.json>"
```

黑區要求逐像素與 B 相同，白區與 C 相同；分數遮罩因 PNG8 量化允許 1 code value 差。每幀保存四份檔 hash、改動數及公式誤差。pixel_fail 回傳非零退出碼；拒絕錯模式、缺幀、不同幾何和覆蓋報告。這是編碼像素值核對，不證明色彩管理、原始浮點精度、PTS、音訊或遮擋語義。

若要校準**已審閱的那份原生模組**，可選執行：

```powershell
python -X utf8 tests/check_native_visible_face.py --module "<reviewed T8>/h3_t8/visible_face_mask.py" --out "<new calibration directory>"
```

此命令明確載入指定 Python 原始碼；只對已核對來源使用。12 幀 CPU 合成素材校準不載入 H3 模型、不啟動 CUDA，也不代替真實 Comfy 圖、偵測、修臉或表演試片。

像素通過後，仍需原速連看與放大對照眼神起動、頭後跟、眨眼、嘴角壓制、呼吸、口型、遮擋及接鏡。清晰度改善但反應提前，仍拒絕候選。

## 3. 瞳的系統字卡：可重現的小範例

[render_system_cards.py](../scripts/render_system_cards.py) 與 [示例時間線](../assets/finishing/system_cards.example.json) 使用既有 Pillow 直接逐格畫圖，不需要新生成模型。960×540、24fps、144 幀：啟動 → ERROR → 權限不足 → 重新啟動。這是六秒 DRAFT 包裝示例，無音軌，尚未對齊正式歌曲；不改主歌聲或分鏡正本。

```powershell
python -X utf8 scripts/render_system_cards.py --config assets/finishing/system_cards.example.json --font "<owned CJK font.ttf or .ttc>" --out "<new cards directory>"
```

字體由使用者本機提供，不隨技能散布。輸出 frames/000000.png… 及 render.json，記錄設定、字體 hash、Pillow／Python 和每幀 RGB hash。輸出目錄已存在就停止；失敗保留 INCOMPLETE 標記，未完成資料不能當成品。

時間線用整數幀及 [start,end) 半開區間，須無缺口、無重疊且覆蓋總幀數；純時間函數可任意重訪同一幀，沒有亂數或跨幀累積狀態。hold 整段保持不動，ERROR 僅畫連續移動線條，不靠隨機閃爍。要加粒子或物理狀態時，改成固定初態順序重播並另驗收。

先依正式音軌版本把 cue 改成實際幀界，綁定字形／字體與所用工具版本，再匯入剪輯器按原 fps。抽樣圖只檢查版面；完整運動、文字可讀性和聲畫觸發需另看整段。不可用「低幀差」自動刪掉刻意停格或角色克制。

## 能力與未測範圍

本輪已測來源拒絕、原生合成算式及字卡重現。H3 真實採樣／新程序冷恢復、動態真人遮擋與微表情、完整 UI 工作流和歌曲同步尚未因本頁而取得資格。GPU 忙碌時準備文件與這些小型檔案／像素檢查，留生成與渲染給當下已授權且可用的 GPU，不停止他人工作。

來源和版本沿用 [第二輪選用卡](finishing-candidates.md) 的固定連結；測試條件見 [公開實驗紀錄](https://github.com/teateatea03/foyege-cinematic-studio/blob/main/docs/experiments/2026-11-09-finishing/README.md)。
