# Rooftop Solar Panel Detector

This project is an end-to-end pipeline for detecting rooftop solar panels in aerial or satellite images using a lightweight YOLOv8-nano model.[web:288][web:289][web:302] It runs object detection, converts pixel-level bounding boxes into real-world area estimates, applies configurable buffer rules, and flags each site as VERIFIABLE or NOT_VERIFIABLE for solar installation suitability.[web:294][web:297][web:303]

## Features

- Fast YOLOv8-nano inference suitable for CPU or GPU deployment.[web:302]
- Works with tiled aerial or satellite imagery at various resolutions.[web:295]
- Converts bounding box dimensions into approximate panel area in square feet or square meters.[web:297]
- Adds a rule-based buffer around panels for safety and clearance requirements.[web:303]
- Aggregates detections per rooftop and exports a clean CSV or Excel report.[web:292]

## Tech Stack

- Python 3.x
- Ultralytics YOLOv8
- NumPy and Pandas for post-processing and reporting[web:295]

## Getting Started

Clone the repository:

git clone <your-repo-url>
cd <your-repo-folder>

Create a virtual environment and install dependencies:

python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

Prepare your input imagery:

- Place test images in a folder such as `data/images`.[web:292]
- Update any configuration or script paths as needed.

Run inference:

python infer.py --weights weights/best.pt --source data/images --out_dir outputs

The script saves detection visualizations and a CSV or Excel file containing panel area, buffer, and VERIFIABLE / NOT_VERIFIABLE status for each site.[web:297]

## Project Structure

- `infer.py`: main script for running detection and post-processing
- `config/`: configuration files for model and buffer rules
- `weights/`: YOLOv8-nano weight files
- `data/`: input images and intermediate data
- `outputs/`: final visualizations and reports

## Use Cases

This tool supports rapid rooftop screening for solar feasibility at neighbourhood, campus, or city scale, helping planners, installers, utilities, and researchers evaluate solar potential from aerial imagery.[web:294][web:297] It can also be used for educational projects in geospatial AI and renewable energy analysis.[web:295]

## Acknowledgements

This project builds on the YOLOv8 ecosystem and open-source work on solar panel mapping from aerial and satellite imagery.[web:288][web:294]

# Project Running Method
# To run everything step by step from solar_project do:
# 1) YOLO prediction
python yolo_detect_predict.py --source images --weights weights/best.pt

# 2) Save detections to JSON
python save_json.py

# 3) Add buffer
python run_buffer_postprocess.py   # or buffer_process.py

# 4) Aggregate by site
python aggregate_sites.py

# 5) Export Excel
python export_to_excel.py

