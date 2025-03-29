# tests/conftest.py
import sys
from pathlib import Path

# Ensure the teamcraft_api module is discoverable
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
