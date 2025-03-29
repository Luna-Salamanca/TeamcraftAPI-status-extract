# tests/test_batch.py
import pytest
from teamcraft_api.core.api import TeamcraftAPI
from teamcraft_api.processing.batch_processor import batch_process_status
from pathlib import Path

def test_batch_process_with_known_status(tmp_path):
    filename = tmp_path / "input.txt"
    filename.write_text("Bloodbath\n")
    api = TeamcraftAPI(quiet=True)

    results = batch_process_status(api, str(filename))
    assert "status_effects" in results or "actions" in results
    assert results["metadata"]["total_effects"] == 1


def test_batch_process_with_invalid_and_comment_lines(tmp_path):
    content = """
    // This is a comment
    UnknownStatus
    \n
    	// Another comment line
    Bloodbath
    """
    filename = tmp_path / "list.txt"
    filename.write_text(content)
    api = TeamcraftAPI(quiet=True)

    results = batch_process_status(api, str(filename))
    assert results["metadata"]["total_effects"] == 2
    assert "failed_lookups" in results


def test_batch_with_duplicates_and_empty_lines(tmp_path):
    content = """
    Bloodbath
    
    Bloodbath
    UnknownStatus
    """
    filename = tmp_path / "duplicates.txt"
    filename.write_text(content)
    api = TeamcraftAPI(quiet=True)

    results = batch_process_status(api, str(filename))
    assert results["metadata"]["total_effects"] == 2  # after deduplication
    assert len(results["failed_lookups"]) >= 0


def test_batch_with_empty_file(tmp_path):
    filename = tmp_path / "empty.txt"
    filename.write_text("")
    api = TeamcraftAPI(quiet=True)

    results = batch_process_status(api, str(filename))
    assert results["metadata"]["total_effects"] == 0
    assert results["status_effects"] == []
    assert results["actions"] == []
    assert results["failed_lookups"] == []