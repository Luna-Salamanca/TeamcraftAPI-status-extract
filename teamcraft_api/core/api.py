# teamcraft_api/core/api.py
import requests
import json
import logging
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode
from datetime import datetime
from time import sleep
from pathlib import Path
from teamcraft_api.core.utils import extract_icon_number, format_icon_path
from teamcraft_api.core.data_saver import save_to_json

logger = logging.getLogger(__name__)

class TeamcraftAPI:
    BASE_URL = "https://api.ffxivteamcraft.com/"
    SEARCH_ENDPOINT = "search"
    TIMEOUT = 10
    RATE_LIMIT_DELAY = 0

    def __init__(self, quiet: bool = False, base_dir: Optional[str] = None):
        self.quiet = quiet
        self.BASE_DIR = Path(base_dir or "api_responses")
        self.RAW_DIR = self.BASE_DIR / "raw"
        self.PROCESSED_DIR = self.BASE_DIR / "processed"
        self.ERROR_DIR = self.BASE_DIR / "errors"
        self.BATCH_DIR = self.BASE_DIR / "batch"
        self._create_directories()

    def _create_directories(self):
        for directory in [self.RAW_DIR, self.PROCESSED_DIR, self.ERROR_DIR, self.BATCH_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
            if not self.quiet:
                logger.info(f"Ensured directory exists: {directory}")

    def _fetch_api_data(self, query: str, search_type: str) -> Optional[Dict[str, Any]]:
        sleep(self.RATE_LIMIT_DELAY)
        try:
            search_url = f"{self.BASE_URL}{self.SEARCH_ENDPOINT}"
            params = {"query": query, "type": search_type}
            full_url = f"{search_url}?{urlencode(params)}"

            if not self.quiet:
                logger.info(f"Fetching data from: {full_url}")
            response = requests.get(full_url, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Network error: {str(e)}", exc_info=True)
            return None

    def _handle_response(self, data: Any) -> Optional[Dict[str, Any]]:
        try:
            if isinstance(data, list) and data:
                return data[0]
            logger.warning("Empty or unexpected response format.")
            return None
        except Exception as e:
            logger.error(f"Error processing response: {str(e)}", exc_info=True)
            return None

    def get_status_info(self, status_name: str) -> Optional[Dict[str, Any]]:
        data = self._fetch_api_data(status_name, "Status")
        if not data:
            save_to_json(self.ERROR_DIR, {"error": "No response from API", "query": status_name}, status_name, 'error', self.quiet)
            return None

        save_to_json(self.RAW_DIR, {
            "user_input": status_name,
            "timestamp": datetime.now().isoformat(),
            "raw_response": data
        }, status_name, 'raw', self.quiet)

        status_data = self._handle_response(data)
        if status_data:
            processed_data = {
                "processed_data": {
                    "name": status_data.get("en", status_name),
                    "icon": extract_icon_number(status_data.get("icon", "")),
                    "type": status_data.get("type", ""),
                    "id": status_data.get("id", 0),
                    "api_path": format_icon_path(status_data.get("icon", "")),
                    "description": status_data.get("description", {}).get("en", "")
                }
            }
            save_to_json(self.PROCESSED_DIR, processed_data, status_name, 'processed', self.quiet)
            return processed_data["processed_data"]

        save_to_json(self.ERROR_DIR, {"error": "No data found", "query": status_name}, status_name, 'error', self.quiet)
        return None

    def get_action_info(self, name: str) -> Optional[Dict[str, Any]]:
        data = self._fetch_api_data(name, "Action")
        if not data:
            save_to_json(self.ERROR_DIR, {"error": "No response from API", "query": name}, name, 'error', self.quiet)
            return None

        save_to_json(self.RAW_DIR, {
            "user_input": name,
            "timestamp": datetime.now().isoformat(),
            "raw_response": data
        }, name, 'raw', self.quiet)

        action_data = self._handle_response(data)
        if action_data:
            processed_data = {
                "processed_data": {
                    "name": action_data.get("en", name),
                    "icon": extract_icon_number(action_data.get("icon", "")),
                    "type": "Action",
                    "id": action_data.get("id", 0),
                    "api_path": format_icon_path(action_data.get("icon", "")),
                    "description": action_data.get("description", {}).get("en", "No description available")
                }
            }
            save_to_json(self.PROCESSED_DIR, processed_data, name, 'processed', self.quiet)
            return processed_data["processed_data"]

        save_to_json(self.ERROR_DIR, {"error": "No action data found", "query": name}, name, 'error', self.quiet)
        return None

    @staticmethod
    def read_status_list(filename: str) -> List[str]:
        path = Path(filename)
        if not path.exists():
            logger.error(f"File not found: {filename}")
            return []

        lines = path.read_text(encoding='utf-8').splitlines()
        return list(dict.fromkeys([
            ' '.join(line.strip().split())
            for line in lines
            if line.strip() and not line.strip().startswith('//')
        ]))

    def batch_process_status(self, filename: str) -> Dict[str, Any]:
        status_list = self.read_status_list(filename)
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

            if (info := self.get_status_info(name)):
                results['status_effects'].append({'name': name, 'data': info})
            elif (info := self.get_action_info(name)):
                results['actions'].append({'name': name, 'data': info})
                if not self.quiet:
                    print(f"Found as action: {name}")
            else:
                results['failed_lookups'].append(name)
                logger.warning(f"Failed to fetch data for: {name}")

            sleep(self.RATE_LIMIT_DELAY)

        output_file = self.BATCH_DIR / f"results_{datetime.now():%Y%m%d_%H%M%S}.json"
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
