"""
Canonical gym equipment list (must match AI prompt in equipment routes) plus
rich display data: muscles, exercise ideas, and tips.
"""

from __future__ import annotations

import re
from typing import Any

# Exact strings the model is told to return (lowercase), line-for-line with EQUIPMENT_PROMPT.
ALL_EQUIPMENT_KEYS: frozenset[str] = frozenset(
    {
        "lat pulldown",
        "treadmill",
        "bench press",
        "leg press",
        "dumbbells",
        "barbell",
        "squat rack",
        "leg curl machine",
        "leg extension machine",
        "chest press machine",
        "shoulder press machine",
        "bicep curl machine",
        "tricep pushdown machine",
        "rowing machine",
        "elliptical trainer",
        "stationary bike",
        "stair climber",
        "cable machine",
        "pull up bar",
        "dip station",
        "kettlebell",
        "medicine ball",
        "resistance bands",
        "smith machine",
        "hack squat machine",
        "calf raise machine",
        "ab crunch machine",
        "back extension machine",
        "hip abduction machine",
        "hip adduction machine",
        "preacher curl bench",
        "incline bench",
        "decline bench",
        "roman chair",
        "battle ropes",
        "punching bag",
        "speed bag",
        "boxing ring",
        "yoga mat",
        "foam roller",
        "exercise ball",
        "step platform",
        "rower",
        "assault bike",
        "fan bike",
        "recumbent bike",
        "upright bike",
        "spin bike",
        "cross trainer",
        "arc trainer",
        "versaclimber",
        "jacob's ladder",
        "ski ergometer",
        "rowing ergometer",
        "boxing dummy",
        "heavy bag",
        "double end bag",
        "speed bag platform",
        "jump rope",
        "agility ladder",
        "cone markers",
        "hurdle",
        "medicine ball rebounder",
        "slam ball",
        "sandbag",
        "weight vest",
        "ankle weights",
        "wrist weights",
        "lifting belt",
        "lifting straps",
        "wrist wraps",
        "knee sleeves",
        "elbow sleeves",
        "compression shorts",
        "lifting shoes",
        "chalk bag",
        "water bottle",
        "towel",
        "gym bag",
        "locker",
        "shower",
        "sauna",
        "steam room",
        "hot tub",
        "massage table",
        "stretching area",
        "cool down area",
    }
)


def _slug(key: str) -> str:
    s = key.lower().replace("'", "").replace("-", " ")
    s = re.sub(r"[^a-z0-9]+", "_", s.strip())
    return s.strip("_").upper()


def _title(key: str) -> str:
    return key.replace("'", "'").title()


def _exercise(name: str, muscles: list[str], how: str) -> dict[str, Any]:
    return {"name": name, "muscles": muscles, "how": how}


