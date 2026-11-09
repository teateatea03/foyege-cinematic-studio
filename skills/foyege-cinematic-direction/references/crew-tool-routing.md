# 劇組工具選用與候選驗收

適用於找 ComfyUI 補強、評估新節點、長鏡續接、擬音、字幕或 3D 資產。2026-11-09 依 T8star-Aix 頻道線索與第一方文件整理；以下是本技能的原創選用卡。方法可先用，候選工具未因列入本頁而取得本機可用資格。Foyege 的空間、外觀、微表演與接鏡仍為驗收核心。

2026-11-09 優先項目已有隔離短測：[操作入口、API 圖與實測限制](priority-crew-setup.md)。字幕 CUDA CLI 可用；空間標記可供預演但仍殘框；MMAudio 擬音已執行、聽審待做。其他候選維持原證據等級。

評估小臉修復、超分、階段恢復、MV 系統字卡或其他聲音候選時，再讀 [第二輪選用卡](finishing-candidates.md)：優先重用階段保存／恢復、保護原表演的局部合成，以及可重現字卡與連續運動檢查；其餘候選按具體缺口準備，未部署項目不提升資格。

已選定階段核對、可見臉合成或系統字卡工作時，讀 [後製實作與 CLI](finishing-tools.md)；來源 guard 不代替原生 Stage Load，像素 pass 不代替微表情／聲音接受。

## 選用順序

先寫這一鏡的缺口，再查 [本機資源](local-resources.md)。列出現有路線、只缺的能力、候選所需輸入／依賴、第一個有辨別力的試片及失敗後回復路線。原工具可完成就沿用；只在新增能力有價值時準備候選。資料整理與實際部署分列，依使用者當下排程和授權執行。

| 缺口／部門 | 先用什麼 | 候選與採用界線 | 第一個驗收 |
|---|---|---|---|
| 美術／角色外觀 | 已有角色圖與本機編輯／參考路線 | MOSS 的 Base／SFT、Edit、CharRef、加速 LoRA 分開配套，不把所有附件疊在一起 | 固定身份與服裝，只改一項姿勢／場景；檢查眼形、髮飾、手及三視角 |
| 導演／走位 | Blender 白模與角色／目標 ID | Visual Marker 是參考圖語義引導，可先人工繪框，不是座標硬鎖或 ControlNet | 先單人走到目標停住；再測雙人，查身份交換、路徑、腳底與殘框 |
| 攝影／運鏡 | 既有相機預演與接鏡設計 | Meridian 是影像／影片重運鏡候選，須另備模型、幾何來源及配套 assets | 小幅橫移，查裁邊、遮擋揭露、臉部與背景；大角度新視野另測 |
| 長鏡／場記 | 已接受 take 的終態及可剪接覆蓋 | H3 分段／Relay 與雙采路線依實際版本選，不承諾無縫或逐詞精準 | 兩段一個接點；完整看續段，查動作重播、身份／光色跳變與聲音重複 |
| 聲音／擬音 | 既有音效素材或本機 MMAudio 等可用路線 | H3 Foley 可列比較；是給既有畫面補動作聲，不是配音或克隆 | 一個清楚接觸事件；獨立音軌，核對同步、意外人聲／音樂和原畫面旁路 |
| 字幕／本地化 | 既有定時字幕與專案詞彙表 | IndexTranslateSRT 可譯 cue 文字；ASR、瀏覽器翻譯、配音是另外的能力 | 短 SRT 含人名、停頓與雙語；檢查 cue 數、時碼、漏譯、換行及可讀性 |
| 3D／資產／預演 | 已有 Blender、SAM3D 與資產 | Hi3D 節點精修同物件的粗網格；完整建模／PBR／綁骨在獨立工作台 | 一個道具 GLB 回 Blender，查尺度、輪廓、UV／材質及鏡頭可見細節 |
| 動畫／綁骨 | 已有可用 rig 與表演參考 | Hi3D 工作台的分件、蒙皮、動作重定向另評估；不等於臉部微表情 rig | 單角色抬臂轉身，查服裝拉伸、腳滑、接觸穿插；臉部另驗收 |
| 提示詞編譯 | 完整導演卡與既有模型適配 | FLUX3 PE 產生文字提示；參考圖／框輸入不保證最終身份 | 比較編譯前後是否偷改人物、眼神、台詞與克制停頓，再分開測出圖 |
| 動作遵循／研發 | 先修因果稿、姿態及參考責任 | Semantic Bridge 是文字條件橋，不是影片 LoRA；依專屬設定與 held-out 場景比較 | 同模型／輸入／seed 開關對照，查改善是否損害臉部及無關動作 |
| MV 字幕／UI／動態圖形 | 現有剪輯與程式圖形工具 | Code-Animate 的時間線與分段渲染可供學習；不整包納入未知授權技能 | 自有素材做短 UI／字幕段，固定時間重渲染，核對音軌與字形 |
| 音樂／改編 | 專案已定主音軌與分軌 | MuLaCover／YuE2／RVC 屬另案創作或聲音實驗；先核對模型／輸出用途條款 | 自有或已授權旋律短段，分開驗收旋律、歌詞、聲線與時長 |

