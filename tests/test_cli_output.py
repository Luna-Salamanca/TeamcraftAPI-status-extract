# tests/test_cli_output.py
import shutil
import sys
from pathlib import Path
from subprocess import run

def test_status_output_to_custom_dir(tmp_path):
    # Create output directory
    out_dir = tmp_path / "outbox"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Get the Python executable path from sys.executable
    python_exe = sys.executable

    cmd = [
        python_exe,  # Use the current Python interpreter
        "-m", "teamcraft_api",
        "--status", "Interject",
        "--output", str(out_dir)
    ]

    # Run command and capture output
    result = run(cmd, capture_output=True, text=True)
    
    # Print debug information
    print("\nCommand:", " ".join(cmd))
    print("\nSTDOUT:", result.stdout)
    print("\nSTDERR:", result.stderr)
    print("\nReturn code:", result.returncode)
    
    if result.returncode != 0:
        print("\nOutput directory contents:")
        if out_dir.exists():
            for p in out_dir.rglob("*"):
                print(f"  {p}")
        else:
            print("  Output directory does not exist")

    # Assertions with detailed error messages
    assert result.returncode == 0, f"Command failed with error: {result.stderr}"
    assert (out_dir / "processed").exists(), f"'processed' directory not found in {out_dir}"
    
    # Check for JSON files
    json_files = list(out_dir.glob("processed/*.json"))
    assert json_files, f"No JSON files found in {out_dir}/processed/"
    
    # Print found JSON files
    print("\nFound JSON files:")
    for json_file in json_files:
        print(f"  {json_file}")

def teardown_module(module):
    """Clean up any remaining test artifacts"""
    paths_to_clean = ["outbox", "api_responses"]
    for path in paths_to_clean:
        if Path(path).exists():
            print(f"\nCleaning up {path}")
            shutil.rmtree(path, ignore_errors=True)

if __name__ == "__main__":
    # Allow running test directly
    import pytest
    pytest.main([__file__, "-v", "-s"])
