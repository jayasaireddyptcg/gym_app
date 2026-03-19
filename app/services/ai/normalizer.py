EQUIPMENT_DB = {
    "lat pulldown": {
        "id": "LAT_PULLDOWN",
        "muscles": ["lats", "biceps"],
        "instructions": "Pull bar to chest with controlled motion"
    },
    "treadmill": {
        "id": "TREADMILL",
        "muscles": ["legs", "cardio"],
        "instructions": "Walk or run at steady pace"
    },
    "bench press": {
        "id": "BENCH_PRESS",
        "muscles": ["chest", "triceps", "shoulders"],
        "instructions": "Lower bar to chest and press up with controlled motion"
    },
    "leg press": {
        "id": "LEG_PRESS",
        "muscles": ["quads", "glutes", "hamstrings"],
        "instructions": "Push platform away with legs, then return slowly"
    },
    "dumbbells": {
        "id": "DUMBBELLS",
        "muscles": ["arms", "shoulders", "chest"],
        "instructions": "Use controlled movements for various exercises"
    },
    "barbell": {
        "id": "BARBELL",
        "muscles": ["full_body", "compound"],
        "instructions": "Use proper form for lifts like squats, deadlifts, presses"
    }
}

def normalize_equipment(label: str):
    label = label.lower()

    for key in EQUIPMENT_DB:
        if key in label:
            return EQUIPMENT_DB[key]

    return None