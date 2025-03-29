# tests/test_api.py
from teamcraft_api.core.api import TeamcraftAPI
from teamcraft_api.processing.status_handler import lookup_status_or_action

def test_lookup_known_status():
    api = TeamcraftAPI(quiet=True)
    result = lookup_status_or_action(api, "Bloodbath")
    assert result is not None
    assert result['type'] in ("status", "action")
    assert "name" in result["data"]


def test_lookup_unknown_status():
    api = TeamcraftAPI(quiet=True)
    result = lookup_status_or_action(api, "DefinitelyNotARealStatus")
    assert result is None
