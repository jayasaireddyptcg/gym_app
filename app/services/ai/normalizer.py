import copy

from app.services.ai.equipment_catalog import EQUIPMENT_DB, match_equipment_key


def normalize_equipment(canonical_key: str):
    """
    Return a deep copy of catalog entry for a canonical equipment key
    (as produced by validate_equipment / match_equipment_key).
    """
    key = canonical_key
    if key not in EQUIPMENT_DB:
        key = match_equipment_key(canonical_key) or ""
    if not key or key not in EQUIPMENT_DB:
        return None
    return copy.deepcopy(EQUIPMENT_DB[key])
