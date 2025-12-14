import os
import pandas as pd
import requests


API_KEY = "AIzaSyAF71xKeFF13D1A8ZHV8foB1upZhRPR7oE"
EXCEL_PATH = os.path.join("data", "input.xlsx")
IMAGES_DIR = os.path.join("images")

IMAGE_ZOOM = 20
IMAGE_SIZE = "640x640"
IMAGE_MAPTYPE = "satellite"

BASE_URL = "https://maps.googleapis.com/maps/api/staticmap"


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def fetch_images_from_excel():
    ensure_dir(IMAGES_DIR)

    df = pd.read_excel(EXCEL_PATH, sheet_name=0)
    df = df.dropna(subset=["latitude", "longitude"])

    print("[DEBUG] df shape:", df.shape)
    print("[DEBUG] full df:")
    print(df)

    if not {"latitude", "longitude", "sample_id"}.issubset(df.columns):
        raise ValueError("Excel must contain 'latitude', 'longitude', 'sample_id' columns")

    image_infos = []

    for idx, row in df.iterrows():
        lat = float(row["latitude"])
        lon = float(row["longitude"])
        sample_id = int(row["sample_id"])
        print(f"[INFO] Fetching image for sample_id {sample_id}: lat={lat}, lon={lon}")

        params = {
            "center": f"{lat},{lon}",
            "zoom": IMAGE_ZOOM,
            "size": IMAGE_SIZE,
            "maptype": IMAGE_MAPTYPE,
            "key": API_KEY,
        }

        resp = requests.get(BASE_URL, params=params)
        print("[INFO] Status code:", resp.status_code)
        resp.raise_for_status()

        img_path = os.path.join(IMAGES_DIR, f"sample_{sample_id}.png")
        with open(img_path, "wb") as f:
            f.write(resp.content)

        image_infos.append(
            {"sample_id": sample_id, "lat": lat, "lon": lon, "image_path": img_path}
        )

    print("[INFO] Done. Saved", len(image_infos), "images.")
    return image_infos


if __name__ == "__main__":
    from pprint import pprint

    infos = fetch_images_from_excel()
    print("Fetched:")
    pprint(infos)
