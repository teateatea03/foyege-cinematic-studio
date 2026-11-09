# 三項優先工具：隔離部署與 5080 短測

2026-11-09。接續 [T8 頻道調查](../../RESEARCH_2026-11-09-t8-channel.md)，把字幕、走位標記與擬音做成可操作入口。[操作方式、配套圖與限制](../../../skills/foyege-cinematic-direction/references/priority-crew-setup.md)；[機讀結果](results.json)。Foyege 的微表演、因果和接鏡方法保持核心。

## 已完成與資格

| 工具 | 真實執行 | 可使用範圍 |
|---|---|---|
| Index Translate 2B | RTX 5080 CUDA／BF16；可攜 CLI 完整跑 8 cue；與已核對版本輸出逐位元組相同 | 本地字幕翻譯初稿、編號／時碼與整句斜體保留；正式發布前仍需審稿 |
| H3 Visual Marker | 四個節點可載入；實際 native Picture 綁定；512×288、90 幀、24fps、4 步、seed 611091101 | 六個抽樣時間顯示單人到點；青／黃框殘留，只列預演試片，不列乾淨成片或微表情驗證 |
| MMAudio | 補齊四個 FP16 權重與 BigVGAN，固定 revision／LFS hash；5 秒靜音自然動作片完成一次生成 | 音檔及合片技術通過，音質、意外人聲和動作同步尚未聽審接受 |

H3 Foley 原指定混合權重未在本機找到；先重用既有 MMAudio 的節點與環境完成擬音能力。沒有用另一個 H3 模型冒稱完成原配方，也沒有改專案主音軌。

## 實際問題與修正

1. 原始 SRT 模型輸入的格式占位符失配，整次輸出被拒絕，未寫入半成品。自有介面改為程式保留整句樣式；混合行內樣式在載入前停止。
2. 全詞彙表出現在每條字幕時，第 8 條曾自行產生人物台詞。改成只帶入當前 cue 出現的來源詞；保留失敗版本。[來源 8 條](subtitle-smoke.zh.srt)、[詞彙表](subtitle-glossary.json)、[最後 GPU 輸出](subtitle-smoke.en.srt) 可直接比較。第 6 條 training 比「排練」寬泛，不把輸出當精確定稿。
3. 標記圖的來源綁定比較 float32 IMAGE，而非 RGB8 位元組；錯誤 hash 被拒絕。核對實際張量後前處理及 native 綁定通過。該次成功不提供相對 clean 圖的成功率。
4. 已有 MMAudio 的前綴取幀把 120 幀／5 秒縮為 4.8 秒，CLIP 只覆蓋前段。僅在隔離來源修正為按來源時間取樣。真實 CUDA ramp 校準顯示 5 秒、40 CLIP／125 sync 幀，末幀接近來源尾端。這是時間取樣測試，不是人耳同步評分。
5. MMAudio 原生輸出 221184 samples／44100Hz（約 5.0155 秒）。保存原件；供回剪的副本只裁尾端 684 samples，成為精確 5 秒。PCM sample-frame alignment 通過；合片的壓縮視訊 packet hash 與原靜音片一致。

## 隔離與驗證

- 使用原 ComfyUI Python／Torch，另設 user／input／output／本機埠和 custom-node whitelist。字幕專屬套件目錄只由該程序載入，沒有全域 .pth，也沒有覆蓋主 Transformers 5.9.0。
- H3／字幕／擬音與 CUDA ramp 測試依次使用 5080，沒有使用或停啟 3080 Ti 的工作。
- 真實瀏覽器分別載入標記 19 節點與擬音 6 節點，沒有 Missing／error node。新隔離 profile 存在 optional CSS／template-list 404 與離線 release-check CSP 錯誤，沒有宣稱 console 零錯誤。
- 四項自有字幕介面回歸測試涵蓋格式不進模型、cue 詞彙範圍、拒絕混合格式與保留已有輸出。它們不代表翻譯模型通用品質。CUDA CLI、GPU 模型執行與 Agent 文字／靜幀檢視分列。
- 新增模型檔依固定來源逐檔核對大小與 hash；沿用的 H3 權重本輪未重新雜湊；新增 safetensors 檢查 header。上游程式僅在本機隔離目錄，公開包包含自有介面、原創圖與圖形 fixture、SRT 案例及測量結果。

## 素材與未完成驗收

擬音參考為 [Jane pouring beer／Angulidayaaluta](https://commons.wikimedia.org/w/index.php?title=File:Jane_pouring_beer.webm&oldid=1253219481)，CC BY-SA 4.0。23–28 秒選段縮為 512×288／24fps，原聲完全移除；本地生成聲音合片沿用 CC BY-SA 4.0 並註記修改。公開庫不含這份原片或衍生聲畫檔。標記用平面人物／門口示意圖由本專案程式繪製。

本輪沒有完整觀看標記片的步態／每幀連續性、沒有聽審擬音，也沒有正式角色或微表情驗收。只有通過相應內容審查的輸出才能進正式連續性帳。服務測完關閉，保留啟動入口和收據供後續使用。
