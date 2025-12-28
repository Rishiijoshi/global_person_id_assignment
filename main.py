# main.py
import os
from datetime import datetime, timedelta
import pandas as pd
from id_manager import GlobalIDManager

FPS = 30
ZONE = "Office_Zone"

def frame_to_timestamp(frame):
    return (datetime.utcnow() + timedelta(seconds=frame / FPS)).isoformat()

def load_class_index(root):
    for r, _, files in os.walk(root):
        for f in files:
            if f.lower() == "class_index.txt":
                mapping = {}
                with open(os.path.join(r, f)) as file:
                    for line in file:
                        k, v = line.strip().split(",")
                        mapping[int(k)] = v
                return mapping
    return {}

def generate_detections(root):
    class_index = load_class_index(root)
    detections = []

    for r, _, files in os.walk(root):
        for file in files:
            if not file.endswith(".txt"):
                continue
            if file.lower() in ["class_index.txt", "readme.txt"]:
                continue

            camera_id = "CAM_01" if file.startswith("f_") else "CAM_02"
            path = os.path.join(r, file)

            with open(path) as f:
                for idx, line in enumerate(f):
                    class_id, start, _ = map(int, line.strip().split(","))
                    detections.append({
                        "camera_id": camera_id,
                        "timestamp": frame_to_timestamp(start),
                        "local_track_id": f"{file}_L{idx}",
                        "zone": ZONE,
                        "bbox": [0, 0, 100, 200],
                        "confidence": 1.0,
                        "action": class_index.get(class_id, "Unknown")
                    })
    return detections

if __name__ == "__main__":
    ROOT_DIR = "./data"  # change as needed
    detections = generate_detections(ROOT_DIR)

    manager = GlobalIDManager()
    output = manager.process_detections(detections)

    df = pd.DataFrame(output)
    print(df.head())
