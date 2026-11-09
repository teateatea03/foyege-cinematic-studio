# 2026-11-09 SAM3D／RefMod 本機驗證

本次補齊本機缺口，完成實際 GPU 推論及輸出檢查。這是維護者指定環境的單次技術紀錄，並非 Foyege 作者對這兩套工具的背書，也不是瞳角色或正式 MV 素材驗收。核心導演方法保持不變。

[機器可讀摘要與雜湊](evidence-summary.json)

## 結果

| 路線 | 實際完成 | 判定 |
| --- | --- | --- |
| SAM3D 全身 | RT-DETR → MoGe2 FOV → SAM3D → GLB → Blender | 執行成功，127 骨骼、72 morph targets |
| SAM3D 表情 | 73 幀／24fps 驅動 → GLB → Blender | 29 個 morph 通道有變化；5080 OptiX 中性、笑容、眨眼三張快照已目視確認 |
| RefMod 完整參考 | 提取、儲存、獨立程序讀檔、H3 生成 | 256 tokens；保留示範人物可辨識外觀，可作技術基準 |
| RefMod pooled16 | 相同生成設定，refinement_steps=0 | 64 tokens；臉眼失真及模糊明顯，不採用為身份保真基準 |

完整參考仍出現與閉嘴提示不符的微張嘴，不能宣稱精準控制表情。兩組原生生成影格共 44 張均已檢視；各 512×512、22 幀、24fps、約 0.917 秒、無聲，解碼與幀數檢查通過。此時長低於原生 H3 文件的訓練時長範圍，只證明短片管線可執行，不代表長鏡頭、細緻眼頭延遲或成片品質通過。

## 安裝與版本

ComfyUI 0.44.2、Python 3.13.11、Torch 2.12.0+cu130；推論及 Blender 5.2.3 LTS OptiX 渲染只使用 RTX 5080。

依本機官方 utility_sam3d_body 模板下載四份權重，總計 5,485,935,084 bytes。下載時核對 HF LFS SHA256 與大小；固定 revision、來源及雜湊見摘要。模型放在 ComfyUI 的 models 目錄：

- detection/sam_3d_body_dinov3_bf16.safetensors
- geometry_estimation/moge_2_vitl_normal_fp16.safetensors
- diffusion_models/rt_detr_v4-x-hgnet_fp32.safetensors
- checkpoints/sam3.1_multiplex_fp16.safetensors

來源：[SAM3D](https://huggingface.co/Comfy-Org/sam-3d-body)、[MoGe](https://huggingface.co/Comfy-Org/MoGe)、[SDPose](https://huggingface.co/Comfy-Org/SDPose)、[SAM3.1](https://huggingface.co/Comfy-Org/sam3.1)。

RefMod 節點為 [ComfyUI-MiniMaxH3Mod](https://github.com/Luisacaotica/ComfyUI-MiniMaxH3Mod/tree/517e8c419a8584fbf69fceb487bc39d83e6a6ec8)，版本 0.2.6、commit 517e8c419a8584fbf69fceb487bc39d83e6a6ec8。既有依賴已足夠，沒有 pip 升降版或 ComfyUI 核心更新。13 項上游 loader 測試通過；兩份實際 safetensors 另由新 CPU 程序、空模組快取成功讀取。獨立磁碟讀檔和服務內生成分別驗證，不宣稱重啟服務後冷啟動生成已測。

H3 模型、文字編碼器及 VAE 沿用本機既有檔案；精確檔名在生成工作流中。這些來源與量化版本須另外核對授權、取得方式與裝置支援，公開包不包含權重。

## 工作流與使用條件

下列為實際成功執行的 API prompt JSON，檔案 SHA256 見摘要。不是 ComfyUI 畫布 UI JSON。

- [S1_fullbody](workflows/S1_fullbody.json)：33.282 秒。
- [S2_face](workflows/S2_face.json)：13.698 秒。
- [R1_full](workflows/R1_full.json)：21.889 秒。
- [R2_pooled](workflows/R2_pooled.json)：1.390 秒。
- [G1_full](workflows/G1_full.json)：178.041 秒。
- [G2_pooled](workflows/G2_pooled.json)：53.811 秒。

輸入檔由使用者放進自己服務的 input 目錄，並核對工作流的檔名：

- S1 使用 fullbody.png，建議可見全身的人物圖。
- S2 使用 face_driver.mp4。本次為 73 幀、24fps、512×512 頭肩驅動；表情 smooth window=1、hand refinement 關閉。
- R1／R2 使用 refmod_reference.png，本次為粉髮示範肖像，並非瞳。
- G1／G2 讀取 R1／R2 儲存於 models/refmods/foyege-tests 的對應檔案；先執行提取／儲存，讓 loader 能列出選項。

在自己已確認就緒的本機 ComfyUI 服務，將工作流以外層 JSON {"prompt": 工作流內容} POST 到 /prompt，依回傳 prompt_id 查詢 /history/{prompt_id}，同時檢查實際輸出。提交即會載入模型並消耗 GPU 資源，先核對閒置裝置及輸入。新版本需比對 /object_info，尤其動態欄位。

R1／R2 是 VAE 參考提取及儲存；G1／G2 是實際 H3 生成，兩者不可混稱。生成共同設定為 seed 6110905、20 steps、res_multistep／simple、512×512、22 幀、單張圖參考、權重 1.0。本次 reference_map 為 <Picture 1>。MiniMaxH3RefModTextEncode 已附帶參考，不再重複 Apply。

完整參考是本次可用基準。pooled16 結果只代表此設定失敗，不能推論其他池化尺寸或 refinement 設定皆失敗。冷／暖啟動及模型載入條件不同，表內秒數不能用來宣稱壓縮帶來速度提升。

## 未驗證與品質邊界

- MHR 重建模型尚未轉接瞳的正式角色；隱藏身體的解剖準確度未測。
- 72 個 morph targets 不代表 72 通道都成功追蹤；本次只觀察到 29 通道有變化，Blender 名稱仍是 target_0…target_71。
- 三張 Blender 快照支持可見笑容及閉眼，未渲染／檢視完整連續動畫，未驗證微小表情的準確度及時間延遲。
- SAM3.1 tracker 權重已下載驗證，但追蹤推論未測；手部 refinement 未測。
- H3 只有約 0.917 秒靜音短測，未取得原速人工驗收，未驗證歌曲同步、聲音或長鏡穩定。
- 原始影片、角色圖片、模型、GLB、Blender 工程及完整私人日誌保留於本機，各自依來源權利管理。公開摘要不能替代實際媒體的重現與驗收。

## 保留與失敗記錄

既有 MOSS CharRef 相容性修補及原生 SAM3D／Wan 檔案前後 SHA256 一致。沒有擴大套件更新、使用另一張忙碌顯卡或開啟挖礦。實驗結束後模型已卸載，服務佇列為空。

Blender 繁中介面中以英文節點名稱查找曾失敗，改用穩定 node type；另一組快照過白，調整材質槽、顯示與燈光後才得到可檢視的 v2。多項設定一起修正，未將某一項宣稱為唯一根因。錯誤與無效快照均留在本機。執行器使用 --python-exit-code 1，避免腳本錯誤仍回報程序成功。

既有工作流 CLI 將輸出映射到固定標準資料夾，對獨立 output 目錄可能誤報 local_path 不存在；本次使用實際檔案、ComfyUI history、解碼及雜湊交叉核對。六次 API 提交均成功，未為補文件重跑 GPU 推論。
