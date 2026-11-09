# 可安裝的劇組技能組

九個技能連同 references、scripts、assets 與既有 tests 一起提供。以 Foyege24 為導演核心；製作統籌協調各部門，不另造一套導演方法。對照完整 [22 組職能盤點](CREW_CAPABILITY_AUDIT_2026-11-09.md) 時，區分「有方法與交接」和「工具已實測」。

## 入口與實際內容

| 入口 | 主要工作與附帶內容 |
| --- | --- |
| [film-production](../skills/film-production/SKILL.md) | 製片／副導、十二階段、劇本拆解、鏡頭工單、測試、對白製作、成本、剪接及交付 |
| [cinematic-screenwriting](../skills/cinematic-screenwriting/SKILL.md) | 人物、場次、台詞、有限劇集、時間估算與導演交接 |
| [foyege-cinematic-direction](../skills/foyege-cinematic-direction/SKILL.md) | 微表演、眼神、克制反應、運鏡、接鏡、來源研究；Blender 代理預演與範例 JSON |
| [set-design](../skills/set-design/SKILL.md) | 平面、尺寸、家具／門窗／機位檢查、日光射線、Blender 白模、疊圖與預演轉換 |
| [mv-presentation](../skills/mv-presentation/SKILL.md) | MV 形式、歌曲時間、聲音、文字、人物呈現與案例 |
| [dance-choreography](../skills/dance-choreography/SKILL.md) | 動作語彙、八拍舞譜、拍點影格表腳本、驅動路線與驗收 |
| [music-designer](../skills/music-designer/SKILL.md) | 音樂方向、歌詞節奏、候選比較、局部修訂、分軌／混音與權利交接 |
| [song-arrangement](../skills/song-arrangement/SKILL.md) | 編曲起伏、ABC 統計與四分軌對比腳本、案例及輸入邊界 |
| [openmontage](../skills/openmontage/SKILL.md) | 對接已安裝的剪輯／時間線／渲染工具，核對能力後執行；簡單媒體工作可交 FFmpeg |

## 其他劇組部門如何使用

服裝、妝髮、道具、選角、燈光、跟焦、場記、DIT、VFX、合成、調色、聲音、品管與封存透過 Foyege 的 [跨部門製作](../skills/foyege-cinematic-direction/references/crew-workflow.md) 及 [部門交接卡](../skills/foyege-cinematic-direction/references/department-handoffs.md) 接入。每張卡保留來源版本、起終狀態、責任、驗收及返回條件。按當鏡需要讀取，不要求單鏡載入整套。

這些職能已有工作方法與表單，仍需專案自己的素材、設備、所選工具和專業驗收；不等於內含自動調色師、音訊引擎、角色 rig 或實體特技安全判斷。

## 安裝與依賴

以 [skill-suite.json](../skill-suite.json) 為清單，從 checkout 執行 `python tools/install_suite.py --destination <技能根目錄>`，預設 crew 九項；`--profile director` 只選導演／編劇；`--skills openmontage` 等會加入其套件依賴。相互引用按已訪問集合處理，不是循環執行任務。

安裝複製完整技能目錄，遇到任一同名目錄在複製前停止，保留所有舊安裝。更新先比對／備份，不以本次打包覆蓋本機技能。安裝器不下載模型、不安裝 Python 套件、不啟動服務，也不修改 GPU 工作。

| 需求 | 外部依賴／輸入 |
| --- | --- |
| 文字規劃 | 能載入 SKILL.md 的代理；不需要 GPU、API key 或付費服務 |
| 安裝 | Python 3.10+（stdlib） |
| 套件檢查 | Python + requirements-dev.txt 中的 PyYAML |
| 平面與疊圖 | Python + Pillow |
| 幾何／相機 | Blender，這輪測試版本見驗證紀錄；`--no-render` 不初始化 GPU |
| Cycles 渲染 | 所選且空閒的單張 GPU／可用後端；不因忙碌或 OOM 轉 CPU |
| 拍表／譜面統計 | Python stdlib + 已核對 BPM／第一拍或受支援 ABC |
| 四分軌統計 | numpy、soundfile、librosa + 對齊 stereo WAV，見 [工具邊界](../skills/song-arrangement/references/tools.md) |
| 剪輯／編碼 | 讀者已裝的 FFmpeg／FFprobe、剪輯器或 OpenMontage；OpenMontage 原始碼不隨包附帶 |
| 後製來源／像素／字卡 | source guard 用 stdlib；PNG audit 用 NumPy＋Pillow，字卡用 Pillow＋自有 CJK 字體；[操作與限制](../skills/foyege-cinematic-direction/references/finishing-tools.md)；可選原生校準需已審 T8 原始碼和 PyTorch |
| 實際生成／表演 | 使用者既有素材、模型、節點、聲音與 rig；先核對當前工具能力及授權 |

## 路由例子

- 「整首 MV 如何開工？」進 film-production；歌曲形式未定時接 mv-presentation，按風險選第一個可驗收小段。
- 「只改她忍住委屈的眼神」進 Foyege 微表演，沿用已定劇本，不重跑全製作流程。
- 「房間相鄰鏡頭不像同一間」進 set-design，修同一母本，再更新受影響機位。
- 「副歌已決定跳舞」進 dance-choreography，音檔未鎖定就做 PROVISIONAL 舞譜，不捏造拍點。
- 「只把三段既有素材接起來」用已裝剪輯器／FFmpeg，無需裝音樂模型。

## 來源與未收錄項

相關技能為本專案維護者既有技能的可攜公開版本，個別教材連結及採用範圍保留。OpenMontage 入口為本專案原創介接文件。第三方 action-choreography-reference 尚無可核對的套件授權，故不重發其文字；本包仍有 Foyege 動作因果與舞譜方法。通用 3D 範本、旁白投影片生產套件未作必要依賴。

不包含第三方影片、曲譜摘錄、模型權重、私有角色、虛擬環境、服務登入或私人實驗 runner。已測項及未測項見 [驗證紀錄](VALIDATION.md)。
