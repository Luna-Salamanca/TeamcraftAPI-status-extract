# tests/test_cli.py
import subprocess
import sys
import os
import pytest

def test_cli_status_runs():
    result = subprocess.run(
        [sys.executable, '-m', 'teamcraft_api', '--status', 'Bloodbath'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Bloodbath" in result.stdout or "Found as" in result.stdout


def test_cli_batch_missing_file():
    result = subprocess.run(
        [sys.executable, '-m', 'teamcraft_api', '--batch', 'nonexistent.txt'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "File not found" in result.stdout or result.stderr
