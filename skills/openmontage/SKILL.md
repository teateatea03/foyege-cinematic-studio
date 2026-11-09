---
name: openmontage
description: 使用已安裝的 OpenMontage 組裝多階段影片、時間線、動態圖文、渲染與品管；簡單裁切或轉碼直接用既有 FFmpeg。先核對執行環境與實際 provider，不預設雲端或模型已可用。
---

# 剪輯與製作執行介面

本技能是原創路由，連到外部 OpenMontage 執行環境；不包含該軟體、模型或服務。完整製作規劃沿用 [film-production](../film-production/SKILL.md)，表演與接鏡沿用 [Foyege](../foyege-cinematic-direction/SKILL.md)。單純圖像編輯不走這條路線。

## 先核對可用入口

需要組裝或渲染時，讀 [執行條件](references/runtime.md)，找目前 OpenMontage checkout 或其 CLI。若有 `openmontage` 命令，先讀其 help／文件；只有實際提供 `status`、`capabilities`、`runtimes` 的包裝器才使用這些子命令。它們是研究環境的便利入口，不保證每份上游安裝都具備。

未提供這些子命令時，依實際 checkout 的指南查能力與啟動方式，不自行發明相同命令。實際 checkout、環境、渲染器及 provider 以目前文件與輸出為準。依該 checkout 的 AGENTS.md、AGENT_GUIDE.md 及所選 pipeline 的階段指南執行，不把本技能當作上游命令的替代規格。沒有 CLI 時保留時間線與素材計畫，使用已可用的剪輯器或 FFmpeg 完成其能處理的部分，不假稱 OpenMontage 已執行。

## 選執行層

- 複合製作、選片與時間線、生成素材整合、動態圖文、渲染和 QC：選實際可用的 OpenMontage pipeline。
- 一次明確的 trim、concat、crop、overlay、probe 或 transcode：直接用既有 FFmpeg／FFprobe。
- 使用者已指定剪輯器或工作流：保留其工程與時間基準；OpenMontage 可作下游，不另建相衝突的正本。
- 可用 provider 僅是能力線索；不因此下載模型、改 ComfyUI、建立憑證或提交付費生成。沿用本次已授權工具及本機優先規則。

## 回交

交回實際時間線／manifest、使用的 shot／take 與 source 範圍、工作版本、渲染輸出、實際檢查及未完成項。原檔與衍生檔分開，幀率、變速、聲道、字幕及顯示處理保持可追溯。

依 [素材與成片驗收](../foyege-cinematic-direction/references/media-handoff.md) 分查檔案、內容、原速播放與聽審。可解碼不等於聲音可懂；敘述型輸出有語音時另查 PCM sample-frame 對齊、逐段辨識／人類回聽與聲畫同步。

本技能只提供介面與交接方法。新機器的端到端生成、渲染與發布需要各自的實際環境、素材及授權，不由安裝此技能自動取得。
