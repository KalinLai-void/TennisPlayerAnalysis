TennisPlayerAnalysis
[English](/README.md) | [繁體中文 (zh-TW)](/README-zh.md)

## Introduction

TennisPlayerAnalysis is a toolkit built on OpenPose for labeling and analyzing tennis stroke trajectories. It enables automatic or manual marking of three key points—ground impact, highest point, and hit point—in video clips, and provides visualizations including CSV output, trajectory images, box plots, and scatter plots.

## Features

1. **Trajectory Labeling (`Label_pose.py`)**

   * Press **a** (or use auto-detect) to start a new stroke.
   * Press **s** to finish normally and export a CSV record + trajectory image.
   * Press **d** to finish and mark as “disturbed.”
   * Press **q** to quit the program.
   * Press **z** to toggle auto/manual labeling mode.

2. **Box Plot Visualization (`ShowBoxPlot.py`)**

   * Draw grouped box plots comparing stroke distances or heights across players.
   * Customizable by gender, origin point (pose vs. ground), number of strokes, orientation (vertical/horizontal), and language (EN/TW).

3. **Scatter Plot Visualization (`ShowScatter_pose.py`)**

   * Plot each stroke’s ground impact, highest point, and hit point on a 2D plane.
   * Color-coded by stroke type; options to display disturbed strokes and annotate point indices.

## Installation & Requirements

1. **Python**: 3.10.x
2. **Create & Activate a Virtual Environment**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **OpenPose**
   This project relies on [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) for real-time pose estimation.

   * Download the Python bindings and models from:
     [https://github.com/KalinLai-void/TennisPoseTrainer/releases/download/OpenPose/openpose.zip](https://github.com/KalinLai-void/TennisPoseTrainer/releases/download/OpenPose/openpose.zip)
   * Extract into the `openpose/` folder so that it contains:

     * `openpose/python/pyopenpose*.pyd` and required `.dll` files
     * `openpose/models/` (Caffe `.caffemodel` and `.prototxt`)

## Data Requirements

* **Video Clips**: Prepare one or more MP4 videos of tennis strokes. Place them in `demo_videos/` or set the `file_path` variable in `Label_pose.py` accordingly.
* **OpenPose Models**: Ensure the `openpose/models/` directory contains all required model files.

## Usage

1. **Label Trajectories**

   ```bash
   python Label_pose.py
   ```

   Output: CSV file in the `file_path` directory, `Trajectory/` images, and optional video clips in `Clips/`.

2. **Generate Box Plots**

   ```bash
   python ShowBoxPlot.py
   ```

3. **Generate Scatter Plots**

   ```bash
   python ShowScatter_pose.py
   ```

## Project Structure

```
TennisPlayerAnalysis/
├─ Label_pose.py
├─ ShowBoxPlot.py
├─ ShowScatter_pose.py
├─ requirements.txt
├─ README.md          # English
├─ README-zh.md       # Traditional Chinese
├─ LICENSE
├─ openpose/
│  ├─ python/         # pyopenpose binding + DLLs
│  └─ models/         # OpenPose model files
└─ demo_videos/       # Example video clips
```

## Configuration Parameters

Edit these at the top of each script to customize behavior:

**Label\_pose.py**

* `file_path`: Path to video file or folder (default: `"D:\Lab\…\正拍"`).
* `method`: Stroke type, 0=forehand, 1=backhand (default: 0).
* `is_mutiple_files`: Folder mode if True, single-file mode if False (default: True).
* `examining_line_percentage_W`: Threshold line for ball entering screen (0–1) (default: 0.85).
* `is_auto`: Auto-label mode if True, manual if False (default: False).

**ShowBoxPlot.py**

* `sex`: Group, 0=men, 1=women (default: 0).
* `isPoseMode`: Use pose point or ground point as origin (default: False).
* `people_amount_in_group`: Number of players per group (default: 3).
* `startBall`, `ballAmount_get`: Indices range for strokes to plot (default: 30, 20).
* `lang`: Language, 0=TW, 1=EN (default: 1).
* `isVert`: Vertical if True, horizontal if False (default: True).

**ShowScatter\_pose.py**

* `method`: Stroke type, 0=forehand, 1=backhand (default: 1).
* `isShowDistrub`: Show disturbed strokes if True (default: False).
* `isPoseMode`: Origin mode, True=pose, False=ground (default: False).
* Additional flags: `isShow2TypeHand`, `isShowNum`, `isShowHightest`, `isShowNumOnLengend` for plot options.


## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.


