# 外部執行環境

OpenMontage 是外部軟體，原始來源為 [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage)。本套件只發布原創介面技能，沒有重新散布上游程式或複製其內部階段技能。

在目前使用環境查找 OpenMontage checkout 及其公開入口；openmontage 全域命令可能是本機包裝器，不是所有上游安裝的既有介面。先讀實際 help／文件。不可用時依上游當前文件安裝，或使用已有剪輯器。不要複製另一台電腦的 checkout／venv 路徑，也不把 PowerShell 包裝器的存在當成 Python、renderer 和 provider 都通過。

需保留並核對：

- 實際軟體 revision、Python／Node／渲染器及 CLI 回傳狀態。
- 所選 pipeline／manifest、目前 provider 契約、可用輸入輸出與圖文／音訊能力。
- 當前工程與品牌、角色、語音及發布規則；共用工具不覆寫它們。
- 已接受素材、主音軌、字幕、時間線與真正使用的版本／雜湊。
- 顯卡只使用明確指定且可用的裝置；文件準備不啟動渲染，忙碌不自動改 CPU 或停其他工作。

status／capabilities 的成功只支持該次探測範圍。真正組裝、渲染、字幕與聲音仍需用代表性素材實測並檢查產物。沒有外部 provider 時不自動改成雲端。

若只需格式檢查、安裝本技能或閱讀方法，不必啟動 OpenMontage、ComfyUI、Docker 或 GPU。
