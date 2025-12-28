# Global Person ID Assignment Module (Task-3)

## Overview
This module assigns persistent Global Person IDs across multiple cameras using
time and zone-based re-identification.

IDs follow the format:
P_00001, P_00002, ...

## Features
- Cross-camera re-identification
- Persistent IDs across runs
- JSON-backed person store
- Clean API for pipeline integration

## Core APIs
- assign_person_id(detection)
- process_detections(detections)

## Matching Logic
1. Same camera + same local track → reuse ID
2. Same zone + time difference ≤ 5 seconds → reuse ID
3. Otherwise → create new ID

## Persistence
Person records are stored in `person_store.json`:
- person_id
- created_at
- last_seen_time
- last_camera_id
- last_zone
- sightings count

## How to Run
```bash
python main.py
