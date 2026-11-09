# 九技能套件驗證：2026-11-09

這輪驗證的是公開套件可安裝、引用完整，以及附帶工具能執行。Foyege24 仍是導演核心，沒有把劇組文件的存在當成整片已驗收。

## 實際結果

| 檢查 | 結果與範圍 |
| --- | --- |
| 整套安裝 | 九個完整技能目錄複製到全新目錄，檔案逐一與公開來源比對 |
| 選裝 | 逐一選九個入口，遞迴補齊依賴後，所有 Markdown 相對檔案連結均在安裝目錄內存在 |
| 碰撞 | 任一同名技能已存在時，整批先停止；舊檔與其餘目錄不變 |
| 安裝測試 | tools/test_install_suite.py 五項通過，含循環依賴及未收錄依賴拒絕 |
| 技能格式 | 九項 quick_validate.py 全通過；套件驗證涵蓋 YAML、JSON、Python AST、相對連結和環境資料掃描 |
| 拍表 | 120 BPM／24fps／零起算小節與 clip frame，CLI 成功輸出；未測實曲拍點偵測 |
| 譜面統計 | 兩段原創 ABC fixture，重複音、休止、和弦與 inline 轉調統計成功 |
| 平面 | sample_room.json：1 PASS、1 WARN、0 FAIL；WARN 為 C2 位於房間外需拆 S 牆；已查看繁中平面圖及機位圖 |
| 日光 | 既有九項幾何單元測試通過，涵蓋窗朝向、牆厚、遮擋與窗楣；非完整照度驗證 |
| 場景白模 | Blender 5.2.3 LTS，--no-render 成功保存 .blend／日光報告；7 PASS、1 WARN、0 FAIL。C2 的 A1 可見面取樣僅 20%，該角度仍待調整，不當成可拍鏡頭 |
| 場景 → 導演預演 | to_previs.py 匯出 C1，Foyege build_previs.py --no-render 建出 121 格／24fps／1280×704 工程與 manifest，rendered=false、device=NONE |
| 四分軌分析 | arc_compare.py 在 40 秒合成 stereo PCM fixture 完成 CLI；四軌均為 22050 Hz、882000 frames、16bit，data chunk 對齊。只測輸入／分析路徑，未做人聲、聽感或真實歌曲品質驗收 |
| 既有本機安裝 | 六個打包來源技能共 42 檔 SHA-256 與操作前紀錄一致，公開版整理未寫回來源 |
| 機密與變更 | Gitleaks 無洩漏；git diff --check 通過；模型、媒體與私人環境未打包 |

執行 Python 3.13.11，PyYAML 6.0.3、Pillow 12.2.0、numpy 2.4.6、soundfile 0.13.1、librosa 0.11.0；這些是本輪環境紀錄，不是最低版本保證。[摘要資料](verification.json)

## 重現入口

從 checkout 執行，將 OUT_* 換成尚不存在的輸出位置，Blender 使用自己的入口。實際運作時用安裝後的技能路徑取代 skills/。

```text
python tools/validate.py
python tools/test_install_suite.py
python tools/install_suite.py --destination OUT_SKILLS
python skills/set-design/scripts/plan_check.py --set skills/set-design/assets/sample_room.json --out OUT_PLAN
python skills/set-design/scripts/to_previs.py --set skills/set-design/assets/sample_room.json --camera C1 --out OUT_PREVIS_JSON
blender --background --factory-startup --python-exit-code 1 --python skills/set-design/scripts/build_set.py -- --set skills/set-design/assets/sample_room.json --out OUT_SET --no-render
blender --background --factory-startup --python-exit-code 1 --python skills/foyege-cinematic-direction/scripts/build_previs.py -- --scene OUT_PREVIS_JSON --out OUT_PREVIS --no-render
python skills/set-design/tests/test_sunlight_check.py
```

GPU 當時滿載，故本輪沒有渲染、模型生成、影片重製或中斷其他工作。OpenMontage 僅驗證可安裝的介接文件，未執行外部 runtime。未進行代理模型行為評測、完整舞蹈、實曲混音、正式角色表演、整片剪輯或最終視聽驗收；詳見各技能原有證據邊界。
