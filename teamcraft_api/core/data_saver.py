# teamcraft_api/core/data_saver.py
import json
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def save_to_json(directory: Path, data: dict, name: str, data_type: str, quiet: bool = False):
    def sanitize_filename(name: str) -> str:
        name = ' '.join(name.split())
        invalid_chars = '<>:"/\\|?*\t'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name

    directory.mkdir(parents=True, exist_ok=True)

    if data_type == 'processed':
        icon = data['processed_data']['icon']
        name = sanitize_filename(data['processed_data']['name'])
        status_id = data['processed_data']['id']
        filename = directory / f"{icon}_{name}_{status_id}.json"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_status_name = sanitize_filename(name)
        filename = directory / f"{safe_status_name}_{timestamp}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        if not quiet:
            logger.info(f"Saved {data_type} response to: {filename}")
    except Exception as e:
        logger.error(f"Error saving JSON to {filename}: {e}", exc_info=True)