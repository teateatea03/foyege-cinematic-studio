# T8star-Aix：其餘候選再篩選

2026-11-09。接續 [首輪頻道盤點](RESEARCH_2026-11-09-t8-channel.md) 與 [三項優先工具短測](experiments/2026-11-09-priority-crew/README.md)，重新評估後製、臉部、長鏡恢復、3D 與聲音候選。結論：優先學三種方法，暫不新增一套模型系統。可直接供製作使用的 [選用卡](../skills/foyege-cinematic-direction/references/finishing-candidates.md) 已納入 Foyege 工具路由。

## 證據範圍

沿用前 150 筆標題清單，再取得 8 支影片 metadata／說明欄，核對同一頻道 ID；由來源連結增讀 4 個固定 revision 的 README 相關段落與 requirements，並追讀既有 H3、Hi3D 和 Code-Animate 專項文件。不是全頻道窮盡調查；沒有連續觀看這批教學、音訊聽辨或新增模型推論。影片日期與新版 repo 功能分開，不能把現況回填為影片當時就有。

[機讀收據](research/t8-remaining-2026-11-09.json) 只保留影片資訊、相關來源及閱讀範圍，不公開說明全文、宣傳連結、第三方技能／工作流或權重。程式授權辨識不代替模型、素材及輸出用途條款。

## 優先學的方法

| 順序 | 方法與劇組缺口 | 既有資源優勢 | 第一個有辨別力的驗證 |
|---|---|---|---|
| 1 | 完成階段保存／恢復；已接受 take 續接 | 重用既有 H3，減少失敗後無謂重採樣 | 新程序恢復完整短 take，核對來源與完整輸出；再做一個接點、排除畫面／聲音重複 |
| 2 | 可見臉保護，再作局部修復 | 先保留原片與手動 ROI，不先新增分割模型 | 含眼先頭後、壓嘴角、遮擋或第二人的短片；原速和逐幀比較，追蹤遺失回原片 |
| 3 | 確定性時間線＋連續運動 QA | 瞳的系統 UI／ERROR 可用既有圖形及剪輯工具 | 自有短字卡重渲染，檢查快速細線、停頓、觸發時間；不誤刪刻意定格 |

這三項是方法採用，不表示已完成相應工具部署或成片驗收。尤其小臉修復會重新生成表演；清晰度、超分及插幀都不能補回原本缺失的演技。

## 保留與暫緩

| 項目 | 判定 | 具體理由 |
|---|---|---|
| FireRedAudio | 對白量大時優先候選 | 回讀、局部修復、保留內部停頓及角色等長分軌有用；先比對既有工具。獨立 worker 的 Python／Torch／Transformers 與主環境不同 |
| IndexTTS 2.5 | 備案，先不導入 | 逐句情感有價值，但與 Drama3／OmniVoice 交接重疊；requirements 要 Transformers 4.x，不能直接改主 host 5.x。API 授權辨識 NOASSERTION，尚未完成條款核對 |
| VOSR2 | 劇照／關鍵幀候選 | 文件定義 IMAGE batch 逐張一階超分，每張 seed+i；已讀 README 未建立時序一致機制。首次執行下載約 7GB 匹配組件，不能借用任意現有 VAE |
| Hi3D | 有具體道具／重定向缺口再上 | 已有 Blender／SAM3D；完整獨立工作台依賴較多，臉部細節與手指仍非強項 |
| Meridian／Semantic Bridge | 留研發 | 重運鏡有幾何、條款和資源前提；文字條件橋需 held-out 對照，不自動等於人物一致性 |
| Topaz／DLSS | 交付需求出現再評估 | 官方授權／外部 runtime 及各自條款；DLSS wrapper 授權不等於 NVIDIA／native runtime 可再散布 |
| RFMSR／SeedVR／FlashVSR | 來源待釐清 | 該影片標題與說明 repo 不足以唯一辨認實作，不用題名當品質或安裝證據 |
| 新音樂／RVC、換角工廠、影片轉提示技能 | 目前不優先 | 已定音軌及既有拆片／導演卡可先完成需求；另案才補新能力 |
| 宣稱無版權的演員庫 | 不列可用資產 | 未取得每項素材來源和授權；宣傳文字不能代替權利證據 |

## 本機比對

有限目錄調查：主 ComfyUI 的候選專屬 DLSS、SeedVR、FlashVSR、Hi3D 與相關臉部模型目錄未找到可辨認資產；onnx 為空、upscale_models 只有占位。不明 yolo/model.pt 不能視為可用臉部偵測器。未掃全機，不能斷言其他位置沒有安裝。既有 H3 隔離原始碼可用於評估手動畫 ROI；移動人物仍需逐幀可靠區域。

