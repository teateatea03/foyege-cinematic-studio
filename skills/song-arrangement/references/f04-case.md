# F04 案例：先調提示詞

F04 用同一段 88 秒歌詞比較提示詞和譜的來源，全部是原始成品，沒有混音或加層。Owner 聽了 6 首：

> 看來 提示詞的重要性 非常非常的優先
> 1～5 都很不錯
> 6 這個很特別 有種乾淨的感覺 或許codex抓到了精隨？

`A_v4` 之前的評語是「還不錯」。這是 Owner 的耳朵判斷，機器只用來找可能的原因。

## 學到什麼

### 先調提示詞，再動譜和後製

同譜同種子比較 `X3`（Owner 的提示詞）和 `A2`（我寫的樂團提示詞）：鼓點密度 4 組都變高，隨拍起伏 3 組變高，都往 Suno 的範圍靠。我之前在譜和後製上花了很多輪，提示詞卻一路改離 Owner 原本的文字。

### 但不要只歸功於提示詞

Owner 說不錯的 1～5 裡，4 號用的是我的譜，5 號用的是我寫的樂團提示詞。兩個條件各自都有版本被說不錯，所以這輪聽感沒有把「提示詞」和「誰寫譜」完全分開。機器上，自己寫譜讀字比較好，我的譜音高起伏比較大。

### 寫明速度

`X2` 寫約 170 BPM，譜面落在 170–180。`X1` 沒寫，133–196。YuE2 官方技能也說速度要寫在 style。

### 單一種子不算提示詞的效果

P103 之後，同樣的提示詞和自己寫譜跑了 6 個種子，它的半說半唱沒有回來（同音比例最高 .35，P103 .71；連同 `X2`、`X4` 也只到 .42）。第 6 首目前也只有 1 個種子，要先換種子，才能說「乾淨」來自提示詞。

### 文字控制不了每件事

前奏寫了空的 `[Intro]`，18 首自己寫譜裡只有 9 首在前奏寫 3 個音以下。Codex 的文字明寫器樂前奏，譜還是在前奏 12 秒寫了 41 個人聲音符。

## 第 6 首改了什麼

Codex 只換文字，歌詞、種子和其他設定都和 `X2_seed103` 相同：

1. **只描述這段有的內容：** 拿掉第二段、Bridge、最終副歌和整首的情緒走向，並說明這段有哪些部分。
2. **指定樂器分工：** 踢鼓和短貝斯互相配合；主歌只留貝斯和踢鼓；晶片音色只在人聲句子的空隙回應；副歌才打開。

這兩項綁在一起，Codex 自己也說不能分別歸因。

> High-speed playful Japanese electro-pop and hard-edged dance, Taiwanese Mandarin female vocals, about 170 BPM. Tight four-on-the-floor kick locks with short bouncy synth bass; strong sidechain makes room for each kick. Bright wide saw synths carry a short recurring hook, with chiptune replies only in gaps between vocal phrases. This excerpt has an instrumental startup intro, one verse, one pre-chorus, one chorus and a short outro. The verse uses nimble clear female sing-rap with a sparse bass-and-kick groove and dry glitch clicks. The pre-chorus adds rising arpeggios and gated snare rolls, then a brief break before the chorus. The chorus opens into a catchy sustained female melody, stacked vocal responses and the bright synth hook over punchy drums. Finish with an abrupt stop and a short digital reboot sting. Crisp modern electronic production, tight low end, clear vocals.

## 機器在第 6 首看到什麼

在 Owner 聽過的 6 首裡比：

| | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 主歌裡其他樂器的進出幅度（dB） | 16.3 | 24.8 | 27.5 | 22.4 | 32.2 | **44.7** |
| 副歌比主歌多的其他樂器（dB） | 4.6 | 11.1 | 6.7 | 3.1 | 4.1 | **.8** |
| 人聲高過伴奏，4–8 kHz（dB） | .2 | 7.8 | .5 | 3.2 | 5.1 | 7.9 |

- **只有第一列把第 6 首和其他 5 首分開。** 主歌開頭約 10 秒（12–21 秒）沒有持續的合成器，也沒有貝斯。其他樂器約 7 成時間幾乎無聲，只有短促的點綴，所以主要聽到人聲和鼓。來源 `X2_seed103` 同一段相反：人聲加持續的合成器，鼓和貝斯幾乎沒有。文字要的是貝斯加踢鼓，實際上貝斯沒有出現，只對了一部分。這裡要分開看平均和中位數：只看 3 秒平均，其他樂器像是沒有變；我第一次也因此寫錯。
- **第三列 2 號也一樣高，** 所以不足以解釋「乾淨」。
- **第二列是風險。** 第 6 首的副歌增加的其他樂器最少。Owner 以前說過「平」和「樂器不夠多」，所以乾淨不能用副歌打不開來換。

這些只是機器看到的差別，不能證明 Owner 聽到的就是這個。

## 其他使用者的經驗

搜尋結果多是部落格和社群貼文，大多談 Suno，只當假設，要自己對照：

- 建議 style 用少量明確的描述，太多會互相抵消，常見說法是 3–7 個（[Violet Recording](https://violetrecording.com/how-to-write-suno-prompts/)、[Jack Righteous](https://jackrighteous.com/blogs/guides-using-suno-ai-music-creation/how-to-write-better-suno-prompts-without-random-tags)）。
- YuE2 這邊沒找到使用者對 style 寫法的實測回報，只有官方技能和第三方指南。

第 6 首的文字其實不短，所以「越短越好」還沒被驗證，也沒被否定。
