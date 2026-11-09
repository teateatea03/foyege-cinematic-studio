# 2026-11-03 RTX 5080 本機短測

## 適用條件

第一輪使用現有 Wan2.2 TI2V 5B 的 I2V 路線，僅使用 ComfyUI 核心節點。此紀錄支持指定樣本與設定的可執行性及逐幀可見結果。角色為既有粉紅髮範例圖的近景裁切，正式專案角色的素材與身份規格需另行驗證。本頁為歷史觀察摘要；2026-11-07 公開整理時沒有重新執行推論，原始媒體未隨包公開。

- GPU 為 RTX 5080，16GB，程序透過 GPU UUID 隔離。服務僅回報一張 CUDA 裝置。
- ComfyUI 0.43.2，PyTorch 2.12.0+cu130，既有 embedded Python 3.13.11。
- 主模型 `wan2.2_ti2v_5B_fp16.safetensors`，UMT5 FP8 scaled encoder，`wan2.2_vae.safetensors`。
- 512×512、24fps、20 steps、CFG 5、uni_pc／simple、shift 8、seed 6031103。
- 輸出保留原生 PNG 影格與 WEBM，另轉 H.264 MP4 供播放。四個成品共 244 個原生影格。
- 所有原生影格已用有時間標記的圖表查看，另核對 MP4 可解碼、影格數、畫幅、fps 與時長。本輪輸出靜音。使用者後續已看片確認展示樣本的觀察結論，範圍見文末回饋紀錄。

## 結果

| take | 對照與時長 | 逐幀觀察 | 可採用範圍 |
| --- | --- | --- | --- |
| T01 | 眼先移、頭後跟，49 格／2.042 秒 | 前段有目光變化，約 1.417 秒出現向畫面左側的突發瞥視，尾端目光再靠回鏡頭 | 指定目標與尾端保持需修正 |
| T02 | 閉唇淺笑與保留疲態，49 格／2.042 秒 | 約 1.6 秒後眼瞼逐漸閉合，尾端嘴角上提；既定注視被打斷 | 嘴角變化可見，持續注視需修正 |
| T03 | 沿用 T01 提示詞與設定，只把長度增至 97 格／4.042 秒 | 約 0.58–0.83 秒目光與頭部轉向畫面右側，後段維持同一方向。明確的眼動後、頭動前停頓仍不夠可讀 | 方向與尾端保持改善，精確先後需修正 |
| T04 | 沿用 T02 設定，僅把疲態句換成明確的開眼、鏡頭目標與眼瞼高度，49 格／2.042 秒 | 約 1.67–2.00 秒嘴角形成淺笑，眼睛保持睜開並朝鏡頭，頭部幅度小 | 本條件下通過開眼淺笑的逐幀檢查，心理上的勉強感仍待觀眾判讀 |

髮色、臉部外觀與服裝在檢視範圍內大致承接首圖。此為目視觀察，正式角色的眼色、標誌、精確臉型與換裝一致性需使用專案素材另測。

四次服務端執行時間分別為 150.35、21.44、44.96、21.66 秒。首輪包含冷載入，後三輪有快取，時間供本機排程參考。生成途中一次 GPU 讀值為 15,414 MiB，屬取樣值，實際峰值與其他解析度仍需測量。

## 可以寫進製作決策的經驗

1. 需要保持目光時，將「疲態」拆成眼瞼高度、視線目標與保持條件。保留角色內在意圖於導演卡，模型稿交代可見狀態。
2. 額外閉眼會改變觀眾對笑容的理解，驗收時分別檢查嘴角、眼瞼與視線。嘴角有變化只是其中一項。
3. 短測要容納主要動作與結尾保持。本次較長版本的方向較穩定，改變影格數也改變取樣張量形狀，只能視為單案例對照。四秒並非通用最低時長。
4. 眼頭延遲需要可讀的中間狀態。若一次文字短測仍無法清楚呈現，改評估有合格驅動表演的 Wan Animate 2、已具臉部控制的動畫，或分鏡承接。下節另有 Wan Animate 2 的淺笑轉移與靜態續接紀錄，精確眼頭延遲及臉部動畫資產路線仍待驗證。
5. 完整鏡頭鏈的身份、節奏與接鏡狀態仍須分開核對。鏡頭生成可執行性與已接受成片各自記錄。

