# 驗證範圍

2026-11-07 公開整理使用 CPU 檢查套件。tools/validate.py 通過：2 個技能、67 個內部連結、1 份 JSON、2 份 Python、24 份文字檔，零錯誤。兩個技能的 quick_validate.py 均回報有效。qtools secrets 掃描約 99.67 KB，沒有命中；啟發式掃描不能保證完全無秘密。

## 可重現結構檢查

在根目錄執行 python tools/validate.py，檢查兩個技能 YAML、內部檔案／標題連結、JSON、Python 語法及常見私人位址模式。這不是全面的秘密掃描或模型行為評測。另使用 Codex 維護的 quick_validate.py 檢查兩個技能，並執行 Gitleaks 掃描。

## 行為與核心審查

文字案例涵蓋眼先頭後、克制淺笑與反打接鏡。以導演卡、參考責任、可讀中間狀態及已接受 take 狀態進行檢查。公開版保留 Foyege 主技能與自含編劇配套，原始安裝及私人創作專案不受此套件修改。

這些案例是文字行為審查，不能證明影片模型能精確照做。

## 媒體與運算限制

歷史六個 take 的參數及觀察見 [短測紀錄](../skills/foyege-cinematic-direction/references/local-tests.md)。原生影格總數 341，示範是靜音技術片；精確眼頭延遲、真人驅動、正式角色身份與歌曲同步仍待測。

本次發布沒有啟動 ComfyUI、載入 GPU 模型或重跑媒體推論。Blender 腳本保持原有 CPU 渲染實作；本次只檢查 Python 語法與資產 JSON，沒有重新渲染。完整連續播放、可懂語音、聲畫同步及最終影片品質須在實際製作中驗收。
