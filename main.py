import requests
import json
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlencode
from datetime import datetime
from time import sleep
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeamcraftAPI:
    BASE_URL = "https://api.ffxivteamcraft.com/"
    SEARCH_ENDPOINT = "/search"
    TIMEOUT = 10
    BASE_DIR = "api_responses"
    RAW_DIR = os.path.join(BASE_DIR, "raw")
    PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
    ERROR_DIR = os.path.join(BASE_DIR, "errors")
    RATE_LIMIT_DELAY = 1

    def __init__(self):
        self.base_url = self.BASE_URL
        self._create_directories()

    def _create_directories(self):

        for directory in [self.RAW_DIR, self.PROCESSED_DIR, self.ERROR_DIR]:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Ensured directory exists: {directory}")

    def _extract_icon_number(self, icon_path: str) -> str:
        """Extract the icon number from the icon path."""
        return icon_path.split('/')[-1].replace('.png', '')

    def _format_icon_path(self, icon_path: str) -> str:
        clean_path = icon_path.replace('/i/', '').replace('.png', '')
        return f"https://xivapi.com/i/{clean_path}.png"

    def save_to_json(self, data: Dict[str, Any], status_name: str, data_type: str) -> None:
        """Save API response to a JSON file in the appropriate local directory."""
        directory = {
            'raw': self.RAW_DIR,
            'processed': self.PROCESSED_DIR,
            'error': self.ERROR_DIR
        }.get(data_type, self.ERROR_DIR)

        if data_type == 'processed':
            icon = data['processed_data']['icon']
            name = data['processed_data']['name']
            status_id = data['processed_data']['id']
            filename = os.path.join(directory, f"{icon}_{name}_{status_id}.json")
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(directory, f"{status_name}_{timestamp}.json")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Saved {data_type} response to: {filename}")
        except Exception as e:
            logger.error(f"Error saving JSON to {filename}: {e}", exc_info=True)

    def get_status_info(self, status_name: str) -> Optional[Dict[str, Any]]:
        """Fetch status (status) information from Teamcraft API."""
        sleep(self.RATE_LIMIT_DELAY)
        try:
            search_url = f"{self.base_url}{self.SEARCH_ENDPOINT}"
            params = {"query": status_name, "type": "Status"}
            full_url = f"{search_url}?{urlencode(params)}"

            logger.info(f"Fetching data from: {full_url}")
            response = requests.get(full_url, timeout=self.TIMEOUT)
            response.raise_for_status()

            raw_data = response.json()
            self.save_to_json({
                "request_url": full_url,
                "timestamp": datetime.now().isoformat(),
                "raw_response": raw_data
            }, status_name, 'raw')

            status_data = self._handle_response(raw_data)
            if status_data:
                processed_data = {
                    "processed_data": {
                        "name": status_data["en"],
                        "icon": self._extract_icon_number(status_data["icon"]),
                        "type": status_data["type"],
                        "id": status_data["id"],
                        "api_path": self._format_icon_path(status_data["icon"]),
                        "description": status_data["description"]["en"]
                    }
                }
                self.save_to_json(processed_data, status_name, 'processed')
                return processed_data["processed_data"]
            return None
        except requests.RequestException as e:
            logger.error(f"Network error occurred: {str(e)}")
        except Exception as e:
            logger.error(f"Error fetching status info: {str(e)}", exc_info=True)
        return None

    def _handle_response(self, data: Any) -> Optional[Dict[str, Any]]:
        """Process API response and return relevant status data."""
        try:
            if isinstance(data, list) and data:
                return data[0]
            logger.warning("Empty or unexpected response format.")
            return None
        except Exception as e:
            logger.error(f"Error processing response: {str(e)}", exc_info=True)
            return None


def main():
    api = TeamcraftAPI()
    status_name = input("Enter the status name to search: ")
    status_info = api.get_status_info(status_name)
    if status_info:
        logger.info(f"Type: {status_info['type']}")
        logger.info(f"Status ID: {status_info['id']}")
        logger.info(f"Icon: {status_info['icon']}")
        logger.info(f"Name: {status_info['name']}")
        logger.info(f"API Path: {status_info['api_path']}")
        logger.info(f"Description: {status_info['description']}")

if __name__ == "__main__":
    main()
