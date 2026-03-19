from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
import base64
import io
from PIL import Image
import uuid

from app.core.database import get_db
from app.services.ai.vision_service import analyze_image_safe
from app.models.food_scan import FoodScan
from app.utils.parser import safe_parse_json
from app.api.deps import get_current_user
from app.models.user import User
from app.utils.response import success_response, error_response
from app.core.logger import logger
import httpx

router = APIRouter()

FOOD_PROMPT = """
You are a food recognition and nutrition analysis system. Identify all food items in the image and provide comprehensive nutritional information.

Return ONLY valid JSON:
{
  "items": [
    {
      "name": "apple",
      "quantity": 1,
      "macros": {
        "calories": 95,
        "protein": 0.5,
        "carbs": 25,
        "fat": 0.3,
        "fiber": 4.4,
        "sugar": 19
      },
      "micronutrients": {
        "vitamins": {
          "vitamin_c": 8.4,
          "vitamin_a": 98,
          "vitamin_k": 4,
          "vitamin_e": 0.5,
          "thiamine": 0.03,
          "riboflavin": 0.06,
          "niacin": 0.2,
          "vitamin_b6": 0.08,
          "folate": 5,
          "vitamin_b12": 0
        },
        "minerals": {
          "calcium": 11,
          "iron": 0.2,
          "magnesium": 8,
          "phosphorus": 20,
          "potassium": 195,
          "sodium": 1,
          "zinc": 0.1,
          "copper": 0.06,
          "manganese": 0.1,
          "selenium": 0
        }
      }
    }
  ],
  "total": {
    "macros": {
      "calories": 95,
      "protein": 0.5,
      "carbs": 25,
      "fat": 0.3,
      "fiber": 4.4,
      "sugar": 19
    },
    "micronutrients": {
      "vitamins": {
        "vitamin_c": 8.4,
        "vitamin_a": 98,
        "vitamin_k": 4,
        "vitamin_e": 0.5,
        "thiamine": 0.03,
        "riboflavin": 0.06,
        "niacin": 0.2,
        "vitamin_b6": 0.08,
        "folate": 5,
        "vitamin_b12": 0
      },
      "minerals": {
        "calcium": 11,
        "iron": 0.2,
        "magnesium": 8,
        "phosphorus": 20,
        "potassium": 195,
        "sodium": 1,
        "zinc": 0.1,
        "copper": 0.06,
        "manganese": 0.1,
        "selenium": 0
      }
    }
  }
}

Rules:
- Identify all visible food items
- Estimate reasonable quantities (portions)
- Provide accurate nutritional values per standard serving
- Include comprehensive vitamins and minerals
- Calculate totals for all items
- Max 5 items per image
- If image is NOT food → return: {"items": [], "total": {"macros": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "sugar": 0}, "micronutrients": {"vitamins": {"vitamin_c": 0, "vitamin_a": 0, "vitamin_k": 0, "vitamin_e": 0, "thiamine": 0, "riboflavin": 0, "niacin": 0, "vitamin_b6": 0, "folate": 0, "vitamin_b12": 0}, "minerals": {"calcium": 0, "iron": 0, "magnesium": 0, "phosphorus": 0, "potassium": 0, "sodium": 0, "zinc": 0, "copper": 0, "manganese": 0, "selenium": 0}}}
- No explanations or extra text
- Use standard nutritional values in mg for vitamins/minerals
"""

