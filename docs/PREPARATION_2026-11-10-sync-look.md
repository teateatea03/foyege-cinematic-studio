# 聲畫對齊與跨鏡光色：實驗前準備

2026-11-10。依「先做，有空再實驗」完成技能與工具準備；本輪不啟動媒體／GPU／模型試驗，不查空閒後自動排隊，也不啟停其他工作。

## 完成內容

[操作與案例](../skills/foyege-cinematic-direction/references/sync-and-look.md) 接回既有詞級觸發及攝影燈光交接。原有 Foyege 微表演、角色目標、空間與接鏡原則保持。

- acting_cues.py：stdlib，將明列音訊 sample frame 以 Fraction 映射到 CFR，支援裁入點及單一正音訊播放速率。預定反應、實際觀察與半開保持區間分開，可查刺激前反應、前後反應及最小間隔；不做 ASR、音訊量測、PTS 或口型分析。
- look_handoff.py：stdlib，記錄各來源解讀、共同工作／觀看／輸出基準、世界光源 ID、已烘焙／計畫 look。只核對宣告差異、未知值和重複／換版 look，不讀影像、不轉換色彩或驗證 OCIO。
- 兩份 DRAFT JSON：音軌 SHA 與光色資訊未綁定的欄位保留 null／provisional。示例數字不是正式歌詞時碼，示例輸出不冒稱 plan／成片已接受。
- 待測卡：一個清楚聲音刺激與克制反應；一組同場正反打的世界窗位、角色色與觀看條件。先保留前後副本與實際原始媒體，按操作頁逐項驗收。

## 本輪只做的檢查

13 項 stdlib 回歸測試通過，並真正以 CLI 新程序執行兩個 DRAFT 範例／拒絕覆蓋既有報告：

| 檢查 | 結果 |
|---|---|
| 第 24 格內的 sample 事件 | 回傳 exact 6003/250、所在格 24、不早於事件的邊界 25；示例維持 provisional |
| 30000/1001、裁切及 2 倍音訊速率 | Fraction 精確換算；不當成視訊變速可改鎖定母帶的許可 |
| 刺激前反應、眼頭順序 | 規劃／觀察衝突分別列出；未觀察維持 not_measured |
| 區間、無效分母／模式與前向相依 | 拒絕區間外事件、speed ramp／多餘時間映射欄及尚未定義的相依 |
| 光色未知 | 原樣保留，不猜 BT.709、Log 或 ACES |
| 同 look 跨鏡使用 | 允許；同鏡 baked＋planned 重複 SHA 則列待審 |
| 同 ID 不同 bytes、故事性換光 | 列版本差異；保留意圖理由供後續審查 |
| 報告不覆蓋 | 第二次 CLI 回非零，原輸出位元組不變 |

這是對原創程式邏輯的檢查；測試裡的「已知」光色名稱和 hash 是 fixture，不是實際配置或模型品質證據。沒有生成音訊、讀取媒體、擷取幀、跑原生 H3、調色、渲染或使用 GPU。

在專案根目錄重現：

```powershell
python -X utf8 skills/foyege-cinematic-direction/tests/test_sync_look.py
python -X utf8 skills/foyege-cinematic-direction/scripts/acting_cues.py --input skills/foyege-cinematic-direction/assets/sync-look/acting_cues.example.json --output "<new cue report.json>"
python -X utf8 skills/foyege-cinematic-direction/scripts/look_handoff.py --input skills/foyege-cinematic-direction/assets/sync-look/look_handoff.example.json --output "<new look report.json>"
```

## 同步與可攜檢查

[機讀紀錄](research/sync-look-preparation-2026-11-10.json) 保存檔案 hash 與同步範圍。Codex 只在兩份舊參考追加入口，其餘 42 舊檔不變；Claude 只改一份舊參考，其餘 40 舊檔不變，另補齊原缺的 camera-movement、crew-workflow、department-handoffs 三份公開參考。兩邊均增加本輪六檔，主入口和本機設定保留，修改前備份留存。三份 Foyege quick_validate 與參考檔存在檢查通過。

完整套件格式／連結／語法、五項安裝測試、Gitleaks 工作目錄掃描及 git diff --check 通過。這些只證明套件和原創核對工具的有限性質，不提升待測素材的資格。

## 留待有空時

| 項目 | 真正要取得的證據 |
|---|---|
| 聲畫試片 | 已接受音檔／take 身份、實際詞邊界、完整原速看聽、PTS／切點與實測反應；歌聲原版保持 |
| 光色正反打 | 真正來源標籤及解讀、實際配置／look、共同觀看條件、世界光源母本、前後畫面及表情可讀性 |
| 既有未完成項 | 真實 H3 冷恢復、真人修臉／遮擋與微表情保留，仍依上輪紀錄維持待測 |

不以填齊 JSON、plan_consistent 或 handoff_consistent 把以上待測改為通過。變更音軌、採樣率、剪輯或處理歷史後，重查受影響 cue／鏡頭；不重跑無關素材。
