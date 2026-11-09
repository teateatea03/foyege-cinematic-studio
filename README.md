# Foyege Cinematic Studio

依 Foyege24 公開教學整理的非官方導演技能，搭配獨立編劇支援。適用於 MV、短劇、長劇、動畫與其他影像。核心是把空間、外觀與表演分工，再用可見事件、微反應與接鏡狀態完成敘事。

## 核心方法

| 方法 | 實際交付 |
| --- | --- |
| 空間交給預演 | 角色 ID、場景拓撲、機位、走位、遮擋與時間線 |
| 外觀綁定素材 | 角色、服裝、場景和道具的參考責任 |
| 微表演留在文字與參考表演 | 刺激、眼神目標、嘴角、呼吸、壓制與殘留 |
| 因果動作 | 發力、接觸、反作用、恢復與終態 |
| 跨鏡延續 | 已接受 take、持物、眼線、情緒和聲音承接 |
| 按工具能力執行 | 模型提示詞、驅動片或臉部動畫的適用範圍 |

[核心方法與檢查](docs/FOYEGE_CORE.md) · [作者來源與閱讀範圍](skills/foyege-cinematic-direction/references/sources.md) · [2026-11-07 研究補強](docs/RESEARCH_2026-11-07.md) · [2026-11-08 YouTube 表演補強](docs/RESEARCH_2026-11-08.md) · [2026-11-09 場景與素材交接](docs/RESEARCH_2026-11-09.md) · [第二輪表演參考補強](docs/RESEARCH_2026-11-09-performance.md) · [KakuDrop 案例適配](docs/RESEARCH_2026-11-09-kakudrop.md) · [製作周邊與交付](docs/RESEARCH_2026-11-09-postproduction.md) · [封存與協作維護](docs/RESEARCH_2026-11-09-stewardship.md)

## 九個劇組技能

以 Foyege24 的微表演、空間與接鏡方法為核心，附完整配套目錄：

| 技能 | 用途 |
| --- | --- |
| [film-production](skills/film-production/SKILL.md) | 製作統籌、副導、工單、排程、測試、成本與交付 |
| [cinematic-screenwriting](skills/cinematic-screenwriting/SKILL.md) | 人物、場次、台詞及導演交接 |
| [foyege-cinematic-direction](skills/foyege-cinematic-direction/SKILL.md) | 導演、眼神、微表情、克制反應、運鏡、預演與接鏡 |
| [set-design](skills/set-design/SKILL.md) | 平面、尺寸檢查、Blender 白模、光線與機位 |
| [mv-presentation](skills/mv-presentation/SKILL.md) | MV 形式、歌曲時間與聲畫呈現 |
| [dance-choreography](skills/dance-choreography/SKILL.md) | 拍表、舞譜、動作和鏡頭交接 |
| [music-designer](skills/music-designer/SKILL.md) | 音樂方向、歌詞節奏、take 比較與混音交接 |
| [song-arrangement](skills/song-arrangement/SKILL.md) | 編曲起伏、譜面及分軌分析腳本 |
| [openmontage](skills/openmontage/SKILL.md) | 既有剪輯／時間線／渲染工具的執行介面 |

服化道、燈光、場記、DIT、VFX、調色、聲音等部門也有交接卡。[完整職能、實際工具與依賴](docs/SKILL_SUITE.md)。純文字規劃不需 GPU 或 API key；生成、渲染及剪輯沿用使用者既有且可用的工具，模型與素材另行準備。

## 安裝至 Codex 或 Claude

需要 Git 與 Python 3.10+。先取得專案，再安裝完整九技能；以下在 PowerShell 執行：

```powershell
git clone https://github.com/teateatea03/foyege-cinematic-studio.git
Set-Location foyege-cinematic-studio
$env:PYTHONUTF8 = '1'
python tools/install_suite.py --destination "$env:USERPROFILE/.codex/skills"
```