# Hand-authored detail for common equipment; others use _default_entry().
RICH_OVERRIDES: dict[str, dict[str, Any]] = {
    "lat pulldown": {
        "muscles": [
            "Latissimus dorsi",
            "Teres major",
            "Biceps brachii",
            "Rhomboids / mid-traps",
        ],
        "muscle_variants": "Wider grip and flared elbows bias the lats; a medium neutral grip adds more mid-back; underhand (reverse) grip recruits biceps more.",
        "instructions": "Sit tall, brace your core, and pull the bar to the upper chest with control. Avoid excessive torso swing.",
        "exercises": [
            _exercise(
                "Wide-grip lat pulldown",
                ["Lats", "Teres major"],
                "Pull to the collarbone; pause; resist on the way up.",
            ),
            _exercise(
                "Close neutral-grip pulldown",
                ["Lats", "Biceps"],
                "Elbows track down toward ribs; squeeze shoulder blades together.",
            ),
            _exercise(
                "Single-arm cable pulldown",
                ["Lats", "Core (anti-rotation)"],
                "One side at a time; keep ribs down and torso square.",
            ),
            _exercise(
                "Straight-arm pulldown (cable)",
                ["Lats", "Serratus"],
                "Arms nearly straight; arc the bar down toward thighs.",
            ),
        ],
        "tips": "Adjust thigh pad so you cannot lift off the seat. Stop if you feel sharp shoulder pain.",
    },
    "bench press": {
        "muscles": ["Pectorals", "Anterior deltoids", "Triceps"],
        "muscle_variants": "Flatter bench emphasizes mid chest; slight decline can shift load; grip width changes triceps vs chest emphasis.",
        "instructions": "Retract shoulder blades, feet planted, bar path slightly arched over the chest.",
        "exercises": [
            _exercise(
                "Flat barbell bench press",
                ["Chest", "Triceps", "Front delts"],
                "Touch lower chest; press up and slightly back toward the rack.",
            ),
            _exercise(
                "Paused bench press",
                ["Chest", "Stability"],
                "1-second pause on chest; no bounce.",
            ),
            _exercise(
                "Close-grip bench press",
                ["Triceps", "Chest"],
                "Hands inside shoulder width; elbows tucked.",
            ),
            _exercise(
                "Tempo bench (3-1-1)",
                ["Chest", "Control"],
                "Slow eccentric to build tension and control.",
            ),
        ],
        "tips": "Use a spotter or safety arms. Wrists stacked; avoid flaring elbows excessively.",
    },
    "leg press": {
        "muscles": ["Quadriceps", "Glutes", "Adductors"],
        "muscle_variants": "High foot placement biases glutes/hamstrings; low placement biases quads; stance width hits adductors differently.",
        "instructions": "Lower until hip crease depth allows without pelvis rounding; press through mid-foot.",
        "exercises": [
            _exercise(
                "Standard leg press",
                ["Quads", "Glutes"],
                "Full control; no locking knees violently at top.",
            ),
            _exercise(
                "Single-leg leg press",
                ["Quads", "Glutes", "Stability"],
                "Fix knee tracking over toes; avoid twisting.",
            ),
            _exercise(
                "Feet-high leg press",
                ["Glutes", "Hamstrings"],
                "Push through heels; longer range if mobility allows.",
            ),
            _exercise(
                "Pulse reps (short ROM)",
                ["Quads", "Metabolic burn"],
                "Small range at deepest comfortable depth.",
            ),
        ],
        "tips": "Do not let lower back peel off the pad. Breathe and brace at heavier loads.",
    },
    "cable machine": {
        "muscles": ["Highly variable", "Chest", "Back", "Arms", "Core"],
        "muscle_variants": "Cable height and body angle completely change the line of resistance—use that to bias upper vs lower chest, lats vs rear delts, etc.",
        "instructions": "Set the pulley height for your goal; stand or sit in a stable stance; control the stack.",
        "exercises": [
            _exercise(
                "Cable crossover / fly",
                ["Chest", "Front delts"],
                "Slight bend in elbows; arc hands together at sternum height.",
            ),
            _exercise(
                "Seated cable row",
                ["Mid-back", "Lats", "Biceps"],
                "Pull handle to lower ribs; sit tall.",
            ),
            _exercise(
                "Cable wood chop (high-to-low)",
                ["Obliques", "Core"],
                "Rotate through hips and ribcage with straight arms.",
            ),
            _exercise(
                "Rope tricep pushdown",
                ["Triceps"],
                "Split the rope at the bottom; elbows pinned.",
            ),
        ],
        "tips": "Check cable wear; use smooth strokes—no slamming the stack.",
    },
    "dumbbells": {
        "muscles": ["Full body (exercise-dependent)", "Stabilizers"],
        "muscle_variants": "Unilateral work reduces asymmetry; alternating tempos hit conditioning; seated vs standing changes core demand.",
        "instructions": "Choose a weight you can control for the full ROM; keep wrists neutral where possible.",
        "exercises": [
            _exercise(
                "Goblet squat",
                ["Quads", "Glutes", "Core"],
                "Hold one DB at chest; squat deep with upright torso.",
            ),
            _exercise(
                "DB bench press",
                ["Chest", "Triceps"],
                "Greater range than barbell; elbows ~45° from ribs.",
            ),
            _exercise(
                "Single-arm row",
                ["Lats", "Rhomboids"],
                "Support on bench; pull elbow to hip.",
            ),
            _exercise(
                "Lateral raise",
                ["Lateral deltoids"],
                "Slight bend in elbows; stop at shoulder height if impingement-prone.",
            ),
        ],
        "tips": "Rubber-hex DBs for home; avoid dropping on hard floors.",
    },
    "barbell": {
        "muscles": ["Compound chains", "Legs", "Back", "Pressing muscles"],
        "muscle_variants": "Squat, hinge, and press patterns load the bar differently—same bar, totally different muscle emphasis.",
        "instructions": "Use collars; walk out with control; keep bar path vertical over mid-foot for squats.",
        "exercises": [
            _exercise(
                "Back squat",
                ["Quads", "Glutes", "Erectors"],
                "Brace; break at hips and knees together.",
            ),
            _exercise(
                "Romanian deadlift",
                ["Hamstrings", "Glutes", "Back"],
                "Soft knee; push hips back; bar close to legs.",
            ),
            _exercise(
                "Overhead press",
                ["Shoulders", "Triceps", "Core"],
                "Stack joints; clear head with bar path.",
            ),
            _exercise(
                "Barbell row",
                ["Lats", "Rhomboids", "Biceps"],
                "Hinge; pull to lower ribs.",
            ),
        ],
        "tips": "Progress load gradually; use safety pins or a power rack for heavy squats.",
    },
    "squat rack": {
        "muscles": ["Quads", "Glutes", "Core", "Back (isometric)"],
        "muscle_variants": "High-bar vs low-bar squat; front rack for quads/core; pin squats for weak ranges.",
        "instructions": "Set J-hooks at mid-chest for unracking; walk back with minimal steps.",
        "exercises": [
            _exercise(
                "Back squat",
                ["Quads", "Glutes"],
                "Depth you own; knees track toes.",
            ),
            _exercise(
                "Overhead squat (advanced)",
                ["Shoulders", "Core", "Quads"],
                "Wide grip; mobility demanding.",
            ),
            _exercise(
                "Pin squat",
                ["Quads", "Concentric strength"],
                "Start from pins at sticking point.",
            ),
            _exercise(
                "Rack pull / partial deadlift",
                ["Posterior chain", "Grip"],
                "Set pins at knee or mid-shin.",
            ),
        ],
        "tips": "Always use safeties; bail technique: dump bar backward on pins in a controlled miss.",
    },
    "smith machine": {
        "muscles": ["Exercise-dependent", "Often quads or chest"],
        "muscle_variants": "Fixed bar path helps beginners; feet-forward split squat biases quads on Smith.",
        "instructions": "Twist to lock/unlock; keep wrists aligned; do not rely on machine for balance on risky moves.",
        "exercises": [
            _exercise(
                "Smith squat",
                ["Quads", "Glutes"],
                "Feet slightly forward if needed for upright torso.",
            ),
            _exercise(
                "Smith incline press",
                ["Upper chest", "Triceps"],
                "Bench angle 30–45°.",
            ),
            _exercise(
                "Smith hip thrust setup",
                ["Glutes", "Hamstrings"],
                "Pad the bar; drive through heels.",
            ),
            _exercise(
                "Inverted row (bar low)",
                ["Upper back", "Biceps"],
                "Body straight; pull chest to bar.",
            ),
        ],
        "tips": "Not identical to free-weight bar path—progress skill on free weights too.",
    },
    "treadmill": {
        "muscles": ["Calves", "Quads", "Hamstrings", "Cardiovascular system"],
        "muscle_variants": "Incline shifts load to calves and glutes; intervals spike heart rate without long duration.",
        "instructions": "Clip safety key; start slow; use rails only for balance, not to support body weight.",
        "exercises": [
            _exercise("Steady-state jog", ["Aerobic capacity"], "Conversational pace 20–45 min."),
            _exercise("Incline walk", ["Glutes", "Calves"], "10–15% incline, brisk walk."),
            _exercise("Interval sprints", ["Power", "Heart rate"], "Work/rest ratios e.g. 30s/60s."),
            _exercise("Walking cooldown", ["Recovery"], "Flush legs post leg day."),
        ],
        "tips": "Wear proper shoes; avoid holding the front bar while leaning back.",
    },
    "kettlebell": {
        "muscles": ["Hips", "Glutes", "Core", "Shoulders (ballistic)"],
        "muscle_variants": "Ballistics (swing, clean, snatch) are hip-driven; grinds (press, squat) are strength-focused.",
        "instructions": "Grip handle firmly; keep wrist straight; power from hip hinge on swings.",
        "exercises": [
            _exercise(
                "Kettlebell swing",
                ["Glutes", "Hamstrings", "Core"],
                "Hike pass between legs; float to chest height.",
            ),
            _exercise(
                "Goblet squat",
                ["Quads", "Core"],
                "Bell at chest; elbows inside knees at bottom.",
            ),
            _exercise(
                "Turkish get-up (learn coached)",
                ["Full body", "Stability"],
                "Slow, segmented movement under load.",
            ),
            _exercise(
                "KB row",
                ["Lats", "Biceps"],
                "Tripod stance; pack shoulder.",
            ),
        ],
        "tips": "Start with hinge pattern mastery before high reps of swings.",
    },
    "pull up bar": {
        "muscles": ["Lats", "Biceps", "Rear delts", "Core"],
        "muscle_variants": "Wide pronated for lats; supinated chin-up for biceps; archer type for single-arm bias.",
        "instructions": "Full hang to start; pull chest toward bar; control descent.",
        "exercises": [
            _exercise(
                "Pull-up (pronated)",
                ["Lats", "Brachialis"],
                "Chest to bar or chin over depending on goal.",
            ),
            _exercise(
                "Chin-up (supinated)",
                ["Biceps", "Lats"],
                "Closer grip; elbows forward.",
            ),
            _exercise(
                "Scap pull-ups",
                ["Lower traps", "Serratus"],
                "Only depression/retraction—no elbow bend.",
            ),
            _exercise(
                "Leg raises hanging",
                ["Hip flexors", "Core"],
                "Posterior pelvic tilt to bias abs.",
            ),
        ],
        "tips": "Use bands or assisted machine to build volume if needed.",
    },
    "rowing machine": {
        "muscles": ["Legs", "Back", "Arms", "Cardio"],
        "muscle_variants": "Drive is legs → hip swing → arms; higher damper is not always “harder”—focus on stroke rate and split.",
        "instructions": "Heel strap snug; handle moves straight, not arcing up early.",
        "exercises": [
            _exercise("Steady row 5k", ["Aerobic", "Leg endurance"], "Consistent split."),
            _exercise("500m repeats", ["Power", "Lactate"], "Rest 1:1 or 1:2."),
            _exercise("Technique drills", ["Coordination"], "Legs-only strokes then add body/arm."),
            _exercise("Recovery row", ["Blood flow"], "Very easy pace post workout."),
        ],
        "tips": "Maintain posture—do not overreach with rounded back at the catch.",
    },
}


