import cv2 as cv
import pathlib
import numpy as np
from my_types import Box
from typing import Any

def read_video(file_path: pathlib.Path) -> list[np.ndarray]:
    file = str(file_path)
    cap = cv.VideoCapture(file)
    if not cap.isOpened():
        raise OSError(f"{file} couldn't be opened")
    
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    
    cap.release()
    return frames

def extract_yolo_info(class_names: dict[int, str], data: Any)->list[Box]:
    boxes = data[0].boxes
    results = []
    for box in boxes:
        cls_id = int(box.cls)
        label = class_names[cls_id]
        box_cls = Box(label, x1=int(box.xyxy[0][0]), y1=int(box.xyxy[0][1]), x2=int(box.xyxy[0][2]), y2=int(box.xyxy[0][3]))
        results.append(box_cls)
    return results
    
def overlay_image(frame: np.ndarray, boxes: list[Box])->np.ndarray:
    for box in boxes:
        label = f"{box.cls} {box.depth:.2f}"
        cv.rectangle(frame, (box.x1, box.y1), (box.x2, box.y2), (0, 255, 0), 2)
        (text_w, text_h), _ = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv.rectangle(frame, (box.x1, box.y1 - text_h - 4), (box.x1 + text_w, box.y1), (0, 255, 0), -1)
        cv.putText(frame, label, (box.x1, box.y1 - 2), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return frame

def save_video(filename: pathlib.Path, frames: list[np.ndarray])-> None:
    path = str(filename)
    fps = 30
    height, width = frames[0].shape[:2]
    frame_size = (width, height)
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(path, fourcc, fps, frame_size)
    for frame in frames:
        out.write(frame)
    out.release()