Claude 使用相同目錄格式，將 destination 改為其技能根目錄，例如 `$env:USERPROFILE/.claude/skills`。安裝器複製完整 references、scripts、assets 與 tests，不只 SKILL.md；不安裝外部工具或模型。

只選導演與編劇可加 `--profile director`；指定技能可用 `--skills set-design`，會補齊套件依賴。遇到任一既有同名目錄會在複製前停止，先比較及備份後再更新，不覆蓋舊安裝。新技能於下一次技能清單載入時可用；若未出現，重開工作階段。

## 使用

```text
使用 $foyege-cinematic-direction，把這場戲拆成鏡頭。
重點是目光先移、頭後跟，嘴角恢復後仍留一點張力。
先給導演卡、模型動作稿與接鏡狀態，採用我的既有資源。
```

```text
使用 $cinematic-screenwriting，寫一場兩人在車站道別的短戲。
完成後交給 $foyege-cinematic-direction，保留沉默與反應。
```

[幾何預演命令](skills/foyege-cinematic-direction/references/spatial-previs.md) 使用相對專案路徑與使用者指定的工具入口。輸出目錄由讀者建立為全新位置。

運鏡需求可用 [運鏡與表情](skills/foyege-cinematic-direction/references/camera-movement.md)：推拉、搖攝、跟拍、環繞、變焦、移焦，連同用途、速度、落定、表情可見區間及接鏡。[研究與本機幾何核對](docs/RESEARCH_2026-11-09-camera-movement.md)

[劇組職能與缺口盤點](docs/CREW_CAPABILITY_AUDIT_2026-11-09.md) 對照 22 組常見職能，重用既有編劇、製作與場景配套；新增跨部門排程、服化道具重置、光色、聲音 cue 及 VFX／後期返回卡。單鏡需求按需使用。

[HyperFlow H3 Flash 教學補強](docs/RESEARCH_2026-11-09-hyperflow-flash.md)：新增壓縮模型分流、參考圖責任、少步數試產與聲音分項驗收；5080 推論仍待測。

[Drama3 語音導演台補強](docs/RESEARCH_2026-11-09-drama3-voice.md)：新增固定選角、三份文字、聲音上下文、局部重配與角色分軌交接，連回觸發詞與微表情；未做音質評比或模型推論。

## 證據與限制

2026-11-09 補齊 SAM3D／RefMod，已完成 5080 推論、GLB／Blender 表情快照及 RefMod 儲存／讀檔／生成。完整參考可作基準，pooled16 出現臉眼失真；瞳角色轉接、長鏡與精準微表情仍待驗收。[結果、版本與六份 API 工作流](docs/experiments/2026-11-09-sam3d-refmod/README.md)

2026-11-03 的單機紀錄包含六個 Wan take、341 個原生影格。開眼淺笑、淺笑轉移與固定機位的保持表情續接有觀察紀錄。精確的眼先頭後、真人驅動、正式角色身份與歌曲同步仍待各案驗證。[條件與限制](skills/foyege-cinematic-direction/references/local-tests.md)

公開包提供文字、腳本與測試摘要。作者影片、角色圖片、模型權重及本機完整實驗媒體由原始來源或各自資產管理。歷史紀錄的結論屬指定條件，公開讀者需自行重現。

## 驗證

Python 3.10 以上安裝 PyYAML 後，在專案根目錄執行。

```text
python -m pip install -r requirements-dev.txt
python tools/validate.py
python tools/test_install_suite.py
```

驗證涵蓋技能 YAML、內部連結、JSON 與 Python 語法。文字案例另見 [驗證範圍](docs/VALIDATION.md)。模型生成與 Blender 渲染需另外執行。

## 來源與授權

Foyege24 是本專案導演方法的主要研究來源。作者原作品與名稱權利由原權利人保有，專案由維護者獨立整理。[來源脈絡](PROVENANCE.md) · [授權註記](NOTICE.md) · [MIT](LICENSE)
