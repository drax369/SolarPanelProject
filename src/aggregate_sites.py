import json
from collections import defaultdict
from pathlib import Path

PRED_BUF_PATH = Path("outputs/predictions_with_buffer.json")
OUT_SITE_PATH = Path("outputs/site_summaries.json")

# simple QC threshold in sq ft (tune this)
MIN_VERIFIABLE_AREA = 200.0

def main():
    if not PRED_BUF_PATH.exists():
        print("predictions_with_buffer.json not found:", PRED_BUF_PATH.resolve())
        return

    with PRED_BUF_PATH.open("r", encoding="utf-8") as f:
        detections = json.load(f)

    by_image = defaultdict(list)
    for det in detections:
        by_image[det["image"]].append(det)

    site_records = []

    for image, dets in by_image.items():
        # keep only detections with has_solar True
        solar_dets = [d for d in dets if d.get("has_solar", False)]

        if not solar_dets:
            # no solar for this image
            site_records.append({
                "image": image,
                "has_solar": False,
                "panel_area_sqft": 0.0,
                "buffer_sqft": 0.0,
                "qc_status": "NOT_VERIFIABLE",
            })
            continue

        # choose detection with max panel_area_sqft
        best = max(solar_dets, key=lambda d: d.get("panel_area_sqft", 0.0))

        area = best.get("panel_area_sqft", 0.0)
        buffer_sqft = best.get("buffer_sqft", 0.0)

        if area >= MIN_VERIFIABLE_AREA:
            qc_status = "VERIFIABLE"
        else:
            qc_status = "NOT_VERIFIABLE"

        site_records.append({
            "image": image,
            "has_solar": True,
            "panel_area_sqft": area,
            "buffer_sqft": buffer_sqft,
            "qc_status": qc_status,
        })

    with OUT_SITE_PATH.open("w", encoding="utf-8") as f:
        json.dump(site_records, f, indent=2)

    print("Wrote site-level summaries to:", OUT_SITE_PATH.resolve())

if __name__ == "__main__":
    main()
