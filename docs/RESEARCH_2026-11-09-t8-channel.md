# T8star-Aix 頻道：ComfyUI 劇組候選盤點

2026-11-09。接續 [Drama3 配音研究](RESEARCH_2026-11-09-drama3-voice.md)，調查使用者所指頻道還有哪些方法值得補進劇組。這是研究與候選清單，未部署新節點、下載權重、啟動服務或執行 GPU 推論。

## 調查範圍

- 頻道為 [T8star-Aix](https://www.youtube.com/@T8star-Aix/)，channel ID `UCCQ8NwZBxQlpE7nQD4i1Viw`。
- 篩選 videos 列表前 150 筆標題；flat listing 有自動翻譯及截斷，不能當作者原文或全頻道覆蓋。再取 12 支完整 metadata／說明欄，核對皆屬同一 channel ID。
- 由說明欄追到 10 個第一方 repo，固定 commit，閱讀下列相關 README／專項正文。取得檔案不等於逐檔審計；本輪未做這 12 支影片的連續觀看、音訊聽辨、完整字幕分析、REA 分鏡或模型測試。
- [可機讀收據](research/t8-channel-2026-11-09.json) 保留影片 ID、上傳日期、長度與來源 SHA。來源程式、影片說明全文及宣傳連結不隨公開包散布。

## 我們最值得採用的順序

P0 表示優先重用既有資源；P1 表示下一個有對應製作缺口時值得準備；P2 為未來候選。優先度是本專案判斷，不是畫質或效能排名。

| 優先度 | 項目 | 幫到的部門與理由 | 目前證據／缺口 |
|---|---|---|---|
| P0 | MOSS 編輯與角色參考 | 美術、定裝、分鏡：先使用既有模型與 CharRef | 本輪核對 10 檔存在且大小符合既有紀錄；CharRef 本機補丁 hash 相符。未重新推論 |
| P1 | Visual Marker 空間引導 | 導演、走位、預演：把「誰到哪裡」畫在參考圖，與 Foyege 的空間分工相容 | 原方法及 T8 Bind／Relay 文件已讀；需核對現有 H3 圖能否承接及殘框風險 |
| P1 | IndexTranslateSRT | 字幕、海外交付、研究助理：翻譯既有定時字幕 | 文件明列保留編號／時碼；未安裝。host Transformers 版本相容是準備重點 |
| P1 | H3 Foley 與既有 MMAudio 比較 | 聲音、後期：替已完成的動作鏡補接觸聲 | 上游有指定短樣片紀錄；本機只有 MMAudio 目錄存在證據，本輪未測任一路線 |
| P1 | 長鏡／Relay 續做方法 | 場記、剪接、導演：事件分段、接受輸出續接、斷點身份與聲音承接 | 本機已有 PromptRelay 目錄；上游長鏈保留品質失敗。先兩段試片再擴長 |
| P2 | Hi3D 與獨立資產工作台 | 美術、3D、動畫：精修道具，未來分件、綁骨與動作重定向 | Comfy 節點與完整工作台不同；已有 Blender／SAM3D，先找具體資產缺口 |
| P2 | Meridian 重運鏡 | 攝影、VFX：已生成鏡頭的小幅相機修改 | 需專屬模型、幾何來源和 assets；目前沒有 5080／16GB 可用證據，部分依賴有非商業研究條款 |
| P2 | FLUX3 PE／Semantic Bridge | 提示詞編譯、動作研發 | 先評估是否超過既有導演卡能力；兩者皆不能單憑文字輸出或訓練收斂證明微表情更好 |
| P2 | Code-Animate | MV 包裝、UI、字幕、資訊圖形：時間驅動和分段渲染 | 適合瞳的系統啟動／ERROR 段方法研究；根目錄無明確授權辨識，本輪不複製技能／程式 |
| 暫緩導入 | 換角技能工廠、YuE2／RVC、MuLaCover | 有合法參考片換角、另案音樂改編才需要 | 工廠與我們已有拆片／工單重疊；YuE2／RVC 僅說明欄線索；MuLaCover 文件標示模型／輸出非商業條款 |

Drama3 已在上一輪補進配音交接；本輪不重複新增一套聲線正本。圖像插幀／放大、小臉修復等標題仍在後續雷達，未因題名列為已驗證工具。後製修臉必須保留原微反應，不能只用更清晰當作表演更好。

## 有用的第一方來源與界線

以下連結固定本輪實際取得的 revision；影片日期早於 repo 現況，因此最新版文件不冒稱是影片當時就有的功能。

### 1. 空間標記

影片：[空間控制](https://www.youtube.com/watch?v=0XVpCRPW2zk)。[原始實驗 README](https://github.com/RK-BoilingPoint/H3-Visual-Marker-Control/blob/0f0274f5f07c0e8dda0bb8cd0286256587f4e959/README.md) 的雙人／三標記段保留成功、殘框與簡化稿不穩定案例。[T8 適配正文](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/VISUAL_MARKER_EXP.md) 區分標記圖準備、真實 Picture 綁定及外置 Relay。採用圖例／角色／目標責任及殘框驗收，不把它叫作座標硬控制。

### 2. 既有影片擬音

[H07 Foley 配方](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/H07_FOLEY_USAGE.md) 明確走原畫面旁路、生成音軌；內部低尺寸解碼影像不作最終畫面。採用獨立分軌及接觸事件驗收，保留既有主歌聲／配樂；上游指定注液案例不外推至任意動作或速度。

### 3. 字幕翻譯與產品分流

影片：[Index Translate](https://www.youtube.com/watch?v=VrQ0Rm9GpOg)。[T8 README](https://github.com/T8mars/Comfyui-Index-Translate-T8/blob/5beac49cd0f8e125f0ca00cb5eba6bc2b7ed265a/README_EN.md) 區分 Comfy 原生節點、Windows 服務及 Chrome 擴充；SRT 輸入須已有時間碼。文件提醒 Transformers 5.17.0 可能影響其他節點，先做相容性調查，不直接升級 host。[原模型 repo](https://github.com/bilibili/Index-Translate/blob/93ac63774d1c6939aec05e6f0f191bf90f225365/README.md) 的多模態家族能力不直接等於 T8 節點已實作全部。

### 4. 長鏡與運鏡

影片：[長鏡／時間控制](https://www.youtube.com/watch?v=tw_VOt1bkAw)、[時間與前饋分塊](https://www.youtube.com/watch?v=eIlTfP0UOng)。[雙模型長鏡紀錄](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/DUAL_MODEL_LONG_VIDEO_EXP.md) 保留畫面結構跳變與數值改善但人審失敗案例；採用「完整續段驗收」與一次性事件只放局部時間窗。分塊節省記憶體不直接代表速度或品質改善。

[Meridian 配套](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/examples/workflows/37-meridian/README.md) 分開相機位置／look／焦距與源時間軌；可能裁掉原圖邊緣。小幅橫移先測，凍結／變速音軌另作處理。Omega 幾何依賴的研究用途條款與主模型分開，重運鏡先留候選。

### 5. 3D 工作台與既有 Blender

影片：[Hi3D](https://www.youtube.com/watch?v=2xV7ef6w5Mk)。[README](https://github.com/T8mars/Comfyui-Hi3d-T8/blob/8fae8e4e86a83f3af92a9b9bfcd6c8b78dfa75bc/README.md) 的 Comfy 節點只精修「同物件參考圖＋粗網格」；完整圖生幾何／PBR 在獨立工作台。[資產正文](https://github.com/T8mars/Comfyui-Hi3d-T8/blob/8fae8e4e86a83f3af92a9b9bfcd6c8b78dfa75bc/docs/ASSET_STUDIO.md) 列分件、蒙皮、動作重定向，但衣物拉伸、腳滑、穿插及手指仍有限制。不能代替可控制的臉部 rig。先對照既有 Blender／SAM3D，只補需要的引擎，不下載完整模型大包。

### 6. PE、文字條件橋與其他未來工具

[FLUX3 PE](https://github.com/T8mars/Comfyui-Flux3-PE-GGUF-T8/blob/4a7fe1af236510eb3788849190b6fa25267d6d91/README.md) 產出 STRING，可收參考圖及 layout；完整出圖還需其他權重。影片 [角色一致性](https://www.youtube.com/watch?v=yh4MZDLISBU) 的標題不作品質證據。[Semantic Bridge Trainer](https://github.com/T8mars/MinimaxH3_Semantic_Bridge_Trainer-T8/blob/3bc62bf5518fb59c784b5d446e343729d2a03d51/README.en.md) 是文字條件訓練，非影片 LoRA；[教學線索](https://www.youtube.com/watch?v=ENX5Ximey-0) 留待有特定動作缺口時做開關比較。

[Code-Animate](https://github.com/T8mars/Code-Animate-T8/blob/d4f0d1216d33781ce47f38de770d93626f85e7ce/README.md) 使用 Canvas2D／WebGL 的 `renderFrame(t)` 與時間線，適合學習可重渲染包裝。[換角工廠](https://github.com/T8mars/video-replacement-skill-factory-T8/blob/5e5a1d85abc661b15a65c0a3094e8bf88810abc5/README.md) 有本機 Comfy 後端說明；只採用試片綁定當前角色及恢復前核對原任務的思路。[MuLaCover](https://github.com/T8mars/Comfyui-Mulacover-T8/blob/7e8b16912557f605547c38709c93e7c5915e32d5/README.md) 的原生 AUDIO／MIDI 路線列音樂候選，文件標示非商業條款，未改動瞳既定主音軌。

## 本機比對與本輪實際變更

只列已取得的本機證據：custom_nodes 目錄可見 `ComfyUI-MiniMaxH3Mod`、`ComfyUI-AIToolkit-MiniMaxH3`、`ComfyUI-PromptRelay`、`ComfyUI-MOSS-Image-Ostris-Edit`、`ComfyUI-MMAudio`、`ComfyUI-MelBandRoFormer`、`ComfyUI-OmniVoice-TTS`、姿勢與 VideoHelperSuite 等。目錄存在不等於節點可載入、權重齊備或工作流可用。新增候選的同名 T8 目錄未出現在這次清單；未掃描整台電腦，因此不斷言其他位置沒有獨立安裝。

本輪對照 2026-11-02 MOSS manifest：10 個 staged 權重檔存在、大小相符；未重新雜湊全部大檔。CharRef `nodes.py` SHA256 與安裝報告一致，保留 `extra_conds` 適配，未回寫上游 `pe_embedder`。既有 CPU 微型測試不提升為完整 GPU 推論結果。

新增可攜 [工具選用與候選驗收](../skills/foyege-cinematic-direction/references/crew-tool-routing.md)，由 Foyege 與 film-production 按需載入；同步本機 Codex／Claude 時只追加此次入口與參考，保留各自既有差異。未複製第三方技能／工作流、模型或媒體。驗證範圍另見 [驗證紀錄](VALIDATION.md)。

## 下一次可執行的短測

依當下最高製作風險選一項，不把研究清單變成必做測試清單：

1. 角色一致性卡住：先用已在機器上的 MOSS／CharRef，單附件、單變量，保護原本機補丁。
2. 走位或目標錯誤：先用乾淨／標記兩版同圖比較單人到點；需節點才另做版本相容準備。
3. 接觸聲不足：自有靜音片只含一個放杯事件，對照既有音效／MMAudio 與候選，原畫面回剪輯。
4. 海外交付：以既有 8–12 cue SRT 和角色詞彙表測翻譯，先驗時碼及語意；無字幕先走已核對 ASR。

上述模型測試本輪皆未執行；GPU 資源留給使用者當前工作。
