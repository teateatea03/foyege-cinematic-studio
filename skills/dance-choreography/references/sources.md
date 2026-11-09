# 來源與可信度

查證日期 2026-11-05。「讀過」是直接讀了頁面；「摘要」只看到搜尋結果的摘要，全文沒讀，引用前要再查。

## 編舞方法

| 來源 | 程度 | 採用 |
|---|---|---|
| Chuyun Oh, K-pop Dance: Music Video Choreography（Cambridge 專書章節）、[K-pop Dance](https://routledge.com/product/isbn/9781032079394)（Routledge, 2022） | 摘要 | 主打動作的定義和設計條件 |
| [Marie Claire 訪問 KATSEYE 編舞師 Grant Gilmore、Sohey Sugihara](https://www.marieclaire.com/culture/music/katseye-performance-directors-grant-gilmore-sohey-sugihara-interview) | 摘要 | 副歌簡單可重複，複雜動作放其他段落；通常要改很多版 |
| [Motif Development 課堂教材](https://westleigh-high.schudio.com/files/School_Closure_Work/Year_10/Dance/Week1/Motif_Development_Powerpoint.pdf)、[Brainscape 卡片](https://www.brainscape.com/flashcards/10807768/packs/19202220) | 摘要，次級來源 | 動作發展手法。Smith-Autard、Humphrey 原著沒讀，術語定義各處不一 |
| [Artlist：Tips for Making a Dance Video](https://artlist.io/blog/tips-for-making-a-dance-video/)、[No Film School](https://nofilmschool.com/2018/06/creative-camera-moves-and-transitions-you-can-use-your-next-music-video)、[God's Ballroom：How to edit dance videos](https://godsballroom.com/misc/how-to-edit-dance-videos.html) | 摘要 | 不必每拍切；切點跟樂句和歌詞；鏡頭要配合舞蹈 |
| `sw-format-adaptation`、`ai-short-drama-screenwriter`、`foyege-cinematic-direction`（本機技能） | 讀過相關段落 | 每場要改變什麼；舞蹈按可見事件排時間；MV 鏡頭標記與足部接地 |

時間、空間、身體和喜劇段落有一部分是編寫者的綜合判斷，沒有逐條來源，尚未經舞者審視。沒有找到編舞師逐步公開做法的一手資料，也沒有讀到 MIKIKO 談副歌與鏡頭的一手訪談。

## 生成與動作來源

| 來源 | 程度 | 採用 |
|---|---|---|
| 本機 M01（HitomiVideoStudio #36 `6647135848`）；Owner 判定（`6647756471`）：「能用 但也只是證明 能用再流程上 不是整體」 | 親自量測 | H3 的速度、方向、結束狀態、臉部細節。只證明能放進流程 |
| Foyege `references/local-tests.md` T05、T06 | 讀過 | Wan Animate 2 的本機設定和接續方式，但只有淺笑 |
| [Comfy：Wan Animate 2](https://blog.comfy.org/p/wan-animate-2-is-now-available-in) | 讀過 | 直接讀驅動影片。頁面沒寫長度、解析度、VRAM 的限制 |
| [Comfy-Org/Wan-Animate-2](https://huggingface.co/Comfy-Org/Wan-Animate-2) | 讀過 | Apache-2.0 標示；上游授權檔未讀 |
| [wanx-troopers 使用者筆記](https://wanx-troopers.github.io/wan-animates.html) | 讀過 | 身形比例、延伸約 3 次後變差、姿態偵測比較。個別使用者的說法 |
| [SCAIL-2 論文](https://arxiv.org/html/2606.10804v1) | 摘要 | 作者說不適合特寫，指標是作者自評。本機沒有這個模型 |
| [MMD-Blender/blender_mmd_tools](https://github.com/MMD-Blender/blender_mmd_tools) | 讀過 | Blender 4.2–5.2，GPL-3.0 |
| [Mixamo FAQ（2022）](https://community.adobe.com/t5/mixamo-discussions/mixamo-faq-licensing-royalties-ownership-eula-and-tos/td-p/13234775) | 摘要，已過時 | 只作提醒，使用前查現行條款 |
| [Kimodo](https://research.nvidia.com/labs/sil/projects/kimodo/docs/getting_started/quick_start.html)、[HY-Motion 1.0](https://arxiv.org/html/2512.23464)、[OpenDance](https://arxiv.org/abs/2506.07565v2) | 摘要 | 只列為待查候選，沒有直接讀 LICENSE |

使用者經驗的缺口：沒有找到用 Wan Animate 2 跳舞的第一手報告。其他 AI MV 的經驗見 [binwang](https://binwang.me/2026-01-02-Music-Video-Generation-with-AI.html)，它用單一靜態場景避開鏡頭間矛盾。

## 看過但不採用的技能

- [high-dynamic-video-choreographer](https://skills.sh/amao2001/ganloss-latent-space/high-dynamic-video-choreographer)，讀過
- [motion-choreographer](https://claudskills.com/skills/motion-choreographer/SKILL.md)，讀過
- [ClawHub dance-video](https://clawhub.ai/skills/dance-video)，摘要，被標為可疑
