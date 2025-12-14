from config import SQFT_PER_PIXEL2


BUFFER_1 = 1200.0
BUFFER_2 = 2400.0


def bbox_area_sqft(bbox):
    x_min, y_min, x_max, y_max = bbox
    w = max(0, x_max - x_min)
    h = max(0, y_max - y_min)
    return (w * h) * SQFT_PER_PIXEL2


def apply_buffer_rule_for_sample(sample):
    """
    sample: one record from predictions.json
    must contain list of panels with 'bbox',
    'overlap_px2_1200', 'overlap_px2_2400'
    """
    panels = sample.get("panels", [])

    # 1) try 1200 sq ft
    best_p = None
    best_overlap = 0.0
    for p in panels:
        ov_px2 = p.get("overlap_px2_1200", 0.0)
        ov_sqft = ov_px2 * SQFT_PER_PIXEL2
        if ov_sqft > best_overlap:
            best_overlap = ov_sqft
            best_p = p

    if best_p is not None and best_overlap > 0:
        return {
            "has_solar": True,
            "buffer_sqft": BUFFER_1,
            "panel_area_sqft": bbox_area_sqft(best_p["bbox"]),
            "panel_bbox": best_p["bbox"],
        }

    # 2) else try 2400 sq ft
    best_p = None
    best_overlap = 0.0
    for p in panels:
        ov_px2 = p.get("overlap_px2_2400", 0.0)
        ov_sqft = ov_px2 * SQFT_PER_PIXEL2
        if ov_sqft > best_overlap:
            best_overlap = ov_sqft
            best_p = p

    if best_p is not None and best_overlap > 0:
        return {
            "has_solar": True,
            "buffer_sqft": BUFFER_2,
            "panel_area_sqft": bbox_area_sqft(best_p["bbox"]),
            "panel_bbox": best_p["bbox"],
        }

    # 3) no solar
    return {
        "has_solar": False,
        "buffer_sqft": BUFFER_2,
        "panel_area_sqft": 0.0,
        "panel_bbox": None,
    }
