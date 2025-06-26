# 🎯 DepthEye 12 – Depth-Aware Object Detection from Video

**DepthEye 12** is a real-time vision system that performs object detection using **YOLOv12** and estimates depth using **MiDaS**. Given a video input, it processes each frame, overlays bounding boxes with class labels and depth estimates, and saves the results as an annotated video.

---

## 🚀 Features

- ✅ Object detection using **YOLOv12**
- 🌊 Monocular depth estimation with **MiDaS DPT-Hybrid**
- 🎞️ Frame-by-frame video analysis
- 🧠 Annotated bounding boxes with labels, confidence, and estimated depth
- 💾 Outputs a processed video with overlays

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **PyTorch**, **Transformers**, **Ultralytics YOLOv12**
- **OpenCV**, **NumPy**
- **MiDaS (Intel ISL)**

---

## 📁 Project Structure

```
├── depth_eye.py         # Main pipeline: detection + depth + overlay + save
├── utils.py             # Frame I/O, overlay, video saving
├── my_types.py          # Box dataclass for bounding boxes + depth
├── requirements.txt     # Python dependencies
├── flake.nix            # Nix environment setup (optional)
├── yolo12n.pt           # YOLOv12 weights file
├── test.mp4             # Example input video
├── out.mp4              # Example output video
```

---

## ▶️ Usage

### 📦 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🎥 2. Run the Detector

```bash
python depth_eye.py --video test.mp4 -o out.mp4
```

- `--video`: Path to the input `.mp4` file
- `--output` or `-o`: Path to save the output annotated video

---

## 📦 Output

- A new video (`out.mp4` by default) will be created.
- Each frame includes:
  - Bounding boxes
  - Class label
  - Confidence score
  - Estimated depth

---

## 🧠 How It Works

1. **YOLOv12** detects objects and returns bounding boxes.
2. **MiDaS** predicts a depth map for the full frame.
3. The system samples depth values from inside each bounding box to estimate object distance.
4. An overlay is drawn on the frame, and all frames are compiled into an output video.

---

## 🧪 Model Notes

- **YOLOv12** weights are automatically downloaded from ultralytics.
- **MiDaS model** (`Intel/dpt-hybrid-midas`) is downloaded automatically from Hugging Face.

---

## 📌 TODOs

- [ ] Add real-time webcam support
- [ ] Add depth-based filtering or alerts
- [ ] Integrate object tracking (e.g., Deep SORT)
- [ ] CLI flag for frame saving instead of video

---

## 🧠 Credits

- [Ultralytics YOLOv5 (base for YOLOv12)](https://github.com/ultralytics/yolov5)
- [Intel MiDaS](https://github.com/isl-org/MiDaS)
- [Hugging Face Transformers](https://huggingface.co/transformers)

---

## 📄 License

MIT License — free to use, modify, and distribute.