def _default_entry(key: str) -> dict[str, Any]:
    k = key.lower()
    display = _title(key)

    if any(
        w in k
        for w in (
            "treadmill",
            "bike",
            "elliptical",
            "rower",
            "ergometer",
            "climber",
            "arc trainer",
            "versaclimber",
            "assault bike",
            "fan bike",
            "ski erg",
            "stair climber",
            "cross trainer",
            "jacob",
        )
    ):
        muscles = ["Legs", "Glutes", "Calves", "Cardiovascular system"]
        mv = "Long steady sessions build aerobic base; intervals improve power and VO2; adjust resistance/incline to bias quads vs glutes."
        exercises = [
            _exercise(f"{display} — steady cardio", muscles[:3], "Moderate effort 20–40 min; nasal breathing if possible."),
            _exercise(f"{display} — intervals", ["Heart rate", "Leg power"], "30–60s hard / easy recovery; build week to week."),
            _exercise(f"{display} — low-intensity recovery", ["Blood flow"], "Easy pace after heavy lifting."),
            _exercise("Cool-down", ["Recovery"], "Gradually drop intensity 3–5 minutes."),
        ]
    elif any(
        w in k
        for w in (
            "bench",
            "preacher",
            "decline",
            "incline",
            "press machine",
            "chest",
            "shoulder press",
            "dip",
        )
    ):
        muscles = ["Pushing muscles (chest/shoulders/triceps)", "Core stability"]
        mv = "Seat/back pad angles change shoulder flexion emphasis; neutral vs pronated grips alter delts and elbows."
        exercises = [
            _exercise("Primary pressing sets", ["Chest or shoulders", "Triceps"], "Full ROM; 2–4 sec lowering phase."),
            _exercise("Pause reps", ["Strength off chest or bottom"], "Kill stretch reflex; harder but safer tempo."),
            _exercise("Drop set (when safe)", ["Metabolic"], "Reduce pin weight and continue."),
            _exercise("Single-arm / alternating", ["Anti-rotation core"], "If equipment allows unilateral loading."),
        ]
    elif any(w in k for w in ("curl", "tricep", "pushdown", "preacher")):
        muscles = ["Biceps or triceps", "Forearms"]
        mv = "Elbow position relative to torso shifts long-head vs short-head bias (biceps) or long triceps head (overhead)."
        exercises = [
            _exercise("Strict curl / pushdown", muscles, "No torso swing; elbows fixed."),
            _exercise("21s or partial ROM burnouts", ["Metabolic"], "Use only when joints feel good."),
            _exercise("Slow eccentrics", ["Tendon tolerance"], "3–5 sec lowering."),
            _exercise("Superset opposite muscle", ["Arms"], "Biceps then triceps to save time."),
        ]
    elif any(
        w in k
        for w in (
            "leg curl",
            "leg extension",
            "leg press",
            "hack squat",
            "calf raise",
            "hip abduction",
            "hip adduction",
            "ab crunch",
            "back extension",
            "roman chair",
        )
    ):
        muscles = ["Lower body or trunk extensors/flexors"]
        mv = "Seat and ankle pad settings change lever arms; single-leg work fixes asymmetry."
        exercises = [
            _exercise("Standard machine sets", muscles, "2–4 sets of 8–15 with control."),
            _exercise("Single-limb variation", ["Unilateral strength"], "Match reps L/R."),
            _exercise("Rest-pause (advanced)", ["Density"], "Short rest, same weight."),
            _exercise("Isometric hold at peak contraction", ["Mind-muscle"], "1–2s squeeze each rep."),
        ]
    elif any(w in k for w in ("rope", "bag", "boxing", "battle", "slam", "sandbag")):
        muscles = ["Full body", "Core", "Shoulders", "Conditioning"]
        mv = "Power and conditioning emphasis; technique first to protect wrists and shoulders."
        exercises = [
            _exercise("Timed rounds", ["Work capacity"], "3min on / 1min off style."),
            _exercise("Power intervals", ["Hips", "Core"], "Explosive reps with full reset."),
            _exercise("Footwork + strikes", ["Coordination"], "Light speed, crisp form."),
            _exercise("Finisher circuit", ["Metabolic"], "Low skill moves only when fatigued."),
        ]
    elif any(
        w in k
        for w in (
            "yoga mat",
            "foam roller",
            "stretch",
            "cool down",
            "massage",
            "sauna",
            "steam",
            "shower",
            "locker",
            "towel",
            "water bottle",
            "gym bag",
            "hot tub",
        )
    ):
        muscles = ["Recovery / mobility (not strength primary)"]
        mv = "Use for warm-up, cooldown, hydration, and tissue care—not a replacement for progressive strength work."
        exercises = [
            _exercise("Dynamic warm-up", ["Mobility"], "5–10 min before lifting."),
            _exercise("Static stretch post-session", ["Flexibility"], "30–60s per muscle group."),
            _exercise("Foam roll major groups", ["Tissue comfort"], "Quads, lats, thoracic—slow passes."),
            _exercise("Hydration & electrolytes", ["Performance"], "Sip through workout; more in heat."),
        ]
    elif any(w in k for w in ("jump rope", "ladder", "cone", "hurdle", "agility")):
        muscles = ["Calves", "Coordination", "Ankles", "Conditioning"]
        mv = "Low-amplitude plyometrics and foot contacts—progress volume slowly."
        exercises = [
            _exercise("Basic bounce", ["Calves", "Rhythm"], "Wrist spin, small jumps."),
            _exercise("High knees / doubles (advanced)", ["Power"], "Build singles first."),
            _exercise("Agility patterns", ["Change of direction"], "Ladders and cones."),
            _exercise("Active recovery", ["Blood flow"], "1–2 min easy rope between sets."),
        ]
    elif any(
        w in k
        for w in (
            "band",
            "ankle weight",
            "wrist weight",
            "vest",
            "belt",
            "strap",
            "wrap",
            "sleeve",
            "shoes",
            "chalk",
        )
    ):
        muscles = ["Accessory to main lifts"]
        mv = "These tools modify load, joint feel, or grip—pair with compound patterns."
        exercises = [
            _exercise("Band-assisted pull-up", ["Back"], "Loop band on bar; reduce assistance over time."),
            _exercise("Band-resisted push-up", ["Chest", "Triceps"], "Band across upper back."),
            _exercise("Weighted vest walk / push-up", ["Core", "Load"], "Keep posture tall."),
            _exercise("Straps for rows", ["Grip endurance"], "Dead-stop rows if grip limits you."),
        ]
    else:
        muscles = ["Multiple groups (depends on exercise selection)"]
        mv = "Pick 2–4 movement patterns (push, pull, legs, core) across the week using this equipment."
        exercises = [
            _exercise(f"{display} — skill practice", muscles, "Light sets; perfect setup and ROM."),
            _exercise(f"{display} — strength sets", muscles, "Heavier, lower reps with full rest."),
            _exercise(f"{display} — muscular endurance", muscles, "Moderate weight, higher reps."),
            _exercise(f"{display} — superset", muscles, "Pair with opposing pattern if space allows."),
        ]

    return {
        "id": _slug(key),
        "display_name": display,
        "muscles": muscles,
        "muscle_variants": mv,
        "instructions": f"Set up the {display.lower()} for your body size. Start with light resistance and add load only when form stays crisp.",
        "exercises": exercises,
        "tips": "Warm up specific joints first; stop if you feel sharp pain; re-rack weights and wipe down when done.",
    }


def _build_db() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for key in sorted(ALL_EQUIPMENT_KEYS):
        if key in RICH_OVERRIDES:
            rich = RICH_OVERRIDES[key].copy()
            rich["id"] = _slug(key)
            rich["display_name"] = _title(key)
            out[key] = rich
        else:
            out[key] = _default_entry(key)
    return out


EQUIPMENT_DB: dict[str, dict[str, Any]] = _build_db()


def match_equipment_key(raw: str | None) -> str | None:
    if not raw:
        return None
    s = str(raw).lower().strip()
    s = s.replace("’", "'")
    if s in ALL_EQUIPMENT_KEYS:
        return s
    s2 = s.replace("-", " ")
    if s2 in ALL_EQUIPMENT_KEYS:
        return s2
    for key in sorted(ALL_EQUIPMENT_KEYS, key=len, reverse=True):
        if key in s or s in key:
            return key
    return None

