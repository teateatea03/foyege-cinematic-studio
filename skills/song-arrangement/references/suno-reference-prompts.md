# Owner 的 Suno 提示詞與對照

2026-11-05 Owner 提供，並附上 Suno 版本《被迫閃耀》兩首當參考。Suno 的音訊只能拿來量測，不能進任何生成流程。這些文字先前的風險判斷在最後一節。

## 提示詞原文

中文：

> 高速日系電音流行與俏皮硬派舞曲, 約 170 BPM, 明亮鋸齒合成器, 彈跳低音, 緊密四拍踢鼓與故障切片音效, 開頭用冷淡機械女聲與簡約啟動音, Drop 突然炸開, 主歌採清晰快速女聲半說半唱, 預副歌逐層堆疊節奏與合成器, 副歌轉成大聲, 易記的合唱式旋律與閃亮舞台音色, 第二段加入密集 rap flow 和 glitch stutter, Bridge 突然抽空伴奏, 親密柔和地獨白, 隨後升調, 加速堆疊進入最終大合唱, 結尾急停後接乾冷機械對白與短促重啟音效, 女聲表演從機械克制, 俏皮焦躁到真摯脆弱再回到爆發, 現代清晰, 強烈側鏈, 低頻緊實, 合成器寬闊

英文：

> High-speed Japanese virtual idol electro-pop with Taiwanese Mandarin lyrics, playful frantic cyberpunk comedy and a sudden sincere emotional bridge, Open with dry robotic female system-voice spoken lines over sparse startup beeps, then a hard punchy electronic drop, Verses use rapid nimble female sing-rap over driving four-on-the-floor kick, sharp synth bass, glitch clicks and chiptune accents; build with rising arpeggiators and tightly gated snare rolls, Explosive sticky idol chorus with bright stacked female harmonies, chant responses, distorted error-code stutters and dense festival synths, Second verse has very fast articulate rap and glitch edits, Drop to intimate near-silent spoken bridge with soft keys and close-miked vulnerable female voice, then slam into a higher-key final chorus with layered choir-like idol doubles and maximal drums, End abruptly into a dry spoken comic outro with a short digital reboot sting, Crisp, loud, tightly edited modern electronic production, strong section contrasts, clear Mandarin diction; preserve the provided lyric sheet and all its section cues

## 我後來寫的提示詞偏離了哪裡

| | Owner 的提示詞 | 我給 F03 `A2` 的提示詞 |
|---|---|---|
| 類型 | 電音偶像 | 動畫片頭流行搖滾，「真樂團」 |
| 主歌唱法 | 快速半說半唱 | 明寫 `melodic singing rather than rapping` |
| 節奏核心 | 四拍踢鼓、強烈側鏈、合成貝斯 | 原聲感鼓、撥弦貝斯、電吉他 |
| 速度 | 「高速」，中文版約 170 BPM | 寫「Fast」，實際靠譜面的 190 BPM |
| 音色事件 | 故障切片、錯誤碼 stutter、起音琶音 | 吉他悶音、強力和弦、弦樂銅管 |

## 目前最值得記住的一條線

Owner 唯一點名「完全不同」的聲音是 S06 的 `P_seed103`。它的來源是：

- **提示詞：** 這段英文提示詞，只略為縮短（1041 字）。
- **作曲：** 沒有給譜，YuE2 自己寫。
- **譜的特徵：** 190 BPM，9 小節器樂前奏，快速半說半唱，同音比例 71%（其他生成譜多半 .1–.4）。

之後我把提示詞改寫成 S07 的 `W`，沒有寫速度。模型自己寫的譜只剩 108–145 BPM，Owner 聽成「那咖西的調調」。只有套用 P103 譜的 `WL`、`WS` 例外。到 F03 我又改成樂團。

**這不能證明自己作曲一定比較好：**

- P 的其他種子不像 P103，其他樂器佔比只有 2–5%，所以有運氣成分。
- VocalRender 同音比例高的譜，曾被評為像在念字。同音比例不是配方。
- F03 Owner 選 A（我的副歌）勝過 B（P103 副歌），但兩者的風格提示也不同，不能單獨歸因於副歌。

## 這次量到的

量測對象是 Suno 三版分離出的人聲，分離工具相同，但可能有伴奏外洩。歌詞位置用滑動 ASR 找，所以是約略值。

| 主歌前 8 句 | Suno 三版 | 我的 6 首 |
|---|---|---|
| 3 kHz 以上比全頻 | -6.5 至 -7.2 dB | -9.9 至 -13.0 dB |
| 明顯低於主要音量的時間 | .04–.05 | .10–.15 |
| 每秒明顯斷開次數 | 1.37–1.49 | 1.08–1.72 |

- 人聲比較亮是目前唯一明顯差異。把我的人聲加亮 3、5 dB，機器讀字沒有變好，這個差異可能來自外洩或唱法，不是 EQ 能補。
- Suno 的音節沒有比較常斷開。我從頻譜圖得到的第一印象，數字不支持。
- 「最初」在 Suno 也不穩。`(1)` 有一個起點讀對，其他起點和另外兩版讀成最精緻、最近、在出租間、飛車，所以這兩個字放在開頭本來就難。
- 「交易策略」在無編號版和 `(1)` 都讀對，`(2)` 只讀到「交易」。

版本名稱對應檔名：無編號版是 `被迫閃耀.mp3`，`(1)`、`(2)` 是 `被迫閃耀 (1).mp3`、`被迫閃耀 (2).mp3`。

## 這段文字能不能用

2026-11-02 讀過 Suno 條款（生效日 2026-09-03）：Output 定義為音訊和影像，沒有提到文字，使用者保有自己提交的內容，包含文字。所以這不屬於音訊禁令。只有在這段文字是 Suno 寫的，而且該條款優先時才不確定。S06 是 Owner 知道這點後批准的。批准只限當次，再用要再問。

F04（2026-11-05）：我問「要批准 F04（回到你的 Suno 提示詞比較，含再次使用這段文字）嗎？」，Owner 回「工單 我也批准」。這次批准同樣只限 F04。
