from openai import OpenAI
from app.core.config import settings
from app.utils.timeout import with_timeout
from app.utils.retry import retry
from app.core.logger import logger
import httpx
import base64

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def download_image_as_base64(image_url: str):
    """Download image and convert to base64 for OpenAI API"""
    try:
        async with httpx.AsyncClient() as client_http:
            response = await client_http.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Convert to base64
            image_data = response.content
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Determine MIME type
            content_type = response.headers.get('content-type', 'image/jpeg')
            
            return f"data:{content_type};base64,{base64_image}"
            
    except Exception as e:
        logger.error(f"Failed to download image: {e}")
        return None

async def analyze_image(prompt: str, image_url: str):
    logger.info(f"Analyzing image: {image_url}")
    
    try:
        # Try direct URL first (for images that are publicly accessible)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": prompt
                },
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text", 
                            "text": "Analyze this image for food items and nutritional information."
                        },
                        {
                            "type": "image_url", 
                            "image_url": {
                                "url": image_url,
                                "detail": "low"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        logger.info(f"AI response received (direct URL): {result[:200]}...")
        return result
        
    except Exception as e:
        logger.warning(f"Direct URL failed, trying base64 conversion: {e}")
        
        # Fallback: download and convert to base64
        base64_image = await download_image_as_base64(image_url)
        
        if not base64_image:
            raise Exception("Failed to download and convert image")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": prompt
                },
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text", 
                            "text": "Analyze this image for food items and nutritional information."
                        },
                        {
                            "type": "image_url", 
                            "image_url": {
                                "url": base64_image,
                                "detail": "low"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        logger.info(f"AI response received (base64): {result[:200]}...")
        return result

async def analyze_image_safe(prompt: str, image_url: str):
    logger.info(f"Starting safe image analysis for: {image_url}")
    
    async def call():
        return await analyze_image(prompt, image_url)

    result = await retry(lambda: with_timeout(call(), timeout=20))

    if not result:
        logger.error("AI call failed or timed out after retries")
        return None

    logger.info("AI call completed successfully")
    return result