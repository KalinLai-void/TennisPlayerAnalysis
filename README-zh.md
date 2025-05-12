# TennisPlayerAnalysis

[English](/README.md) | [繁體中文 (zh-TW)](README-zh.md)

## 簡介

本專案為【應用智慧辨識技術於精準網球抽球能力提升之研究與實作】之延伸實作，結合背景相減、HSV 分割與 OpenPose 姿勢估計，能自動偵測並標記每次網球擊球動作：

- 擷取擊球起迄影格、落地點、最高點與擊球點  
- 匯出包含這些資訊與姿勢關鍵點的 CSV 檔  
- 產生揮拍軌跡影像與影片剪輯  
- 利用 `ShowBoxPlot.py` 產生箱型圖分析擊球高度／距離  
- 利用 `ShowScatter_pose.py` 產生散佈圖可視化每球重心與擊球位置

此工具適用於研究與教練分析，可快速量化選手正拍與反拍的技術差異與穩定度。  

## 論文參考

**標題**：應用智慧辨識技術於精準網球抽球能力提升之研究與實作 citeturn0file0  
**作者**：賴冠綸、林暐庭、林威成  
**機構**：國立高雄科技大學資訊工程系；高科大教務處體育室  

## 依賴環境

- Python 3.7 以上  
- OpenCV  
- imutils  
- numpy  
- pandas  
- Pillow  
- pyopenpose（需編譯 OpenPose Python）  
- matplotlib  

## 安裝步驟

1. Clone 本專案：  
   ```bash
   git clone https://github.com/<你的帳號>/TennisPlayerAnalysis.git
   cd TennisPlayerAnalysis
````

2. 建立並啟動虛擬環境：

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   ```
3. 安裝相依套件：

   ```bash
   pip install -r requirements.txt
   ```
4. 下載並放置 OpenPose Python 模組與模型：

   * 將編譯後的 `openpose/python` 與 `openpose/models` 資料夾放至專案根目錄下 `openpose/`。

## 設定說明

於 `Label_pose.py` 開頭區段調整：

```python
file_path = r"D:/Lab/YourFolder"      # 影片資料夾或單檔路徑
is_multiple_files = True               # True=處理資料夾, False=單支影片
openpose_path = r"./openpose/python"  # OpenPose Python lib 路徑
openpose_model_path = r"./openpose/models"  # 模型資料夾
method = 0  # 0=正拍, 1=反拍
examining_line_percentage_W = 0.85      # 偵測基準線位置比例
is_save_video = True                    # 是否儲存每球原始與結果影片
is_get_complete_trajectory = False      # 是否繪製完整軌跡
is_auto = False                         # 是否自動觸發按鍵
```

確保 `pyopenpose` 可於 Python 中匯入。

## 執行方式

### 1. 標記與追蹤

```bash
python Label_pose.py
```

* 輸出 CSV 檔 (Index、File、Time、StartFrame、EndFrame、GroundPoint、HightestPoint、HitPoint、PoseKeyPoints)
* 在 `Trajectory/` 產生軌跡圖，於 `Clips/Origin`、`Clips/Result` 儲存每球影片剪輯

### 2. 箱型圖分析

```bash
python ShowBoxPlot.py
```

* 可於檔案頂端設定 `sex`、`startBall`、`ballAmount_get`、`isVert` 等參數

### 3. 散佈圖分析

```bash
python ShowScatter_pose.py
```

* 可於檔案頂端設定 `method`、`isShowDistrub`、`isPoseMode` 等參數

## 專案結構

```
TennisPlayerAnalysis/
├── Label_pose.py         # 標記與追蹤主程式
├── ShowBoxPlot.py        # 產生箱型圖
├── ShowScatter_pose.py   # 產生散佈圖
├── requirements.txt      # 套件清單
├── openpose/             # OpenPose Python 與模型
├── README.md             # 英文說明
└── README-zh.md          # 繁體中文說明 (本檔)
```

## 貢獻指南

1. Fork 本專案
2. 建立新分支：`git checkout -b feature/YourFeature`
3. 提交修改：`git commit -m 'Add feature'`
4. 推送分支：`git push origin feature/YourFeature`
5. 開啟 Pull Request

## 授權條款

採用 MIT License，詳見 [LICENSE](LICENSE)。

```
```