## T04 實際提示詞

```text
Locked close-up matching the reference image. The character keeps looking toward the camera. After a short listening pause the corners of her closed mouth rise slowly into a very small polite smile. Her eyes stay open, fixed on the lens, with the upper eyelids held at the same height as in the first frame. She holds the faint closed-mouth smile with her head and shoulders quiet, breathing gently.
```

負面提示為 `blurry face, distorted eyes, deformed face, subtitles, text, camera shake, exaggerated facial expression, extra teeth`。此欄屬本次 Wan 配方，其他模型依其支援方式適配。聆聽刺激本輪由提示詞安排，音效或對白觸發的聲畫時序另測。

## 可追溯證據

完整檔案由維護者保存在私人實驗紀錄，未包含在公開包。其 `manifest.json`、四份 API workflow、`T01` 至 `T04` submission／history、`review-summary.json`、逐幀雜湊清單、服務啟動參數與日誌保留輸入及輸出證據。工作流 canonical SHA-256 依序如下。

```text
T01 5e7812cca1e5a5177114f958674143e353cc55f99e04a390c2a50d85c3dd6c46
T02 56a4ca17be57aa7da88022257b18fb0fd1ca0bbecae0fde3d2e04dde46007561
T03 a2e368c8b45cae788735b893af3b235736b002e15e06df37aa835bf5d7addfb6
T04 338d612a6ae7959fc8ca0631ef240e9389f5e97f2df389a8c10d8360aac0c8d9
```


## Wan Animate 2 表演轉移與延續

第二輪兩次服務端執行時間為 162.80 與 48.11 秒，前者包含新模型載入，後者沿用快取。沿用同一張 5080，使用 `wan_animate_2_distill_int8_convrot.safetensors`、UMT5 FP8 scaled、CLIP Vision H 與 `Wan2_1_VAE_bf16.safetensors`。512×512、24fps、10 steps、LCM／simple、CFG 1、shift 5，pose_strength 與 reference_image_strength 均為 1。pose cache 存放 CPU，精度 int8。此配方只使用本機核心節點，顯存與記憶體上限依實際長度另測。

- **T05 表演轉移**。以 T04 的 49 格淺笑影片為驅動，角色參考改成既有黑髮男性人偶範例的近景。輸出 49 格／2.042 秒。逐幀可見約 1.67 秒後嘴角上提，眼睛保持睜開，外觀維持男性範例的黑髮、臉部與黑色帽衫。這是生成影片驅動另一角色的單案例，真人參考轉移與正式角色的身份規格需另測。
- **T06 延續**。使用 T05 已查看的尾幀作 continue_motion，video_frame_offset 輸入 49，seed 改為 6031104。驅動片的後 48 格由 T04 尾幀複製保持，完整驅動共 97 格。輸出移除一格重疊後為 48 格／2 秒。逐幀可見淺笑與外觀延續，表演幅度很小。此案例驗證固定機位、保持表情的接縫，運鏡、肢體動作與情緒大轉變另測。

已查看這兩段全部 97 個原生影格，並額外對照 T05 尾五格與 T06 起始十一格。接縫未見明顯換臉、構圖跳動或笑容重置。作為輔助紀錄，臉部 ROI 的 RGB 平均絕對差於 T05 最後一個影格間隔為 5.96，接縫為 2.23，T06 首個間隔為 0.79，量尺為 0–255。此數字只描述像素變化。使用者後續已看片確認展示合併試片的觀察結論。

此版本的續接需保留節點輸出的修剪資訊。

