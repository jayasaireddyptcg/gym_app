import json
import re
from app.core.logger import logger

def safe_parse_json(raw: str):
    if not raw:
        logger.warning("Empty or None response received")
        return None
    
    # Log the raw response for debugging
    logger.info(f"Raw AI response: {raw[:500]}...")
    
    # Try direct JSON parsing first
    try:
        parsed = json.loads(raw.strip())
        logger.info("Successfully parsed direct JSON")
        return parsed
    except json.JSONDecodeError as e:
        logger.info(f"Direct JSON parsing failed: {e}")
    
    # Try to extract JSON from markdown code blocks
    json_patterns = [
        r'```json\s*(.*?)\s*```',
        r'```\s*(.*?)\s*```',
        r'```JSON\s*(.*?)\s*```'
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, raw, re.DOTALL | re.IGNORECASE)
        for match in matches:
            try:
                parsed = json.loads(match.strip())
                logger.info(f"Successfully parsed JSON from markdown pattern: {pattern}")
                return parsed
            except json.JSONDecodeError:
                logger.debug(f"Failed to parse match from pattern {pattern}: {match[:100]}")
                continue
    
    # Try to find JSON object(s) in the text - more robust pattern
    json_object_patterns = [
        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Nested objects
        r'\{.*\}'  # Simple objects
    ]
    
    for pattern in json_object_patterns:
        matches = re.findall(pattern, raw, re.DOTALL)
        for match in matches:
            try:
                parsed = json.loads(match)
                logger.info(f"Successfully parsed JSON from text pattern: {pattern}")
                return parsed
            except json.JSONDecodeError:
                logger.debug(f"Failed to parse match from pattern {pattern}: {match[:100]}")
                continue
    
    # Try to extract JSON by finding the first { and last }
    first_brace = raw.find('{')
    last_brace = raw.rfind('}')
    
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        json_candidate = raw[first_brace:last_brace + 1]
        try:
            parsed = json.loads(json_candidate)
            logger.info("Successfully parsed JSON using brace extraction")
            return parsed
        except json.JSONDecodeError:
            logger.debug(f"Failed to parse brace-extracted JSON: {json_candidate[:100]}")
    
    logger.error(f"Failed to parse JSON from AI response after all attempts")
    return None
