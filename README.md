# 📘 About This Project

This project is part of my personal learning journey into **advanced Python concepts** and **real-world software engineering practices**, including:

- Structuring modular Python projects  
- Writing unit tests and handling edge cases  
- Working with external APIs
- Managing data with file I/O and JSON  
- Using GitHub for version control, collaboration, and documentation

It serves as a sandbox to improve my skills in:
- Clean architecture
- Exception handling
- Code maintainability
- Git workflows and pull requests

> I'm using this repository to **learn, iterate, and improve** through hands-on experience.

# 🛠️ Teamcraft API Fetcher

A modular Python CLI tool to fetch, process, and save data from the Teamcraft API.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
---

## 📦 Installation
```bash
# Clone and install in editable mode
pip install -e .
```


---

## ✅ Features

✅ Fetches **Status** info from the Teamcraft API  
✅ Automatically falls back to **Action** if Status is not found  
✅ Saves responses in structured folders (`raw/`, `processed/`, `errors/`, `batch/`) or custom output folder via `--output`  
✅ Provides **xivapi** icon URL for easy embedding  
✅ Optional **quiet mode** for clean batch processing  
✅ Uses `pathlib` and sanitized filenames for cross-platform safety

---

## 🚀 Usage

### 🔹 Single Lookup (Interactive)
```bash
python -m teamcraft_api --status "Interject"
```

### 🔹 Batch Lookup
```bash
python -m teamcraft_api --batch ./data/status_list.txt
```

### 🔹 Quiet Batch
```bash
python -m teamcraft_api --batch ./data/status_list.txt --quiet
```

### 🔹 Specify Output Directory
```bash
python -m teamcraft_api --status "Damage Up" --output ./custom_output/
```

---

## 📂 Directory Structure
```
api_responses/ or --output path
├── raw/        ← full API responses
├── processed/  ← cleaned status/action data
├── errors/     ← failed lookups or exceptions
└── batch/      ← batch run summaries
```

---

## 📘 Example CLI Output
```
INFO: Searching for status: Interject
INFO: Not found as Status — trying Action instead...
INFO: Found as action: Interject
INFO: Data saved to: api_responses/processed/000808_hr1_Interject_7538.json
```

---

## 📦 Example Outputs

### 🔸 Raw API Response (`raw/`)
```json
{
  "user_input": "Damage",
  "timestamp": "2025-03-26T17:55:36.662413",
  "raw_response": [
    {
      "en": "Damage Up",
      "id": "61",
      "icon": "/i/215000/215519.png",
      "description": { "en": "Damage dealt is increased." },
      "type": "Status"
    }
  ]
}
```

### 🔸 Processed Output (`processed/`)
```json
{
  "processed_data": {
    "name": "Damage Up",
    "icon": "215519",
    "type": "Status",
    "id": "61",
    "api_path": "https://xivapi.com/i/215000/215519.png",
    "description": "Damage dealt is increased."
  }
}
```

---

## 🌐 Using the Icon URLs

The processed `api_path` field gives you a usable image URL from XIVapi:
```
https://xivapi.com/i/215000/215519.png
```
Use it in frontends, bots, dashboards, or embedded UIs.

---

## 📄 status_list.txt Format
Each line should be one status or action name. Comments (//) and blanks are ignored.
```
Damage Up
Down for the Count
Interject
Magic Vulnerability Up
```

---

## ✅ Testing & Coverage

### 🔸 Windows
```bash
.\make.bat test       # Run all tests
.\make.bat coverage   # Run tests with coverage report
.\make.bat clean      # Clean cache and build artifacts
```

### 🔸 Linux/macOS
```bash
make test
make coverage
make clean
```

> Ensure you have a GNU Makefile if using Linux/macOS. See `make.bat` for equivalent commands.
> Not tested on Linux/macOS yet.
---

## 🧪 Requirements
- Python 3.7+
- requests, pytest, pytest-cov, build
Install all development dependencies with:
```bash
pip install -e ".[dev]"
```
---

## 🤝 Contributing
- Open issues for bugs or feature ideas
- Submit pull requests to enhance functionality

---

## 👤 Author
[Luna](https://github.com/Luna-Salamanca)

---

## 📄 License
MIT — free to use, modify, and distribute.
