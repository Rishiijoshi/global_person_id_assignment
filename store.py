# store.py
import json
import os
from datetime import datetime

class PersonStore:
    def __init__(self, store_path="person_store.json"):
        self.store_path = store_path
        self.persons = {}
        self.local_map = {}
        self.last_id = 0
        self._load()

    def _load(self):
        if os.path.exists(self.store_path):
            with open(self.store_path, "r") as f:
                data = json.load(f)
                self.persons = data.get("persons", {})
                self.local_map = data.get("local_map", {})
                self.last_id = data.get("last_id", 0)
        else:
            self._persist()

    def _persist(self):
        with open(self.store_path, "w") as f:
            json.dump(
                {
                    "persons": self.persons,
                    "local_map": self.local_map,
                    "last_id": self.last_id
                },
                f,
                indent=4
            )

    def generate_new_person_id(self):
        self.last_id += 1
        pid = f"P_{self.last_id:05d}"
        return pid

    def create_person(self, person_id, detection):
        self.persons[person_id] = {
            "person_id": person_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_seen_time": detection["timestamp"],
            "last_camera_id": detection["camera_id"],
            "last_zone": detection["zone"],
            "sightings": 1
        }
        self._persist()

    def update_person(self, person_id, detection):
        person = self.persons[person_id]
        person["last_seen_time"] = detection["timestamp"]
        person["last_camera_id"] = detection["camera_id"]
        person["last_zone"] = detection["zone"]
        person["sightings"] += 1
        self._persist()
