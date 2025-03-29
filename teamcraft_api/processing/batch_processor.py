# teamcraft_api/processing/batch_processor.py
from teamcraft_api.processing.status_handler import lookup_status_or_action
from teamcraft_api.core.api import TeamcraftAPI
from teamcraft_api.constants.config import BATCH_DIR
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

def batch_process_status(api: TeamcraftAPI, filename: str) -> dict:
    status_list = api.read_status_list(filename)
    results = {
        'metadata': {
            'total_effects': len(status_list),
            'timestamp': datetime.now().isoformat(),
            'source_file': filename
        },
        'status_effects': [],
        'actions': [],
        'failed_lookups': []
    }

    for index, name in enumerate(status_list, 1):
        print(f"Processing: {name} ({index}/{len(status_list)})")
        result = lookup_status_or_action(api, name)
        if result:
            key_map = {
                "status": "status_effects",
                "action": "actions"
            }
            results[key_map[result['type']]].append({"name": name, "data": result["data"]})
        else:
            results['failed_lookups'].append(name)
            logger.warning(f"Failed to fetch data for: {name}")

    output_file = BATCH_DIR / f"results_{datetime.now():%Y%m%d_%H%M%S}.json"
    output_file.write_text(json.dumps(results, indent=4, ensure_ascii=False), encoding='utf-8')

    print(f"\nBatch processing complete. Results saved to {output_file}")
    print(f"Successfully processed status effects: {len(results['status_effects'])}")
    print(f"Successfully processed actions: {len(results['actions'])}")
    print(f"Failed lookups: {len(results['failed_lookups'])}")

    if results['failed_lookups']:
        print("\nFailed lookups:")
        for failed in results['failed_lookups']:
            print(f"  - {failed}")

    return results
