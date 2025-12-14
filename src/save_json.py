from ultralytics import YOLO
from pathlib import Path
import json

# 1) Load model
model = YOLO("runs/detect/train3/weights/best.pt")

# 2) Set image and output dirs
image_dir = Path("images")
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# 3) Collect images
image_paths = sorted(list(image_dir.glob("*.png")) + list(image_dir.glob("*.jpg")))
print("Found images:", [p.name for p in image_paths])

all_results = []

# 4) Run inference and build JSON (manual from boxes)
for img_path in image_paths:
    results = model.predict(source=str(img_path), conf=0.4, verbose=False)
    r = results[0]

    if r.boxes is None or len(r.boxes) == 0:
        continue

    boxes = r.boxes.xyxy.tolist()      # [x1, y1, x2, y2]
    scores = r.boxes.conf.tolist()     # confidence
    classes = r.boxes.cls.tolist()     # class index

    for box, score, cls_id in zip(boxes, scores, classes):
        det = {
            "image": img_path.name,
            "bbox_xyxy": box,
            "confidence": float(score),
            "class_id": int(cls_id),
            "class_name": r.names[int(cls_id)],
        }
        all_results.append(det)

# 5) Save JSON
out_file = output_dir / "predictions.json"
with out_file.open("w") as f:
    json.dump(all_results, f, indent=2)

print(f"Saved {len(all_results)} detections to {out_file}")