@router.post("/scan")
async def scan_food(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        return error_response("INVALID_FILE", "File must be an image")
    
    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    
    if len(file_content) > max_size:
        return error_response("FILE_TOO_LARGE", "Image file must be less than 10MB")
    
    # Reset file pointer
    await file.seek(0)
    
    try:
        # Convert image to base64 for AI analysis
        image_base64 = base64.b64encode(file_content).decode('utf-8')
        mime_type = file.content_type or 'image/jpeg'
        data_url = f"data:{mime_type};base64,{image_base64}"
        
        logger.info(f"Processing image upload: {file.filename}, size: {len(file_content)} bytes")
        
        raw = await analyze_image_safe(FOOD_PROMPT, data_url)

        if not raw:
            return error_response("AI_TIMEOUT", "AI service unavailable")

        parsed = safe_parse_json(raw)

        if not parsed:
            # Log the problematic response for debugging
            logger.error(f"Failed to parse AI response: {raw}")
            
            # Instead of failing completely, return a generic "unable to analyze" response
            # This is better than a hard error for user experience
            fallback_response = {
                "items": [],
                "total": {
                    "macros": {
                        "calories": 0, 
                        "protein": 0, 
                        "carbs": 0, 
                        "fat": 0, 
                        "fiber": 0, 
                        "sugar": 0
                    }, 
                    "micronutrients": {
                        "vitamins": {
                            "vitamin_c": 0, 
                            "vitamin_a": 0, 
                            "vitamin_k": 0, 
                            "vitamin_e": 0, 
                            "thiamine": 0, 
                            "riboflavin": 0, 
                            "niacin": 0, 
                            "vitamin_b6": 0, 
                            "folate": 0, 
                            "vitamin_b12": 0
                        }, 
                        "minerals": {
                            "calcium": 0, 
                            "iron": 0, 
                            "magnesium": 0, 
                            "phosphorus": 0, 
                            "potassium": 0, 
                            "sodium": 0, 
                            "zinc": 0, 
                            "copper": 0, 
                            "manganese": 0, 
                            "selenium": 0
                        }
                    }
                }
            }
            
            # Save the failed attempt for debugging
            try:
                scan = FoodScan(
                    user_id=current_user.id,
                    items=[],
                    total_calories=0
                )
                db.add(scan)
                await db.commit()
            except Exception as e:
                await db.rollback()
                logger.error(f"Database error saving fallback: {e}")
            
            return success_response({
                "items": fallback_response["items"],
                "total": fallback_response["total"],
                "warning": "AI response could not be parsed properly. Please try again with a clearer image."
            })

        # Validate the response structure
        if not isinstance(parsed, dict):
            return error_response("AI_PARSE_ERROR", "Invalid response format")

        items = parsed.get("items", [])
        total = parsed.get("total", {"macros": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "sugar": 0}, "micronutrients": {"vitamins": {"vitamin_c": 0, "vitamin_a": 0, "vitamin_k": 0, "vitamin_e": 0, "thiamine": 0, "riboflavin": 0, "niacin": 0, "vitamin_b6": 0, "folate": 0, "vitamin_b12": 0}, "minerals": {"calcium": 0, "iron": 0, "magnesium": 0, "phosphorus": 0, "potassium": 0, "sodium": 0, "zinc": 0, "copper": 0, "manganese": 0, "selenium": 0}}})

        if not items:
            return error_response("NOT_FOOD", "Image does not contain valid food items")

        # Validate items structure
        for item in items:
            if not isinstance(item, dict) or "name" not in item or "macros" not in item:
                return error_response("AI_PARSE_ERROR", "Invalid item structure in response")

        try:
            scan = FoodScan(
                user_id=current_user.id,
                items=items,
                total_calories=total["macros"]["calories"]
            )

            db.add(scan)
            await db.commit()
        except Exception as e:
            await db.rollback()
            logger.error(f"Database error: {e}")
            return error_response("DB_ERROR", "Failed to save data")

        return success_response({
            "items": items,
            "total": total
        })
        
    except Exception as e:
        logger.error(f"Error processing image upload: {e}")
        return error_response("PROCESSING_ERROR", f"Failed to process image: {str(e)}")

@router.post("/debug-image")
async def debug_image_url(
    image_url: str = Form(None),
    file: UploadFile = File(None),
    current_user: User = Depends(get_current_user)
):
    """Debug endpoint to check if an image is accessible"""
    
    debug_info = {
        "url": image_url,
        "accessible": False,
        "content_type": None,
        "size_bytes": None,
        "ai_test": False,
        "error": None,
        "method": "url" if image_url else "file_upload"
    }
    
    image_data_url = None
    
    # Handle file upload
    if file and file.filename:
        try:
            file_content = await file.read()
            debug_info["size_bytes"] = len(file_content)
            debug_info["content_type"] = file.content_type
            debug_info["filename"] = file.filename
            debug_info["accessible"] = True
            
            # Convert to base64 for AI test
            import base64
            image_base64 = base64.b64encode(file_content).decode('utf-8')
            mime_type = file.content_type or 'image/jpeg'
            image_data_url = f"data:{mime_type};base64,{image_base64}"
            
            logger.info(f"Debug file upload: {file.filename} ({len(file_content)} bytes)")
            
        except Exception as e:
            debug_info["error"] = str(e)
            logger.error(f"File upload debug error: {e}")
    
    # Handle URL
    elif image_url:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(image_url)
                response.raise_for_status()
                
                debug_info["accessible"] = True
                debug_info["content_type"] = response.headers.get("content-type")
                debug_info["size_bytes"] = len(response.content)
                image_data_url = image_url
                
                logger.info(f"Debug image URL accessible: {image_url} ({debug_info['size_bytes']} bytes)")
                
        except Exception as e:
            debug_info["error"] = str(e)
            logger.error(f"Image URL debug error: {image_url} - {e}")
    else:
        debug_info["error"] = "No image URL or file provided"
    
    # Test with AI service
    if image_data_url:
        try:
            ai_result = await analyze_image_safe("What do you see in this image?", image_data_url)
            debug_info["ai_test"] = ai_result is not None
            if ai_result:
                debug_info["ai_response_preview"] = ai_result[:100] + "..."
        except Exception as e:
            debug_info["ai_error"] = str(e)
    
    return success_response(debug_info)
