# HyperFlow H3 Flash：按執行路線編譯導演卡

只在選用 Flash、評估壓縮模型或分析相關教學時閱讀。它是補充執行路線；微表演、空間與接鏡仍沿用 Foyege 方法。這輪只查教學、原始碼與靜態工作流，未在本機推論。

## 先辨認是哪一條 H3

Flash 是剪枝、低秩及雙時間條件的獨立模型，不能只把完整 H3 的步數調低或掛原 HyperFlow LoRA 當成同一配方。`fl2va` 權重用於文字、首圖、首尾圖；`ref2va` 權重用於參考生成，兩者不可互換。已有 H3 編碼器／VAE 可先核對後重用，主模型和 loader 仍需配對。

記錄桌面客戶端、ComfyUI 核心、節點包與權重各自版本；教學中的桌面版號不能直接當核心版本。釘選的官方節點要求核心原生 H3 支援（0.43.0+），新版官方 loader 同時支援 GGUF／INT8；影片中的社群 INT8 包不是所有新版配置的必要依賴。

## 參考責任與提示詞

- ComfyUI Flash 的已文件化 ref2v 路線是圖片參考，圖序對應 `<Picture 1>` 等標記。Python INT8 的混合影音參考另查該 runtime；核心節點出現音訊槽，不足以證明每種 Flash 後端都支援。
- 每圖綁定「角色身份／服裝、場景、道具」責任；多圖不是多個起始或終止幀。需要指定終態時評估首尾幀路線，仍檢查中間接觸與受力。
- 單一主提示詞寫場景、動作、機位及聲音；此配方沒有獨立負面提示。將必要保持狀態寫成正向可見描述。下例是本專案原創、未生成的測試稿，需先綁定兩張真實參考：

```text
Close-up of <Picture 1> in the room of <Picture 2>.
She notices the offscreen monitor; her gaze shifts toward it while her head stays still.
Her lips part briefly, then close. A small tension remains at one mouth corner.
The camera stays at eye level and holds the close-up through her settling reaction.
Soft room ambience accompanies the shot.
```

導演卡另保留刺激、起終態、檢查區間與切鏡餘量。文字中的眼先頭後是測試目標，不是逐幀控制；若精準順序失敗，回到已驗證驅動／動畫或拆鏡方法，不以加長提示詞代替控制能力。

## 配方與資源邊界

釘選官方模板採 HyperFlow Sigmas 的 4／6／8 步、Euler、BasicGuider（無 CFG 分支，等效 CFG=1），預設 6 步。24fps、`17n+5` 格、寬高為 32 倍數；文件訓練範圍約 124–362 格。以實際對齊後格數／24 算時長，不能把 UI 接受更長數值當成已驗證長鏡。

`ref_image_size=match` 按輸出面積縮小參考；`max` 保留更高參考解析度但增加 token、時間與顯存壓力。比較速度或身份時記錄此項、圖數、輸出尺寸及載入時間，不能把縮小參考造成的加速全部歸給模型。

9GB 左右的 GGUF 是磁碟權重大小，不是全流程顯存需求；文字編碼、VAE、參考與激活也佔記憶體。釘選上游只量過 24／32GB 顯卡，明列 16GB GPU 尚未量測；16GB **系統 RAM** 的展示不能當成 16GB **VRAM** 成功。新卡先列候選及缺件，不承諾可用或速度。GPU 忙碌時做文件準備，不啟動模型、不因忙碌轉 CPU。

## 速度、表演與聲音分開驗收

先用同一版素材和可比較設定測「一次視線轉移→嘴角恢復→保持段」，再測雙人參考／一次接觸，最後才加入雙人對白。每階段記成功、失敗與未檢查；需要比較 4／6／8 步時一次只改步數，沿用授權候選上限。壓縮模型的快速出片不證明眼球、身份或聽者反應已過關。

為生成段分開標記嘴部話輪、眼神、姿勢／傷痕、切點、台詞與聲線。生成器可能自行切鏡；若工單要單鏡連續，就依輸出實際切點驗收，不能只看起終格。

原生音訊是候選素材；人聲內容、說話者、對嘴、聲線和接縫需要原速視聽。瞳 MV 已鎖定的歌曲不得被同步生成音訊替換；音畫共同生成不等於外部主音軌精準對嘴，另依可用音訊控制路線製作與剪輯。

## 來源與採用範圍

- 零度解說 [10:09 教學](https://www.youtube.com/watch?v=n6MeunOm980)：閱讀全段 YouTube 自動字幕，查看分散靜幀及 08:48–08:53、09:28–09:45 加密樣本。字幕會將 H3 誤寫成 2.3；未做獨立音訊聽審。作者於 08:58 自述 24GB，09:44 自述聲音有問題；不是本機效能或音質證據。
- [Flash 原始碼／規格](https://github.com/Video-Rebirth/hyperflow-h3-flash/tree/703747ee414f895985a4c3b87e59f4fd03fc9f14)：閱讀 README 的架構、runtime、資源與 benchmark 條件，以及 integrations 的輸入／配方；資料為上游主張。
- [官方節點／API 模板](https://github.com/Video-Rebirth/ComfyUI-HyperFlow-Flash/tree/c807a89653569531b5c61ef691060acf467c552c)：閱讀 loader、schema、README 及八份 API 工作流；未在本機載入該節點。程式與權重授權分開核對，模型權重不是無限制開源素材。
