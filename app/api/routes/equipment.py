import base64

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.ai.vision_service import analyze_image_safe
from app.services.ai.normalizer import normalize_equipment
from app.models.equipment_scan import EquipmentScan
from app.utils.parser import safe_parse_json
from app.services.ai.validators import validate_equipment
from app.api.deps import get_current_user
from app.models.user import User
from app.utils.response import success_response, error_response
from app.core.logger import logger

router = APIRouter()

EQUIPMENT_PROMPT = """
You are a gym equipment recognition system.

Return ONLY valid JSON:
{
  "equipment": "<one item from allowed list>",
  "confidence": number
}

Allowed equipment:
- lat pulldown
- treadmill
- bench press
- leg press
- dumbbells
- barbell
- squat rack
- leg curl machine
- leg extension machine
- chest press machine
- shoulder press machine
- bicep curl machine
- tricep pushdown machine
- rowing machine
- elliptical trainer
- stationary bike
- stair climber
- cable machine
- pull up bar
- dip station
- kettlebell
- medicine ball
- resistance bands
- smith machine
- hack squat machine
- calf raise machine
- ab crunch machine
- back extension machine
- hip abduction machine
- hip adduction machine
- preacher curl bench
- incline bench
- decline bench
- roman chair
- battle ropes
- punching bag
- speed bag
- boxing ring
- yoga mat
- foam roller
- exercise ball
- step platform
- rower
- assault bike
- fan bike
- recumbent bike
- upright bike
- spin bike
- cross trainer
- arc trainer
- versaclimber
- Jacob's ladder
- ski ergometer
- rowing ergometer
- boxing dummy
- heavy bag
- double end bag
- speed bag platform
- jump rope
- agility ladder
- cone markers
- hurdle
- medicine ball rebounder
- slam ball
- sandbag
- weight vest
- ankle weights
- wrist weights
- lifting belt
- lifting straps
- wrist wraps
- knee sleeves
- elbow sleeves
- compression shorts
- lifting shoes
- chalk bag
- water bottle
- towel
- gym bag
- locker
- shower
- sauna
- steam room
- hot tub
- massage table
- stretching area
- cool down area

Rules:
- If image is NOT gym equipment → return:
{
  "equipment": "unknown",
  "confidence": 0
}
- No explanations
- No extra text
"""

@router.post("/scan")
async def scan_equipment(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        return error_response("INVALID_FILE", "File must be an image")

    max_size = 10 * 1024 * 1024
    file_content = await file.read()

    if len(file_content) > max_size:
        return error_response("FILE_TOO_LARGE", "Image file must be less than 10MB")

    try:
        image_base64 = base64.b64encode(file_content).decode("utf-8")
        mime_type = file.content_type or "image/jpeg"
        data_url = f"data:{mime_type};base64,{image_base64}"
        logger.info(
            "Equipment scan upload: %s, %s bytes",
            file.filename,
            len(file_content),
        )
        raw = await analyze_image_safe(EQUIPMENT_PROMPT, data_url)
    except Exception as e:
        logger.error("Equipment scan read failed: %s", e)
        return error_response("INVALID_FILE", "Could not read image upload")

    if not raw:
        return error_response("AI_TIMEOUT", "AI service unavailable")

    parsed = safe_parse_json(raw)

    if not parsed:
        return error_response("AI_PARSE_ERROR", "Invalid AI response")

    validated = validate_equipment(parsed)

    if not validated:
        return error_response("NOT_EQUIPMENT", "Image does not contain valid gym equipment")

    if validated["confidence"] < 0.6:
        return error_response("LOW_CONFIDENCE", "AI confidence too low")

    normalized = normalize_equipment(validated["equipment"])

    if not normalized:
        return error_response("UNKNOWN_EQUIPMENT", "Equipment not recognized")

    confidence = float(validated.get("confidence") or 0.8)

    try:
        scan = EquipmentScan(
            user_id=current_user.id,
            equipment_id=normalized["id"],
            confidence=confidence,
            muscles=normalized["muscles"],
            instructions=normalized["instructions"],
        )

        db.add(scan)
        await db.commit()
    except Exception:
        await db.rollback()
        return error_response("DB_ERROR", "Failed to save data")

    payload = {
        **normalized,
        "confidence": confidence,
    }
    return success_response(payload)