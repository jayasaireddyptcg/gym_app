from fastapi import APIRouter, Depends
from typing import List, Optional
import logging

from app.models.user import User
from app.api.deps import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

EXERCISES = [
    {
        "id": "1",
        "name": "Bench Press",
        "category": "Chest",
        "difficulty": "Intermediate",
        "icon": "🏋️",
        "description": "The bench press is a compound exercise that targets the chest, shoulders, and triceps. It is one of the most popular exercises for building upper body strength.",
        "muscles": ["Chest", "Shoulders", "Triceps"],
        "equipment": ["Barbell", "Bench"],
        "steps": [
            "Lie flat on a bench with your feet on the floor",
            "Grip the barbell slightly wider than shoulder-width",
            "Unrack the bar and lower it to your chest",
            "Press the bar back up to the starting position",
            "Repeat for desired number of repetitions"
        ],
        "tips": [
            "Keep your feet flat on the floor for stability",
            "Maintain a slight arch in your lower back",
            "Do not bounce the bar off your chest",
            "Use a spotter for heavy lifts"
        ]
    },
    {
        "id": "2",
        "name": "Squat",
        "category": "Legs",
        "difficulty": "Intermediate",
        "icon": "🦵",
        "description": "The squat is a fundamental compound exercise that targets the quadriceps, hamstrings, and glutes. It is essential for building lower body strength.",
        "muscles": ["Quadriceps", "Hamstrings", "Glutes", "Core"],
        "equipment": ["Barbell", "Squat Rack"],
        "steps": [
            "Position the bar on your upper back",
            "Stand with feet shoulder-width apart",
            "Bend your knees and hips to lower your body",
            "Keep your chest up and back straight",
            "Return to standing position"
        ],
        "tips": [
            "Keep your knees in line with your toes",
            "Do not let your knees cave inward",
            "Maintain a neutral spine throughout",
            "Go as low as flexibility allows"
        ]
    },
    {
        "id": "3",
        "name": "Deadlift",
        "category": "Back",
        "difficulty": "Advanced",
        "icon": "💪",
        "description": "The deadlift is a powerful compound exercise that works multiple muscle groups including the back, legs, and core.",
        "muscles": ["Back", "Hamstrings", "Glutes", "Core"],
        "equipment": ["Barbell"],
        "steps": [
            "Stand with feet hip-width apart, bar over mid-foot",
            "Bend at hips and knees to grip the bar",
            "Keep your back straight and chest up",
            "Drive through your heels to stand",
            "Lower the bar back down with control"
        ],
        "tips": [
            "Keep the bar close to your body",
            "Do not round your lower back",
            "Engage your core throughout the movement",
            "Start with lighter weights to master form"
        ]
    },
    {
        "id": "4",
        "name": "Pull Up",
        "category": "Back",
        "difficulty": "Intermediate",
        "icon": "🏋️",
        "description": "The pull-up is an excellent exercise for building back and bicep strength using body weight.",
        "muscles": ["Latissimus Dorsi", "Biceps", "Rhomboids"],
        "equipment": ["Pull-up Bar"],
        "steps": [
            "Hang from the bar with palms facing away",
            "Pull yourself up until chin is over the bar",
            "Lower yourself back down with control",
            "Repeat for desired repetitions"
        ],
        "tips": [
            "Engage your core to prevent swinging",
            "Focus on pulling your elbows down",
            "Use a assisted variation if needed",
            "Control the descent for better results"
        ]
    },
    {
        "id": "5",
        "name": "Push Up",
        "category": "Chest",
        "difficulty": "Beginner",
        "icon": "💪",
        "description": "The push-up is a classic bodyweight exercise that builds chest, shoulder, and tricep strength.",
        "muscles": ["Chest", "Shoulders", "Triceps", "Core"],
        "equipment": ["None"],
        "steps": [
            "Start in a plank position",
            "Lower your body until chest nearly touches floor",
            "Push back up to starting position",
            "Keep your body in a straight line throughout"
        ],
        "tips": [
            "Keep your core engaged",
            "Do not let your hips sag or pike up",
            "Modify on knees if needed",
            "Keep elbows at 45-degree angle"
        ]
    },
    {
        "id": "6",
        "name": "Lunges",
        "category": "Legs",
        "difficulty": "Beginner",
        "icon": "🦵",
        "description": "Lunges are a unilateral leg exercise that improves balance and strengthens the legs.",
        "muscles": ["Quadriceps", "Hamstrings", "Glutes"],
        "equipment": ["None"],
        "steps": [
            "Stand with feet hip-width apart",
            "Step forward with one leg",
            "Lower your body until both knees are at 90 degrees",
            "Push back to starting position",
            "Alternate legs"
        ],
        "tips": [
            "Keep your front knee over your ankle",
            "Maintain an upright torso",
            "Start without weights to master form",
            "Step far enough to avoid leaning forward"
        ]
    },
    {
        "id": "7",
        "name": "Plank",
        "category": "Core",
        "difficulty": "Beginner",
        "icon": "🧘",
        "description": "The plank is an isometric core exercise that strengthens the entire midsection.",
        "muscles": ["Core", "Shoulders", "Back"],
        "equipment": ["None"],
        "steps": [
            "Start in a push-up position on forearms",
            "Keep your body in a straight line",
            "Engage your core and hold",
            "Breathe steadily throughout"
        ],
        "tips": [
            "Do not let hips sag or rise",
            "Squeeze your glutes for stability",
            "Start with shorter holds and build up",
            "Keep neck neutral"
        ]
    },
    {
        "id": "8",
        "name": "Bicep Curl",
        "category": "Arms",
        "difficulty": "Beginner",
        "icon": "💪",
        "description": "The bicep curl is an isolation exercise that targets the biceps.",
        "muscles": ["Biceps"],
        "equipment": ["Dumbbells"],
        "steps": [
            "Stand with dumbbells at your sides",
            "Curl the weights toward your shoulders",
            "Squeeze at the top",
            "Lower back down with control"
        ],
        "tips": [
            "Keep elbows stationary at your sides",
            "Avoid swinging the weights",
            "Use a controlled motion",
            "Work both arms equally"
        ]
    },
    {
        "id": "9",
        "name": "Shoulder Press",
        "category": "Shoulders",
        "difficulty": "Intermediate",
        "icon": "🏋️",
        "description": "The shoulder press builds overhead strength and muscle in the deltoids.",
        "muscles": ["Deltoids", "Triceps", "Upper Chest"],
        "equipment": ["Dumbbells", "Barbell"],
        "steps": [
            "Hold weights at shoulder height",
            "Press weights overhead",
            "Extend arms fully at the top",
            "Lower back down with control"
        ],
        "tips": [
            "Keep core tight throughout",
            "Do not arch your lower back",
            "Bring weights down to shoulder level",
            "Avoid locking elbows at the top"
        ]
    },
    {
        "id": "10",
        "name": "Leg Press",
        "category": "Legs",
        "difficulty": "Intermediate",
        "icon": "🦵",
        "description": "The leg press is a machine exercise that targets the legs with less spinal load than squats.",
        "muscles": ["Quadriceps", "Hamstrings", "Glutes"],
        "equipment": ["Leg Press Machine"],
        "steps": [
            "Sit in the leg press machine",
            "Place feet shoulder-width on the platform",
            "Lower the weight by bending knees",
            "Push back up without locking knees"
        ],
        "tips": [
            "Do not let knees cave inward",
            "Keep lower back pressed against seat",
            "Use a controlled tempo",
            "Start with lighter weight to learn movement"
        ]
    }
]

CATEGORIES = ["All", "Chest", "Back", "Legs", "Arms", "Shoulders", "Core"]


@router.get("/exercises")
async def get_exercises(
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Get exercises request - category: {category}, search: {search}")
    
    filtered = EXERCISES
    
    if category and category != "All":
        filtered = [e for e in filtered if e["category"] == category]
    
    if search:
        search_lower = search.lower()
        filtered = [e for e in filtered if search_lower in e["name"].lower()]
    
    return {
        "success": True,
        "data": {
            "exercises": filtered,
            "categories": CATEGORIES
        }
    }


@router.get("/exercises/{exercise_id}")
async def get_exercise(
    exercise_id: str,
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Get exercise request - id: {exercise_id}")
    
    exercise = next((e for e in EXERCISES if e["id"] == exercise_id), None)
    
    if not exercise:
        return {"success": False, "error": {"message": "Exercise not found"}}
    
    return {
        "success": True,
        "data": exercise
    }
