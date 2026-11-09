# 來源與採用程度

查閱日期 2026-11-05。多數是製作人文章、教學和訪談的摘要，不是對照實驗。這份技能本身還沒有經過製作人審閱，也還沒有用生成結果驗證。

## 編曲與段落對比

| 來源 | 類型 | 採用內容 |
|---|---|---|
| [Bobby Owsinski：編曲元素](https://bobbyowsinskiblog.com/song-arrangement-elements/) | 混音工程師、作者 | 五種元素；同時響的數量 |
| [Gary Ewer：段落對比 8 法](https://www.secretsofsongwriting.com/2013/06/17/8-ways-of-creating-contrast-between-song-sections/) | 詞曲教學 | 音域、節奏、和聲、人聲的對比 |
| [iZotope：主副歌對比](https://www.izotope.com/en/learn/music-production-tips-to-create-contrast-between-verse-and-chorus) | 廠商教學 | 人聲層數、寬度、頻率內容 |
| [Lost Stories Academy：前副歌](https://loststoriesacademy.com/blogs-and-tutorials/why-pre-choruses-exist) | 製作人學校 | 前副歌的工作；進副歌前變薄 |
| [mastrng：對比](https://mastrng.substack.com/p/contrast-mixing-engineer) | 母帶工程師專欄 | 1–5 dB 的案例；空間和頻率對比 |
| [Splice：活動量](https://splice.com/blog/?p=2821) | 廠商教學 | 用活動量決定誰在前面 |
| [Unison：Future Bass](https://unison.audio/how-to-make-future-bass/) | 音色廠商教學 | 電子音樂層次、人聲切片、前置抽離 |
| [Jack Righteous：Suno 張力](https://jackrighteous.com/de/blogs/guides-using-suno-ai-music-creation/suno-ai-build-intensity-prompt) | AI 音樂使用者 | 能量 1–5、五個槓桿、常見失敗 |

## 日本動畫與偶像歌曲

| 來源 | 類型 | 採用內容 |
|---|---|---|
| [なっさん：アニソン構成](https://note.com/aug_is_the_tonic/n/na02bb265ea17) | 聽眾分析 | 落ちサビ、ラスサビ、Dメロ的意外 |
| [神前暁訪談](https://realsound.jp/2020/04/post-535105_2.html) | 作曲家訪談 | 大量試做、切貼、依作品結構寫歌 |
| [UtaTen：ヒャダイン](https://utaten.com/specialArticle/index/4909) | 樂評，非本人 | 打破結構、轉調、高資訊量 |
| [Real Sound：WEAVER 樂曲分析](https://realsound.jp/2014/05/post-516_2.html) | 樂評 | 不變的部分襯托變化 |
| [Real Sound：中田ヤスタカ](https://realsound.jp/2019/05/post-362554_2.html) | 樂評 | 人聲加工是為了融入音軌 |
| [島村楽器：編曲](https://www.shimamura.co.jp/update/?p=7469) | 樂器行教學 | 各段換鼓型做緩急 |
| [Sound House：王道進行](https://www.soundhouse.co.jp/contents/staff-blog/index?post=891) | 樂器行專欄 | IV–V–iii–vi 常用在副歌 |

## 華語製作人

| 來源 | 類型 | 採用內容 |
|---|---|---|
| [林易祺專訪](https://shopping.harvestmusician.com/blog/MusicProducer202012) | 製作人訪談 | 重複的副歌靠層層疊加、人聲和效果變化 |
| [呂紹淳專訪](https://shopping.harvestmusician.com/blog/Arrangement202105) | 編曲家訪談 | 了解合成器和音色；編曲時就想到混音 |

## 那卡西和演歌感（只作為假說）

| 來源 | 內容 |
|---|---|
| [Nakasi（Wikipedia）](https://en.wikipedia.org/wiki/Nakasi) | 通常由鍵盤和鼓伴奏歌手 |
| [北投那卡西樂手經歷](https://www.twcenter.org.tw/wp-content/uploads/2015/12/g02_18_02_08.pdf) | 從吉他、鼓、歌手三人，到 1990 年起常見的琴師加歌手 |
| [Japanese mode（Wikipedia）](https://en.wikipedia.org/wiki/Japanese_mode) | ヨナ抜き等音階 |

這些資料只確認編制。沒有找到完整的節奏與和聲分析。「F01 聽起來像那卡西是因為編制相近」是推論。

## 工具（尚未實測）

| 工具 | 授權 | 使用者回報 |
|---|---|---|
| [pedalboard](https://github.com/spotify/pedalboard) | GPL-3.0 | 支援外部樂器外掛；有特定 VST3 崩潰的回報（#346） |
| [DawDreamer](https://github.com/DBraun/DawDreamer) | GPL-3.0 | 有 Surge 不出聲的回報（#120，未關閉）；Model D 無法載入，但 pedalboard 可以（#187） |
| [Surge XT](https://github.com/surge-synthesizer/surge) | GPL-3.0 | 開源合成器；在 pedalboard 裡，預設要等編輯器畫面出現才載得進去（pedalboard #394，未關閉） |
| [ACE-Step 1.5 Lego／Complete](https://github.com/ace-step/ACE-Step-1.5) | MIT，base 模型 4.46 GiB | 2026 年 4–6 月有亂音、不同步和雜訊的回報（#1048、#1088、#1255）；8 月改為略過 LM 當預設（#1287），之後沒找到成功的使用回報 |

## 查了但沒取得

- 陳建騏訪談（[關鍵評論網](https://www.thenewslens.com/feature/behind-the-music/267149)）伺服器拒絕讀取，只看到摘要。
- 田中秀和訪談（soundmain）無法連線。
- ヒャダイン本人談《行くぜっ!怪盗少女》編曲的訪談沒有找到。
- 《Sound & Recording》的編曲文章沒有取得全文。
- MusicRadar 的兩篇文章只讀到標題，沒有採用內容。
