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

## 兩個技能

- [foyege-cinematic-direction](skills/foyege-cinematic-direction/SKILL.md) 是主入口，負責分鏡、微表演、預演、提示詞與接鏡。
- [cinematic-screenwriting](skills/cinematic-screenwriting/SKILL.md) 將前提轉為人物選擇、場次與台詞，交接給主入口。

純文字規劃可直接使用。實際生成先核對使用者擁有的素材、模型、節點與負載。Blender 工具是可選的幾何預演，需要可用的 Blender 執行檔。

## 安裝至 Codex

將本專案網址交給 Codex，要求安裝上述兩個技能即可。使用 Codex 內建安裝器時，在 Windows PowerShell 執行以下命令，需已有 Python。

```powershell
$env:PYTHONUTF8 = '1'
py "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo teateatea03/foyege-cinematic-studio --path skills/foyege-cinematic-direction skills/cinematic-screenwriting
```

安裝器遇到既有同名目錄會停止。更新前先比較現有版本與本專案內容。新技能於下一輪正常載入時可被使用。

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

## 證據與限制

2026-11-09 補齊 SAM3D／RefMod，已完成 5080 推論、GLB／Blender 表情快照及 RefMod 儲存／讀檔／生成。完整參考可作基準，pooled16 出現臉眼失真；瞳角色轉接、長鏡與精準微表情仍待驗收。[結果、版本與六份 API 工作流](docs/experiments/2026-11-09-sam3d-refmod/README.md)

2026-11-03 的單機紀錄包含六個 Wan take、341 個原生影格。開眼淺笑、淺笑轉移與固定機位的保持表情續接有觀察紀錄。精確的眼先頭後、真人驅動、正式角色身份與歌曲同步仍待各案驗證。[條件與限制](skills/foyege-cinematic-direction/references/local-tests.md)

公開包提供文字、腳本與測試摘要。作者影片、角色圖片、模型權重及本機完整實驗媒體由原始來源或各自資產管理。歷史紀錄的結論屬指定條件，公開讀者需自行重現。

## 驗證

Python 3.10 以上安裝 PyYAML 後，在專案根目錄執行。

```text
python -m pip install -r requirements-dev.txt
python tools/validate.py
```

驗證涵蓋技能 YAML、內部連結、JSON 與 Python 語法。文字案例另見 [驗證範圍](docs/VALIDATION.md)。模型生成與 Blender 渲染需另外執行。

## 來源與授權

Foyege24 是本專案導演方法的主要研究來源。作者原作品與名稱權利由原權利人保有，專案由維護者獨立整理。[來源脈絡](PROVENANCE.md) · [授權註記](NOTICE.md) · [MIT](LICENSE)
