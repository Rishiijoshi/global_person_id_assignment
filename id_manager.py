# id_manager.py
from datetime import datetime
from store import PersonStore

class GlobalIDManager:
    def __init__(self, store_path="person_store.json", time_threshold=5):
        self.store = PersonStore(store_path)
        self.time_threshold = time_threshold

    def assign_person_id(self, detection):
        local_key = f"{detection['camera_id']}::{detection['local_track_id']}"
        det_time = datetime.fromisoformat(detection["timestamp"])

        # 1️⃣ Exact local-track match
        if local_key in self.store.local_map:
            pid = self.store.local_map[local_key]
            self.store.update_person(pid, detection)
            detection["person_id"] = pid
            return detection

        # 2️⃣ Time + zone re-identification
        for pid, person in self.store.persons.items():
            last_seen = datetime.fromisoformat(person["last_seen_time"])
            time_diff = abs((det_time - last_seen).total_seconds())

            if (
                time_diff <= self.time_threshold and
                person["last_zone"] == detection["zone"]
            ):
                self.store.local_map[local_key] = pid
                self.store.update_person(pid, detection)
                detection["person_id"] = pid
                return detection

        # 3️⃣ New person
        new_pid = self.store.generate_new_person_id()
        self.store.local_map[local_key] = new_pid
        self.store.create_person(new_pid, detection)
        detection["person_id"] = new_pid
        return detection

    def process_detections(self, detections):
        return [self.assign_person_id(d) for d in detections]
