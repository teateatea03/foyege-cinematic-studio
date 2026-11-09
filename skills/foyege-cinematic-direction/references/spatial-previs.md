# 空間、資產與 Blender 預演

## 選擇預演精度

以鏡頭需要的精度決定工作量。站位和入畫時機可用柱體／球體，跪姿、抬腕、倚靠等依賴肢體關係時用可讀四肢的人形，精確抛接、搏鬥或手部接觸需要關鍵姿態、骨架或適配動作。簡單粗模中的僵硬姿勢可能被帶進成片，重要動作不足時也可能讓模型猜錯。[S4](sources.md)

有固定場景外觀時，先確認場景圖，再搭出其可見布局。單張圖未交代的房間、門後空間和尺寸標為設計假設。白模只保留影響路徑、遮擋、構圖和接觸的幾何。材質細節依外觀參考處理。

## 座標與身份

- 世界採 X／Y 水平、Z 向上，記錄單位。角色 ID、家具 ID 和場景拓撲跨鏡保持一致。
- 每台相機記錄位置、朝向／look-at、鏡頭焦距和畫幅。畫面左右從當前相機看，切鏡後重新檢查。
- 角色朝向與眼神分開。身體面向門口時，眼睛可以回看同伴。明確描述有動機的先後。
- 同色代理與資產 ID 對照，參考圖片負責外觀，預演影片負責隨時間改變的空間／運動。不可讓兩個互相衝突的空間版本同時主導。
- 跨軸若屬創作選擇，設計可讀的過渡或建立鏡頭。道具交接指定交出者、手別、接觸時刻、接收者與最終持有狀態。

## 參考圖職責

多圖輸入時，為每檔列「負責項目、可用槽位、可能衝突、證據狀態」。身份基準選五官可辨的已接受圖，起始幀須符合本鏡開始狀態，表情峰值圖可作終態設計。模型支援的實際槽位決定送入方式。[R3](related-skills.md#r3-分鏡連續性檢查) [R6](related-skills.md#r6-資產基準與交接)

- 教學箭頭、角色卡文字、表情格線與色塊保留在導演檢查版。生成輸入另取乾淨單格，保留原圖及派生版本關係。
- 空間圖綁布局，材質圖只綁外觀。兩圖布局衝突時先選定權威版本，列出另一圖的取用範圍。
- 新物件成為主體時，標明同場轉向、剪接或換場，使用可辨地標建立關係。世界位置固定，畫面左右隨攝影機推導。
- POV 由鏡頭主人與故事設定決定可見手、袖口、影子與倒影。劇情需要的手別、交接及持物責任要留在連續性帳。

## 交付預演

先檢查起、中、終三個時刻，再看完整運動。指出「第幾秒人物被遮住」等具體問題，只修對應機位或動作。保留可修改 .blend，交給影片模型的是其支援的渲染影像／影片。預演與生成目標的時長、畫幅須對齊。

跨鏡頭共用工程與時間線，再分段輸出。沿用同一空間可減少重搭引入的漂移，生成端仍需驗證角色與細節連續性。

運鏡的敘事用途、路徑／朝向／焦距分工、速度與停頓另見 [運鏡與表情](camera-movement.md)。既有腳本可驗證的相機欄位與需在另存工程完成的控制分開列明。

## 本機最小工具

附帶 [build_previs.py](../scripts/build_previs.py) 與 [two-person.json](../assets/two-person.json)，可產生雙人代理、家具、移動相機、俯視圖、三張預覽與 .blend。用於粗略站位／機位測試，臉部表演、骨架、接觸與完整動畫另行製作。

在獨立背景程序執行。輸出目錄必須尚不存在，避免覆蓋工程。以下從本專案根目錄執行，Blender 若不在 PATH，將 $blender 設為自己的執行檔路徑。

```powershell
$blender = (Get-Command blender -ErrorAction Stop).Source
$skillRoot = (Resolve-Path './skills/foyege-cinematic-direction').Path
$outputRoot = Join-Path ([IO.Path]::GetTempPath()) ('foyege-previs-' + [guid]::NewGuid().ToString('N'))
& $blender --background --factory-startup --python-exit-code 1 --python (Join-Path $skillRoot 'scripts/build_previs.py') -- --scene (Join-Path $skillRoot 'assets/two-person.json') --out $outputRoot
if ($LASTEXITCODE -ne 0) { throw 'Previs build failed' }
```

JSON 欄位使用公尺、影格和角度。
- fps、frames、resolution 設定整段預演。整數 fps，duration = frames / fps，影格 1 對應 t=0。
- actors 的 id、color、yaw_deg、keys 定義身份色、面向和移動。keys 為 frame 與 location，location 是腳底中心。yaw_deg 為繞世界 Z 軸旋轉，0 度面向世界 -Y，90 度面向 +X。
- boxes 使用 id、location、size 定義家具中心與尺寸。
- camera 的 lens_mm 與 keys 定義位置及 look_at。演算法在關鍵點間線性移動，每格烘焙視線方向。
- 每組 keys 需從 1 覆蓋至 frames，順序遞增。朝向固定，精確表演需要後續編輯。
- topview 的 center、height、ortho_scale 控制地圖視野。
- 檢查輸出的 manifest.json 和實際影像後才接受布局。代理顏色及物件名稱可查身份，文字標籤僅供俯視圖。

需要連續預演時從已生成 .blend 輸出 PNG 序列，再編碼。新建空目錄後執行，以下假設專案 24fps、96格。

```powershell
New-Item -ItemType Directory -Path (Join-Path $outputRoot 'sequence') -ErrorAction Stop
& $blender --background (Join-Path $outputRoot 'scene.blend') --render-output (Join-Path $outputRoot 'sequence/frame_####') --render-format PNG --render-anim
if ($LASTEXITCODE -ne 0) { throw 'Sequence render failed' }
ffmpeg -n -framerate 24 -start_number 1 -i (Join-Path $outputRoot 'sequence/frame_%04d.png') -c:v libx264 -pix_fmt yuv420p (Join-Path $outputRoot 'previs.mp4')
```

腳本採低解析度 Cycles CPU 渲染，便於本機測試。需要正式生成參考時按輸入規格調解析度與片長。幾何代理只驗證空間，微表演另以近景影片或實拍試演檢查。
