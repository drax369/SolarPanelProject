from pathlib import Path
import json
from collections import defaultdict

print("aggregate_results.py STARTING")

pred_path = Path("outputs/predictions.json")
print("Reading from:", pred_path)

with pred_path.open() as f:
    detections = json.load(f)

print("Num detections:", len(detections))

by_image = defaultdict(lambda: {
    "panel_count": 0,
    "total_area": 0.0,
    "max_conf": 0.0,
    "min_conf": 1.0,
    "sum_conf": 0.0,
})

for det in detections:
    x1, y1, x2, y2 = det["bbox_xyxy"]
    conf = det["confidence"]
    area = (x2 - x1) * (y2 - y1)

    info = by_image[det["image"]]
    info["panel_count"] += 1
    info["total_area"] += area
    info["sum_conf"] += conf
    info["max_conf"] = max(info["max_conf"], conf)
    info["min_conf"] = min(info["min_conf"], conf)

for image, info in by_image.items():
    avg_conf = info["sum_conf"] / info["panel_count"]
    print(
        image,
        "| panels:", info["panel_count"],
        "| total_area(px^2):", round(info["total_area"]),
        "| avg_conf:", round(avg_conf, 3),
        "| max_conf:", round(info["max_conf"], 3),
        "| min_conf:", round(info["min_conf"], 3),
    )
