# 優先工具：已跑通的入口與限制

2026-11-09 在 RTX 5080 16GB 以隔離環境完成字幕、空間標記與 MMAudio 擬音短測。以下是可重用介面與該次條件；安裝技能不會自動安裝第三方 runtime 或權重。角色、聲音、主時間線仍沿用專案正本。

## 字幕：本地 CUDA CLI

[translate_srt.py](../scripts/translate_srt.py) 呼叫 Index Translate 的外部 `index_translate_core`；只在這個程序載入指定的套件目錄。需要已驗證的官方 2B 模型、相容的 GPU PyTorch，以及隔離的 Transformers 5.17.0／tokenizers 0.23.1／safetensors 0.8.0。使用者指定其他版本時，先核對相容性。參數必須指向實際存在的目錄。

在技能根目錄執行，以下路徑以自己的環境替換：

```powershell
python -X utf8 scripts/translate_srt.py source.zh.srt result.en.srt `
  --vendor "<Index Translate source>/_vendor" `
  --packages "<isolated Python packages>" `
  --model "<models>/Index-Translate-2B" `
  --cuda-device "<authorized GPU UUID>" `
  --source zh --target en --glossary glossary.json
```

- 僅處理已有時間碼的 SRT；ASR 是另一個步驟。指定單張 CUDA 裝置，顯存不足或 CUDA 不可用就停止，不偷偷改 CPU。
- 輸出 UTF-8 BOM，保留 cue 編號／時間碼；可加 `--bilingual`。輸出與同名 receipt 已存在時拒絕覆蓋。
- 目前支援純文字及整句 `<i>`／`<b>`／`<u>`。格式留在程式側，只有正文進模型；混合行內樣式或 ASS 控制碼在載入模型前拒絕，需人工整理。
- 詞彙表只帶入本 cue 確實出現的來源詞。實測將無關人物詞彙加進所有 cue 曾引發加戲；這個範圍限制降低該次失敗，不是語意正確保證。
- receipt 保留模型 revision、實際裝置、精度、版本、每 cue 結果、耗時及待審狀態。`acceleration.cpu_reference` 是上游可選 kernel 回退標籤；本次模型呼叫為 CUDA／BF16，並有實際 CUDA 記憶體紀錄，不把這個標籤解讀為整個模型在 CPU。

八條 GPU 短測保持所有編號、時碼與斜體；可攜 CLI 的輸出與已核對版本逐位元組相同。「排練」被譯為較寬泛的 training，正式字幕仍須語意與可讀速度審稿。不可把未審譯文直接覆蓋正式字幕或沿用新配音的舊詞級表情時間。

## 空間標記：預演先用

自有示意圖 [marker_fixture.png](../assets/priority-crew/marker_fixture.png)、[標記預處理 API 圖](../assets/priority-crew/marker_preprocess.api.json)、[單鏡生成 API 圖](../assets/priority-crew/marker_generation.api.json)。前處理圖不載入擴散模型；生成圖需要外部 T8 H3 節點、既有 Ref2VA INT8、Ref2V Turbo4、H3 NVFP4 Qwen 及音／影 VAE。另附由真實瀏覽器匯出的 [UI 圖](../assets/priority-crew/marker_generation.ui.json)。上傳素材並按實際節點核對後才執行。

該次 512×288、90 幀、24fps、4 步、seed 611091101，真實 Picture 1 綁定通過。六個不同時間的抽樣圖顯示單人向門前目標移動，末幀雙腳位於目標區；青／黃框仍存在。這支只具預演與走位試片資格，沒有乾淨成片、細緻微表情、雙人或全段步態品質資格。沒有做 clean 圖對照，不宣稱標記相對普通文字的提升率。

更換圖片／裁切後，舊 `expected_source_sha256` 不能沿用。該欄比較的是實際 float32 IMAGE 位元組，與 PNG 檔 hash 或 RGB8 hash 不同；先用編輯器核對，或明示人工 authoring 並清空欄位。保留底圖、框、圖例和實際 Picture 順序。換成正式角色時重新驗收身份、眼神、動作與殘框。

## 擬音：MMAudio 隔離路線

[六節點 API 圖](../assets/priority-crew/foley_generation.api.json)／[UI 圖](../assets/priority-crew/foley_generation.ui.json) 使用外部 MMAudio 節點與 large 44k v2、CLIP、Synchformer、VAE、BigVGAN 權重。將 `LoadVideo` 改成自己的靜音片；`duration` 必須等於整個輸入影格批次所涵蓋的秒數，提示詞同步改成實際事件。保存獨立音軌，原畫面經後期旁路接回。

本機隔離副本有一項時間取樣修正：原節點取批次前 N 幀作 8fps／25fps 特徵，120 幀／5 秒輸入會被縮為 4.8 秒；CLIP 只看到前段。修正版以 `floor((i / target_fps) * input_frames / duration)` 在整個來源時間上取樣，容許重複幀補足特徵頻率。CUDA 影格 ramp 校準得到完整 5 秒、40 CLIP／125 sync 幀。這份修正僅在該隔離副本，公開包不含第三方節點原始碼；其他安裝先核對取樣實作，不能只見同名節點就套用實測資格。

一次 5 秒靜音自然動作短測完成，輸出 44.1kHz 單聲道、221184 samples（約 5.0155 秒）。原檔保留，供剪輯的副本裁掉尾端 684 samples 至精確 220500 samples；PCM block alignment 通過，聲畫合片保留原壓縮視訊 packet 位元組。未聽審，不宣稱自然、無意外人聲或接觸時序已被接受。不得以 waveform／解碼通過代替聽辨。

H3 Foley 所需指定混合權重未在本次本機清單中找到，因此沒有冒用其他 H3 權重做它的驗收；先用既有 MMAudio 補齊擬音能力，H3 分支仍是候選。

## 準備與回復

使用獨立的 ComfyUI user／input／output 與本機埠、明確 whitelist 外部節點，避免測試入口接管原工作區。主環境的 Torch／Transformers、現有節點與私人 GPU 規則不因這份技能而改變。任務完成關閉自己啟動的測試服務，保留模型、收據、失敗紀錄及候選。

來源：[T8 H3 固定版本](https://github.com/T8mars/comfyui-minimax-h3-audio-T8/tree/3a23f333537d9a715aad7ce79af8d9ec891d9ad8)、[Index 適配固定版本](https://github.com/T8mars/Comfyui-Index-Translate-T8/tree/5beac49cd0f8e125f0ca00cb5eba6bc2b7ed265a)、[本機 MMAudio 來源版本](https://github.com/kijai/ComfyUI-MMAudio/tree/8eaeb72edc3aaf2059b57f2d96a1f6f689f19ae2)、[MMAudio 權重](https://huggingface.co/Kijai/MMAudio_safetensors/tree/5984623e6b436818c6ff287ef6eec93e3e05aa3f)、[BigVGAN](https://huggingface.co/nvidia/bigvgan_v2_44khz_128band_512x/tree/95a9d1dcb12906c03edd938d77b9333d6ded7dfb)。程式、模型及素材條款各自保留；試片素材不打包。