查得 GPU 驅動 621.01 高於上游 DLSS 文件的 616.56 數字門檻，尚未驗證其 runtime／DLL／功能。標準 Topaz 路徑未見程式，沒有調查其他安裝位置。既有 MOSS／CharRef 的準備與補丁保持，不重複下載或覆寫。這些是目錄／文件證據，沒有新增 GPU 佔用。

## 固定來源與具體採用範圍

- H3 [可見臉保護](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/VISIBLE_FACE_MASK_EXP.md)、[凍結多人來源](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/MULTIFACE_FROZEN_SOURCE_EXP.md)、[外部 take 續接](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/examples/workflows/67-radar-external-continuation/README.md)：採來源／階段責任、最終混合保護與上下文裁除；不同冷交付路線的模型需求不同。
- H3 [無臉分支](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/NO_FACE_LAZY_EXP.md)、[模組化採樣](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/MODULAR_SAMPLING_EXP.md)：未知不等於無臉；額外活躍輸出可能仍觸發重分支。僅採條件跳過與階段分離方法，不引入作者自己的人工批准儀式。
- 原版 [FaceRefine](https://github.com/Carasibana/ComfyUI-H3-FaceRefine/blob/d8521d14fe0d721d80cd9417fff5a559cbc21aba/README.md)：讀至 1.1.2 追蹤遺失回原像素、1.1.0 硬切分鏡說明。T8 [適配紀錄](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/FACE_REFINE_ADVANCED_VALIDATION.md) 基於另一版原始實作；未做追蹤程式差異審計，不假定新版修正已移植。
- [VOSR2](https://github.com/ylchen333/ComfyUI-VOSR2/blob/6a21810b3f4f1a0ffc477c55330db0ac03c671f0/README.md)：獨立社群包，匹配 DiT／Qwen2D VAE／DINOv2-L；大於訓練尺度的 tiling 與顯存需求依文件評估，未本機測試。
- [FireRedAudio](https://github.com/T8mars/comfyui-fireredaudio-T8/blob/715203a451dd4db6ca412be86c723db9fc1d89dd/README.md)、[worker 依賴](https://github.com/T8mars/comfyui-fireredaudio-T8/blob/715203a451dd4db6ca412be86c723db9fc1d89dd/requirements.txt)：採 ASR 輔助、非破壞返修及分軌交付的候選用途，不取代人工聽審。
- [IndexTTS 2.5](https://github.com/T8mars/comfyui-indextts25-t8/blob/22c65286ccaf87665b6b3a65107beb84e45267b3/README.md)、[依賴](https://github.com/T8mars/comfyui-indextts25-t8/blob/22c65286ccaf87665b6b3a65107beb84e45267b3/requirements.txt)：逐句情感與版本隔離；尚未評估聲線和演技。
- [Code-Animate 工具正文](https://github.com/T8mars/Code-Animate-T8/blob/d4f0d1216d33781ce47f38de770d93626f85e7ce/skill/TOOLS.md)、[技能描述](https://github.com/T8mars/Code-Animate-T8/blob/d4f0d1216d33781ce47f38de770d93626f85e7ce/skill/SKILL.md)：採確定性與有狀態渲染的區分、連續運動檢查；靜止／抖動指標只作提示，保留 Foyege 的克制表演與刻意效果。
- H3 [DLSS](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/DLSS_NR_AUDIT.md)、[Topaz](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/TOPAZ_EXP.md)、[HyperFlow](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/HYPERFLOW_LONG_VIDEO_EXP.md)：外部 runtime／授權及特定長鏡路線邊界；不外推到任意有嘴型 MV。

## 文字走查與待測

維護者依新卡人工走查：小臉已清晰但壓嘴角提前，拒絕以清晰度採用；雙人遮臉時偵測抓到另一人，保留原片並報失追；三秒沉默字卡不以低幀差刪除；換參考／音軌後不借用舊階段身份；一般單鏡提示詞繼續用既有表演卡，不展開工具準備；缺原片／遮罩時交付待綁定比較卡，不宣稱已保護。這些是文字核對，沒有獨立模型行為測試。

本輪沒有安裝、下載模型、啟動服務或使用 GPU；已部署三項工具的殘框、字幕語意與擬音未聽審限制，仍依原實驗紀錄保留。
