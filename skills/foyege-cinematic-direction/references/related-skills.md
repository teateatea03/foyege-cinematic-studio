# 同類技能研究與採用範圍

2026-11-03 檢閱六個公開技能專案的相關原文。以下連結固定至當次 commit，閱讀範圍列於各項。外部技能的工作法經本機流程適配，新增方法目前只有文件與案例檢查，影像效果待可用 GPU 與實際素材驗證。

## R1 中文表情演繹

`dashian1/biaoqing-yanyi-skill`，讀取完整 SKILL.md。借用「台詞對誰說、想改變什麼」來設計語氣與可見反應。轉入 [微表演](microacting.md) 的台詞目的欄。其固定畫幅、真人風格、情緒曲線與時長按作品另定。GitHub 未辨識授權，保留連結並以本技能自己的工作卡整理。[原始技能](https://github.com/dashian1/biaoqing-yanyi-skill/blob/2a58fed6affdfec1f3ee75431d231e3ae749e130/SKILL.md)

## R2 導演分鏡與剪接

`wuwangzhang1216/DirectorSKILL`，MIT。閱讀主技能的劇情節拍、關鍵幀、工具適配段，以及剪接與故障診斷的相關段落。採用入鏡／出鏡配對設計及按故障層修正，補入 [製作](production.md)。原文固定裁頭尾影格與統一把手秒數可能刪掉微反應，本技能依事件位置和音軌決定保留範圍。[主技能](https://github.com/wuwangzhang1216/DirectorSKILL/blob/c65ae0d14457053efb1e354c7e7f7e120d97fad1/SKILL.md) [剪接原文](https://github.com/wuwangzhang1216/DirectorSKILL/blob/c65ae0d14457053efb1e354c7e7f7e120d97fad1/references/editing-and-assembly.md) [診斷原文](https://github.com/wuwangzhang1216/DirectorSKILL/blob/c65ae0d14457053efb1e354c7e7f7e120d97fad1/references/failure-modes.md)

## R3 分鏡連續性檢查

`jerrymama123/storyboard-continuity-guard-skill`，讀取完整 SKILL.md。採用參考圖職責、空間地標、註記與成片圖分離的檢查，補入 [空間預演](spatial-previs.md)。手別、道具持有與 POV 可見範圍依劇情保留。GitHub 未辨識授權，以原創欄位整合方法。[原始技能](https://github.com/jerrymama123/storyboard-continuity-guard-skill/blob/cc9e8be140e4f318aeddcbc471b6c39aa9d2a30a/SKILL.md)

## R4 局部臉部動作與表情參考

`OSideMedia/higgsfield-ai-prompt-skill` 的 `higgsfield-facs`，MIT。閱讀來源界線及表情參考規劃段。借用按場景挑選少量表情狀態的思路。作者也將 Seedance 解讀 AU 碼列為經驗性提示慣例。本機採可見變化描述，AU 到 rig／控制節點的映射需另有實證。[原始技能](https://github.com/OSideMedia/higgsfield-ai-prompt-skill/blob/6a6a5dd105d285782dd6992692be4d8b3825ca13/skills/higgsfield-facs/SKILL.md)

## R5 人物微表情分鏡

`Roselfish/persona-microexpression-master`，閱讀流程、靜態表情檢查與素材分析段。其終點是靜態分鏡。借用表情方向、幅度、身份分項檢查，並增加本機所需的動態時序驗收。工具名稱與逐步確認流程屬原宿主設計。GitHub 未辨識授權，以自行撰寫的檢查欄位整合。[原始技能](https://github.com/Roselfish/persona-microexpression-master/blob/7ffbcd118df0280b1a0f9944103229482463da88/SKILL.md)

## R6 資產基準與交接

`0xhughs/director-skills`，MIT。讀取根路由、golden image 與 continuity handoff 文件。採用乾淨身份基準、場景與道具狀態交接，補入 [參考圖職責](spatial-previs.md)。本機沿用已接受資產，依鏡頭缺口選圖。[主技能](https://github.com/0xhughs/director-skills/blob/35ca0a2b4cd55b0668aa9ea0f40273324b774bb4/SKILL.md) [參考基準](https://github.com/0xhughs/director-skills/blob/35ca0a2b4cd55b0668aa9ea0f40273324b774bb4/skills/character-location-prop-bible/references/golden_image_workflow.md) [狀態交接](https://github.com/0xhughs/director-skills/blob/35ca0a2b4cd55b0668aa9ea0f40273324b774bb4/skills/short-film-development/references/continuity_handoff.md)

## 整合後的證據界線

- 臉部代碼與情緒名稱只作設計註記。精確控制以實際模型介面、rig 映射與輸出驗證為準。
- 表情靜幀能檢查形態與身份。反應順序、停頓和接鏡仍需連續影像。
- 視線承接以世界目標與當前機位推導。雙人反打常呈相向眼線，逐鏡判斷畫面左右。
- 本機原有六次短測與使用者觀看紀錄保留於 [local-tests.md](local-tests.md)。本次研究新增的工作卡屬待測設計。
