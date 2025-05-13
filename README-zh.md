TennisPlayerAnalysis
[English](/README.md) | [繁體中文 (zh-TW)](/README-zh.md)

## 簡介

TennisPlayerAnalysis 是一套基於 OpenPose 的網球揮拍軌跡標記與分析工具。

* **Label\_pose.py**：讀取影片，自動或手動標記「落地點」、「最高點」、「擊球點」，輸出 CSV 與每球軌跡圖。
* **ShowBoxPlot.py**：將多組球員的擊球水平或高度，繪製成分組箱型圖。
* **ShowScatter\_pose.py**：將每球「落地/最高/擊球點」三點散佈於座標平面，並以顏色區分。

## 功能

1. **自動標記揮拍軌跡**

   * 按 `a` (或自動偵測到球進入畫面) → 開始新一輪
   * 按 `s` → 正常結束，輸出 CSV + 軌跡圖
   * 按 `d` → 結束並標示「受干擾」
   * 按 `q` → 離開程式
   * 按 `z` → 切換自動/手動標記模式

2. **分組箱型圖**

   * 調整參數後，執行 `python ShowBoxPlot.py` 顯示箱型圖

3. **三點散佈圖**

   * 調整參數後，執行 `python ShowScatter_pose.py` 顯示散佈圖

## 安裝與環境要求

1. **Python 版本**：3.10.x
2. **建立並啟動虛擬環境**：

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. **安裝依賴**：

   ```bash
   pip install -r requirements.txt
   ```
4. **OpenPose**
   此程式主要基於 [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) 所開發，由 CMU Perceptual Computing Lab 提供，能即時偵測人體姿態、手勢、表情等。

   * 我們已將 Python binding 及模型打包，請至[此處下載 openpose.zip](https://github.com/KalinLai-void/TennisPoseTrainer/releases/download/OpenPose/openpose.zip)，並解壓縮到 `openpose/` 資料夾下
   * 最終結構需包含：

     * `openpose/python/pyopenpose*.pyd` + 對應的 `.dll`
     * `openpose/models/`（caffemodel + prototxt）

## 資料需求

* **影片檔**：請準備至少一段 MP4 格式的網球揮拍錄影，並將其放在專案內 `demo_videos/` 或指定在 `Label_pose.py` 中的 `file_path`。
* **OpenPose 模型**：確保 `openpose/models/` 裡有正確的 `.caffemodel` 與 `.prototxt`

## 使用範例

* **標記軌跡**：

  ```bash
  python Label_pose.py
  ```

  → 於指定 `file_path` 下產生 `<name>.csv`、`Trajectory/` 圖片、`Clips/` 影片剪輯

* **繪製箱型圖**：

  ```bash
  python ShowBoxPlot.py
  ```

* **繪製散佈圖**：

  ```bash
  python ShowScatter_pose.py
  ```

## 專案結構

```
TennisPlayerAnalysis/
├─ Label_pose.py
├─ ShowBoxPlot.py
├─ ShowScatter_pose.py
├─ requirements.txt
├─ README.md
├─ LICENSE
├─ openpose/
│  ├─ python/         # pyopenpose binding + DLLs
│  └─ models/         # OpenPose 模型檔
└─ demo_videos/       # (選用) 測試用影片
```

## 配置說明

程式開頭的主要參數說明如下，請直接在對應檔案頂端修改：

**Label\_pose.py**

* `file_path`：來源影片或資料夾路徑，預設 `"D:\Lab\…\正拍"`
* `method`：拍法，0=正拍、1=反拍；預設 0
* `is_mutiple_files`：多檔案模式，True=資料夾、False=單檔；預設 True
* `examining_line_percentage_W`：球進入畫面判定線位置（0\~1 之間）；預設 0.85
* `is_auto`：自動標記模式，True/False；預設 False

**ShowBoxPlot.py**

* `sex`：組別，0=男、1=女；預設 0
* `isPoseMode`：原點為姿勢點或地板點，True/False；預設 False
* `people_amount_in_group`：每組人數；預設 3
* `startBall`、`ballAmount_get`：要跳過和要繪製的球序範圍；預設 30、20
* `lang`：語言，0=繁中、1=英；預設 1
* `isVert`：箱型圖方向，True=直向、False=橫向；預設 True

**ShowScatter\_pose.py**

* `method`：拍法，0=正拍、1=反拍；預設 1
* `isShowDistrub`：是否顯示受干擾球，True/False；預設 False
* `isPoseMode`：原點模式，True=姿勢、False=地板；預設 False
* 其他：`isShow2TypeHand`、`isShowNum`、`isShowHightest`、`isShowNumOnLengend`…等，可依註解自行調整


## 授權條款

本專案採用 MIT License，詳見 [LICENSE](./LICENSE)


