from argparse import ArgumentParser
import pathlib
from utils import read_video, overlay_image, save_video
import numpy as np
from my_types import Box
from ultralytics import YOLO
from transformers import DPTImageProcessor, DPTForDepthEstimation
import torch
from utils import extract_yolo_info
from tqdm import tqdm
class DetectionDepthModel:
    def __init__(self)->None:
        self.yolo = YOLO("yolo12n.pt")
        self.class_names = self.yolo.names
        self.midas = DPTForDepthEstimation.from_pretrained("Intel/dpt-hybrid-midas", low_cpu_mem_usage=True)
        self.preprocess_midas = DPTImageProcessor.from_pretrained("Intel/dpt-hybrid-midas")
    def _call_yolo(self, image: np.ndarray)->list[Box]:
        data = self.yolo(image)
        boxes = extract_yolo_info(self.class_names, data)
        return boxes

    def _call_midas(self, image: np.ndarray)->torch.Tensor:
        inputs = self.preprocess_midas(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = self.midas(**inputs)
            predicted_depth = outputs.predicted_depth
        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=image.shape[:2],
            mode="bicubic",
            align_corners=False,
        )
        return prediction
    def __call__(self, image: np.ndarray)->list[Box]:
        boxes = self._call_yolo(image)
        depth_image = self._call_midas(image).squeeze()
        for box in boxes:
            depth_crop = depth_image[box.y1:box.y2, box.x1:box.x2]
            if depth_crop.numel() > 0:
                depth_value = float(torch.mean(depth_crop))  # If it's a torch tensor
            else:
                depth_value = 0.0
            box.depth = depth_value
        return boxes


def detect_object_and_depth(model: DetectionDepthModel, frame: np.ndarray)->list[Box]:
    boxes = model(frame)
    return boxes



def main()->None:
    parser = ArgumentParser(prog="DepthEye is a tobject tracker with depth information")
    parser.add_argument("--video", help="path to a mp4 video", type=pathlib.Path)
    parser.add_argument("-o", "--output", help="path to the save the video", type=pathlib.Path, default=pathlib.Path("out.mp4"))
    args = parser.parse_args()
    video = read_video(args.video)
    model = DetectionDepthModel()
    frames = []
    for i, frame in tqdm(enumerate(video)):
        boxes = detect_object_and_depth(model, frame)
        img = overlay_image(frame, boxes)
        frames.append(img)
    save_video(args.output, frames)
if __name__ == "__main__":
    main()