1. 保留原本角色參考，將已查看的上一段尾幀接入 continue_motion。
2. video_frame_offset 沿用上一個 conditioning 節點輸出。此版核心會依重疊影格往回對齊驅動片，避免自行重算跳過一格。
3. 採樣後，TrimVideoLatent 使用 conditioning 的 trim_latent 輸出，先去掉角色參考前綴再解碼。
4. 解碼後，ImageFromBatch 使用 trim_image 輸出移除重疊部分。這次首段為 0、延續段為 1。
5. T05 的 49 格與 T06 的 48 格在本機直接串接為 97 格／4.042 秒，影片未額外補幀或交叉淡化。檢查接縫的外觀與表情後才進入正式連續性帳。

上述行為已核對本機 ComfyUI 0.43.2 的 nodes_wan.py 與實際輸出。更新版本或換工作流時重新讀節點 schema，保留其 trim／offset 契約。

兩輪共六個 take、341 個原生影格。新增 canonical workflow SHA-256 如下。

```text
T05 dfc29ede0c0cfe59ebf63d62e23c6961e80f0035b5712c50b68bc899a4638167
T06 dc840f11d0712c436506fb2074b51e66abbe79c8fecb6940888086591c7ffd4e
```

transfer-inputs.json、continuation-inputs.json 與 seam-review.json 保存驅動片的複製保持、上一段來源、裁切、雜湊、影格數及接縫檢查。成品為靜音技術試片，展示片的看片回饋見下節，正式角色素材需另測。


## 使用者看片回饋

2026-11-03，使用者看完 T04 開眼淺笑與 T05／T06 合併試片後，確認展示樣本與上述觀察結論一致。播放速度未另行回報。此為當次使用者回饋摘要，不代表公開讀者已獨立重現。

此回饋涵蓋展示的三個 take。精確眼頭延遲仍需修正，正式角色身份與 MV 音軌仍需另外驗證。原始回饋與涵蓋範圍保存於實驗目錄的 user-playback-review.json。

## 2026-11-09 GPU 遮擋預演

在使用者指定的優先 MV 任務回報完成及 GPU 工作結束後，讀取當下低負載，再進行本輪兩個獨立背景渲染。Blender 5.2.3 LTS、本機已支援 GPU 的預演工具、Cycles 8 samples、640×360；兩份 manifest 均記錄 RTX 5080 單卡 OptiX、CPU fallback 為空，渲染程序已正常退出。沒有啟動 ComfyUI 或影片模型。幾何建構與以下射線量測使用 CPU，GPU 證據限於實際渲染。

輸入為 [A 遮擋](../assets/occlusion-test/A_occluded.json) 與 [B 讓開](../assets/occlusion-test/B_clear.json)。C1 位於 (0, 0.5, 0)，C2 位於 (0, -0.5, 0)，相機位於 (0, -5, 1.6)、看向 (0, 0, 1.1)，50mm。B 只把 C2 的世界 X 改為 0.9 公尺；C1、相機、材質、光線與其他設定相同。兩端關鍵位置相同，24fps／24 格只是靜態工程時間範圍；每版輸出第 1、12、24 格預覽及俯視圖，未輸出完整動畫。

已查看兩版成對機位與俯視圖。A 的藍色 C1 頭部被橘色 C2 遮住；B 的 C1 頭部可辨。在第 1 格同一 C1 頭部投影外接框內作 25×25 射線取樣，首先命中 C1 頭或鼻的格點由 0/625 變為 481/625。這是幾何取樣，分母含未命中頭部的框角，不是可見面積百分比、觀眾視線或微表情評分。

本案例支持從最終相機先排除遮擋，再測表演。沒有測得動態連續性、眼神／表情、生成模型遵循度或觀眾注意力效果。JSON 保存原創幾何輸入；GPU 運算後端以本輪本機 manifest 為準，不推及所有 Blender 部署。研究目錄另保存 .blend、八張 PNG、輸入與工程雜湊、對照圖及 visibility.json。
