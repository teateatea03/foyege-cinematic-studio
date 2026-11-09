# 聲畫節拍與跨鏡光色：準備及核對

只在要把已定表演接到音軌，或處理同組鏡頭光色交接時讀對應部分。本輪先備妥表單、原創 stdlib CLI 與待測案例，依使用者安排把實際媒體／GPU／模型實驗留待有空時。規格核對與真實視聽驗收分開。

## 聲畫：把刺激落到真正的時間基準

沿用 [詞級觸發](acting-beats.md) 與 [事件分層](performance-transfer.md#對齊事件再比較各層)。先鎖主音軌／對白版本、角色與刺激，再安排少量反應；工具不決定演法，不要求每鏡都做眼先頭後。

1. 從已接受音檔取得 sample rate、起點與 SHA256。source_sample 是每聲道共用時間的 **sample frame 編號**，不是 bytes，也不乘聲道數。
2. ASR／詞對齊只供定位；用原速聽辨字音、尾音、呼吸與停頓，校好實際刺激點。沒有音檔就保留 provisional，不能從歌詞猜精確落秒。
3. 用 [acting_cues.example.json](../assets/sync-look/acting_cues.example.json) 綁音軌與時間線。示例 48024、25、29、34 等數字是算術範例，不是瞳正式歌的時碼或通用反應延遲。
4. 分開 planned_frame 和 observed_frame。observed_frame 只有真的看過對應 take 才填；音軌 hash 也是呼叫者聲明，CLI 不讀媒體。需要檔案身份核對可另用既有 [來源 guard](finishing-tools.md#1-把一次完成工作綁定到來源)。

### 可直接執行

在技能根目錄執行（Python 3.10+，無額外套件）：

```powershell
python -X utf8 scripts/acting_cues.py --input "<current cue specification.json>" --output "<new cue report.json>"
```

支援模式是 constant_audio_rate_cfr：整數幀、正有理數 fps 與單一正音訊速率。時間線欄位必須是範例明列的六項，不接受 VFR、倒放或 speed ramp；此時改用剪輯器／實測 PTS 和分段映射，不硬套平均 fps。

```text
exact timeline frame =
start_frame + (source_sample - audio_in_sample) / sample_rate × fps / audio_playback_rate
```

audio_playback_rate 只指這條音軌的播放速率。MV 主音軌鎖定時保持 1/1；只把畫面慢放不能順手改這個值。需受保護的唱法、詞句與歌曲長度沿用原版本。

CLI 用 Fraction 避免長片及 30000/1001 的浮點累積誤差；事件回報所在格 floor 與「第一個不早於事件的影格邊界」ceil。當事件落在第 24 格內，ceil 可能是 25；這是保守邊界慣例，不宣稱人類知覺一定要求多等一格，也不自動改動你的剪法。

- start_frame 是零基、含起點；整段及保持區間都是 [start,end) 半開區間。hold_end_frame 是不含的結束邊界。
- 反應不得無因地早於它宣稱的觸發。若人物預判、觀眾先知或有更早刺激，把真正原因列成事件，不為求通過任意把語詞 cue 往前挪。
- after_reaction 可引用前一筆已列的反應，min_gap_frames 是當鏡自行決定的最小間隔。可核對「眼先、頭後」或「嘴角收回後保持」的**宣告**；不保證模型做到。
- 剪短、重錄、重採樣、換主音軌或改音訊速率後，重定位 sample、重算相關 cue。只換相機也需重查必要表情在當鏡是否可見。
- 無 SHA／provisional 事件會維持 provisional；全部資訊已填且未見順序問題，只回 plan_consistent。content_acceptance 永遠不因算式通過而提升。
- 時序衝突回 needs_review／退出碼 1；無效規格或輸出已存在回 2；正常報告回 0。缺觀察不冒稱影片通過，既有報告不覆蓋。

### 待有空時的聲畫試片

用自有或已授權的短對白／鎖定歌曲原段，選一個真的能聽出的刺激。綁真實 SHA、詞邊界與一個克制反應，保留原主音軌；先檢查原生 take，再檢查剪輯輸出。

待驗：眼神是否真的在刺激後改變、頭與嘴角的順序、發音有無衝突、保持是否可讀；在開頭／中段／尾端與切點查偏移。若口型或動作已有錯，不靠改 cue 報告把它變成通過。反應時間碼來自觀看測量，ASR 不能量出嘴角或眼神。

## 光色：共用基準，逐鏡記處理歷史

沿用 [攝影燈光與外觀基準](department-handoffs.md#攝影燈光與外觀基準)。相鄰鏡頭先綁同一世界光源、LOOK／角色材質與觀看條件，再比較；反打不等於把窗光搬到另一面。

用 [look_handoff.example.json](../assets/sync-look/look_handoff.example.json) 為同一光況／look group 建基準：

| 欄位 | 負責什麼 |
|---|---|
| world_light_id／母本說明 | 指向同一場景世界光源與事件；ID 相同不是光向／曝光已實測 |
| 每鏡 input_color | 已知 primaries／transfer／matrix／range；不明用 JSON null |
| input_transform | 各來源如何進工作空間；不同來源可不同，不強迫輸入標籤一樣 |
| working_space／color_config_sha256 | 真正工作空間、OCIO 或相應配置版本；名稱相同不代替實檔核對 |
| view_transform／display | 真正看片條件，與創作 look、輸出標籤分開 |
| output_color | 交回規格；寫入標籤不是已完成像素色彩轉換 |
| baked_looks／planned_looks | 已烘焙與計畫套用的創作 look，逐項 ID／實檔 SHA，不混作顯示 LUT |

```powershell
python -X utf8 scripts/look_handoff.py --input "<current look handoff.json>" --output "<new look report.json>"
```

此 CLI **只核對聲明**，不讀影像、不調色、不套 LUT，也不驗 OCIO 設定有效性。已知輸出／工作／觀看／光源宣告與基準不同會列差異；input_color 按各鏡保存，不把合理的混合來源當成錯誤。

同一鏡的 baked 與 planned 若含同 SHA 或重複 look ID，列待審；同 ID 換了內容另列版本疑點。相同 look 用於不同鏡是正常。跨檔位元組不同但效果等價的 LUT，工具無法辨識；同 SHA 也不能證明處理真的有套用。

故事需要燈光事件、夢境或舞台變色時，保留 intentional_changes 的具體理由，差異仍供審查；不同設計可另立 look group，不強制全片同色。null 保留 needs_binding；宣告一致只回 handoff_consistent，最終外觀仍未驗。無效規格／覆蓋輸出回 2，待審差異回 1，其餘報告回 0。

### 待有空時的光色比較

選同一場景兩個不同機位，鎖世界窗位與 LOOK／服裝版本。先核對原片、實際來源標籤、配置檔與 look 歷史；未知來源不能直接改標 Log、HDR、ACES 或 BT.709。

在同一顯示／view 下順播原片及處理副本，檢查膚色／角色主色、眼睛與嘴角的可讀性、主光方向、背景和高光、服裝材質。量測用穩定且有意義的區域；整張直方圖受構圖影響，不以數值接近當作匹配成功。不要把深膚色、陰影或刻意舞台變光自動拉成同一亮度。

先試一組正反打並保留處理前後副本；失敗回查光源／來源解讀／look 是否重複，再決定調色或重做。顏色更一致卻抹掉嘴角張力或暗部眼神，仍不接受。參數、色卡、顯示與實際看片證據分別記錄。

## 本輪完成與留待實驗

本輪只驗原創 CLI 的算術、JSON 結構、差異回報及不覆蓋行為；未讀取音訊／影片、對齊真人、跑模型、改像素、生成／渲染或使用 GPU。實際聽辨、PTS、口型、表情、色彩管理與跨鏡外觀均列待測。沒有新增下載、環境升級、常駐服務或自動排程。

方法沿用既有 Foyege 表演／事件原則與 [光色交接](department-handoffs.md)，沒有新增第三方模型依賴；[準備紀錄](https://github.com/teateatea03/foyege-cinematic-studio/blob/main/docs/PREPARATION_2026-11-10-sync-look.md) 列實際檢查範圍。
