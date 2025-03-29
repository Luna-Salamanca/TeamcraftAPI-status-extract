# teamcraft_api/processing/status_handler.py
from teamcraft_api.core.api import TeamcraftAPI
from typing import Dict, Optional
import logging
import json

logger = logging.getLogger(__name__)


def lookup_status_or_action(api: TeamcraftAPI, name: str) -> Optional[Dict]:
    status_info = api.get_status_info(name)
    if status_info:
        return {"type": "status", "data": status_info}

    logger.warning(f"No status found for: {name}. Trying as action...")
    action_info = api.get_action_info(name)
    if action_info:
        logger.info(f"Found as action: {name}")
        return {"type": "action", "data": action_info}

    logger.error(f"No data found for: {name}")
    return None
