# teamcraft_api/constants/config.py
from pathlib import Path

# API Configuration
BASE_URL = "https://api.ffxivteamcraft.com/"
SEARCH_ENDPOINT = "search"
TIMEOUT = 10
RATE_LIMIT_DELAY = 0

# Directory Paths
BASE_DIR = Path("api_responses")
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"
ERROR_DIR = BASE_DIR / "errors"
BATCH_DIR = BASE_DIR / "batch"
