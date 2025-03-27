import requests
import json
import logging
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode
from datetime import datetime
from time import sleep
from pathlib import Path
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeamcraftAPI:
    BASE_URL = "https://api.ffxivteamcraft.com/"
    SEARCH_ENDPOINT = "search"
    TIMEOUT = 10
    BASE_DIR = Path("api_responses")
    RAW_DIR = BASE_DIR / "raw"
    PROCESSED_DIR = BASE_DIR / "processed"
    ERROR_DIR = BASE_DIR / "errors"
    BATCH_DIR = BASE_DIR / "batch"
    RATE_LIMIT_DELAY = 0

    def __init__(self, quiet: bool = False):
        self.base_url = self.BASE_URL
        self.quiet = quiet
        self._create_directories()

    def _create_directories(self):
        for directory in [self.RAW_DIR, self.PROCESSED_DIR, self.ERROR_DIR, self.BATCH_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
            if not self.quiet:
                logger.info(f"Ensured directory exists: {directory}")

    def _extract_icon_number(self, icon_path: str) -> str:
        return icon_path.split('/')[-1].replace('.png', '')

    def _format_icon_path(self, icon_path: str) -> str:
        clean_path = icon_path.replace('/i/', '').replace('.png', '')
        return f"https://xivapi.com/i/{clean_path}.png"

    def save_to_json(self, data: Dict[str, Any], status_name: str, data_type: str) -> None:
        def sanitize_filename(name: str) -> str:
            name = ' '.join(name.split())
            invalid_chars = '<>:"/\\|?*\t'
            for char in invalid_chars:
                name = name.replace(char, '_')
            return name

        directory = {
            'raw': self.RAW_DIR,
            'processed': self.PROCESSED_DIR,
            'error': self.ERROR_DIR
        }.get(data_type, self.ERROR_DIR)

        if data_type == 'processed':
            icon = data['processed_data']['icon']
            name = sanitize_filename(data['processed_data']['name'])
            status_id = data['processed_data']['id']
            filename = directory / f"{icon}_{name}_{status_id}.json"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_status_name = sanitize_filename(status_name)
            filename = directory / f"{safe_status_name}_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            if not self.quiet:
                logger.info(f"Saved {data_type} response to: {filename}")
        except Exception as e:
            logger.error(f"Error saving JSON to {filename}: {e}", exc_info=True)

    def _fetch_api_data(self, query: str, search_type: str) -> Optional[Dict[str, Any]]:
        sleep(self.RATE_LIMIT_DELAY)
        try:
            search_url = f"{self.base_url}{self.SEARCH_ENDPOINT}"
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
            self.save_to_json({"error": "No response from API", "query": status_name}, status_name, 'error')
            return None

        self.save_to_json({
            "user_input": status_name,
            "timestamp": datetime.now().isoformat(),
            "raw_response": data
        }, status_name, 'raw')

        status_data = self._handle_response(data)
        if status_data:
            processed_data = {
                "processed_data": {
                    "name": status_data.get("en", status_name),
                    "icon": self._extract_icon_number(status_data.get("icon", "")),
                    "type": status_data.get("type", ""),
                    "id": status_data.get("id", 0),
                    "api_path": self._format_icon_path(status_data.get("icon", "")),
                    "description": status_data.get("description", {}).get("en", "")
                }
            }
            self.save_to_json(processed_data, status_name, 'processed')
            return processed_data["processed_data"]

        self.save_to_json({"error": "No data found", "query": status_name}, status_name, 'error')
        return None

    def get_action_info(self, name: str) -> Optional[Dict[str, Any]]:
        data = self._fetch_api_data(name, "Action")
        if not data:
            self.save_to_json({"error": "No response from API", "query": name}, name, 'error')
            return None

        self.save_to_json({
            "user_input": name,
            "timestamp": datetime.now().isoformat(),
            "raw_response": data
        }, name, 'raw')

        action_data = self._handle_response(data)
        if action_data:
            processed_data = {
                "processed_data": {
                    "name": action_data.get("en", name),
                    "icon": self._extract_icon_number(action_data.get("icon", "")),
                    "type": "Action",
                    "id": action_data.get("id", 0),
                    "api_path": self._format_icon_path(action_data.get("icon", "")),
                    "description": action_data.get("description", {}).get("en", "No description available")
                }
            }
            self.save_to_json(processed_data, name, 'processed')
            return processed_data["processed_data"]

        self.save_to_json({"error": "No action data found", "query": name}, name, 'error')
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

def main():
    choice = input("Enter '1' for single status search or '2' for batch processing: ")

    try:
        if choice == '1':
            api = TeamcraftAPI()
            status_name = input("Enter the status name to search: ")
            status_info = api.get_status_info(status_name)
            if status_info:
                logger.info(json.dumps(status_info, indent=4, ensure_ascii=False))
            else:
                logger.warning(f"No status data found for: {status_name}. Trying as action...")
                action_info = api.get_action_info(status_name)
                if action_info:
                    logger.info(f"Found as action: {status_name}")
                    logger.info(json.dumps(action_info, indent=4, ensure_ascii=False))
                else:
                    logger.error(f"No data found for status or action: {status_name}")

        elif choice == '2':
            filename = input("Enter the path to your status list file: ")
            if not Path(filename).exists():
                logger.error(f"File not found: {filename}")
                return
            api = TeamcraftAPI(quiet=True)
            api.batch_process_status(filename)

        else:
            logger.error("Invalid choice. Please enter '1' or '2'.")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