## 四個易錯接點

**視覺標記。** 保留乾淨底圖、標記版與角色／目標圖例；標記座標綁定實際源圖及裁切版本。核對真實 Picture 順序，首尾幀可能占用前面的編號。T8 的 Bind 與一般預處理接線證據不同；編號正確不等於角色身份已證實。clean-VAE／marked-Qwen 分流屬另一項實驗，不能預設會去框。

**長鏡。** 穩定場景與外觀可放 global，單次台詞／動作依可用 Relay 綁局部事件，避免每段重播。先確認上下文來自哪個實際接受輸出；更換模型、提示詞、參考、時間或採樣方案時重新辨識續做與快取。顏色修正、前綴相同或邊界差值下降，都不能代替整段觀看。

**聲音。** 擬音候選只接聲音分軌，保存原畫面及原音；若測試純生成擬音，來源靜音與保留現場聲兩種條件分開。字幕翻譯保留源 cue 與時間碼；更改斷句或配音時建立新版本，不能繼續冒用舊詞級表情觸發點。音訊解碼及同步檢查之外，仍需實際聽辨。

**新依賴。** 同名節點、權重和整合包可能有不同功能。先核對 host Python、Core、Torch、Transformers、CUDA／wheel、模型架構和工作流版本。已有本機補丁保留；不要為一個候選升級整套 ComfyUI。獨立工作台須單列服務、權重及環境，不因下載節點而標為全功能就緒。程式授權與每個模型／輸出條款分別記錄。

## 一張候選卡

```text
鏡號／部門／具體缺口：
既有路線與不足：
候選來源＋固定 revision：
責任：文字／身份／空間／動作／聲音／後製：
輸入資產 ID、版本與來源範圍：
Core／節點／權重／外部 runtime；已存在與待準備分列：
保留原檔與回復路線：
最小比較：基準／唯一變量／候選數／停止條件：
技術判準；微表演、動作、聲音與接鏡判準：
結果：未部署／可載入／短測／內容通過／已接受：
```

例如：角色 A 聽見門外聲音，先看門、壓下嘴角，再走到門邊停住。白模負責路徑與機位；標記只協助指認人和目標；聲音 cue 負責刺激；眼神與嘴角仍由表演卡控制。一次先測走位，不能因走到門邊便宣稱微表情通過。

## 來源與閱讀範圍

本次為頻道目錄、12 支影片說明連結與以下來源相關正文調查，沒有完整觀看該批影片或新增本機推論；測試卡是自行整合。

- [原始標記實驗](https://github.com/RK-BoilingPoint/H3-Visual-Marker-Control/blob/0f0274f5f07c0e8dda0bb8cd0286256587f4e959/README.md)：含殘框及不穩定案例。
- [T8 標記適配](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/VISUAL_MARKER_EXP.md)、[長鏡](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/DUAL_MODEL_LONG_VIDEO_EXP.md)、[擬音](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/docs/H07_FOLEY_USAGE.md)、[Meridian](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/blob/3a23f333537d9a715aad7ce79af8d9ec891d9ad8/examples/workflows/37-meridian/README.md)：功能與限制正文。
- [Hi3D](https://github.com/T8mars/Comfyui-Hi3d-T8/blob/8fae8e4e86a83f3af92a9b9bfcd6c8b78dfa75bc/README.md)、[資產工作台](https://github.com/T8mars/Comfyui-Hi3d-T8/blob/8fae8e4e86a83f3af92a9b9bfcd6c8b78dfa75bc/docs/ASSET_STUDIO.md)：節點／獨立環境邊界及品質限制。
- [SRT 適配](https://github.com/T8mars/Comfyui-Index-Translate-T8/blob/5beac49cd0f8e125f0ca00cb5eba6bc2b7ed265a/README_EN.md)、[翻譯模型原專案](https://github.com/bilibili/Index-Translate/blob/93ac63774d1c6939aec05e6f0f191bf90f225365/README.md)：具體支援模式依部署產品分開。
- [FLUX3 PE](https://github.com/T8mars/Comfyui-Flux3-PE-GGUF-T8/blob/4a7fe1af236510eb3788849190b6fa25267d6d91/README.md)、[文字條件橋](https://github.com/T8mars/MinimaxH3_Semantic_Bridge_Trainer-T8/blob/3bc62bf5518fb59c784b5d446e343729d2a03d51/README.en.md)：候選輸入／輸出與用途。
- [程式影像](https://github.com/T8mars/Code-Animate-T8/blob/d4f0d1216d33781ce47f38de770d93626f85e7ce/README.md)、[換角工廠](https://github.com/T8mars/video-replacement-skill-factory-T8/blob/5e5a1d85abc661b15a65c0a3094e8bf88810abc5/README.md)、[MuLaCover](https://github.com/T8mars/Comfyui-Mulacover-T8/blob/7e8b16912557f605547c38709c93e7c5915e32d5/README.md)：概念參考；未捆綁第三方程式、技能、工作流、權重或媒體。YuE2／RVC 本輪僅取得影片說明線索，尚未審其實作。
