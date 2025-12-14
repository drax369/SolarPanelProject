import json
from pathlib import Path

# ---- scale + buffer settings ----
FEET_PER_PIXEL = 0.5  # TODO: replace with your measured value
SQFT_PER_PIXEL2 = FEET_PER_PIXEL ** 2

BUFFER_1 = 1200.0
BUFFER_2 = 2400.0


def bbox_area_sqft(bbox):
    x_min, y_min, x_max, y_max = bbox
    w = max(0, x_max - x_min)
    h = max(0, y_max - y_min)
    return (w * h) * SQFT_PER_PIXEL2


def apply_buffer_rule_for_sample(sample):
    """
    sample: ONE detection from predictions.json
    (flat format with keys: image, bbox_xyxy, confidence, class_id, class_name)
    For now we just compute area_sqft; no true buffer because there is no buffer info yet.
    """
    bbox = sample["bbox_xyxy"]
    area_sqft = bbox_area_sqft(bbox)

    # dummy rule: if area > 0, mark has_solar True with 1200 buffer
    if area_sqft > 0:
        return {
            "has_solar": True,
            "buffer_sqft": BUFFER_1,
            "panel_area_sqft": area_sqft,
        }

    return {
        "has_solar": False,
        "buffer_sqft": BUFFER_2,
        "panel_area_sqft": 0.0,
    }


PRED_PATH = Path("outputs/predictions.json")
OUT_PATH = Path("outputs/predictions_with_buffer.json")


def main():
    print("DEBUG: script started")
    print("DEBUG: expecting predictions at:", PRED_PATH.resolve())

    if not PRED_PATH.exists():
        print("DEBUG: predictions.json NOT FOUND")
        return

    with PRED_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"DEBUG: loaded {len(data)} samples from predictions.json")

    new_data = []
    for i, sample in enumerate(data):
        buffer_result = apply_buffer_rule_for_sample(sample)
        new_data.append({**sample, **buffer_result})
        if i == 0:
            print("DEBUG: first buffer_result:", buffer_result)

    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2)

    print("DEBUG: wrote output to:", OUT_PATH.resolve())


if __name__ == "__main__":
    main()
