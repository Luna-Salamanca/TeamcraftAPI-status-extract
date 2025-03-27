# **Teamcraft API Fetcher**

## **Overview**
This Python script interacts with the *Teamcraft API* to fetch information about status effects (buffs, debuffs, etc.) — and now also Actions if the status isn't found. It saves structured responses locally.

---

## **Features**

✅ Fetches **Status** info from the Teamcraft API  
✅ Automatically falls back to **Action** if Status is not found  
✅ Saves responses in structured folders (`raw/`, `processed/`, `errors/`, `batch/`)  
✅ Provides **xivapi** icon URL for easy embedding  
✅ Optional **quiet mode** for clean batch processing  
✅ Uses `pathlib` and sanitized filenames for better cross-platform support  

---

## **Requirements**

- **Python** `3.7+`
- Install dependencies:
  ```sh
  pip install requests
  ```

---

## **Usage**

### 🔹 Single Lookup

```sh
python main.py
# Enter: 1
# Then: Enter a status or action name like "Weakness" or "Interject"
```

### 🔹 Batch Lookup

```sh
python main.py
# Enter: 2
# Then: Enter the path to a list file (e.g., status_list.txt)
```

Batch mode supports a quiet terminal experience and logs results in a summary file under `api_responses/batch`.

---

## **Example CLI Output**

```
INFO: Searching for status: Interject
INFO: Not found as Status — trying Action instead...
INFO: Found as action: Interject
INFO: Data saved to: api_responses/processed/000808_hr1_Interject_7538.json
```

---

## **Directory Structure**

```
api_responses/
├── raw/        ← full API responses
├── processed/  ← cleaned status/action data
├── errors/     ← failed lookups or exceptions
└── batch/      ← batch run summaries
```

---

## **Example Outputs**

### 🔸 Raw API Response (`raw/`)

```json
{
    "user_input": "Damage",
    "request_url": "https://api.ffxivteamcraft.com/search?query=Damage&type=Status",
    "timestamp": "2025-03-26T17:55:36.662413",
    "raw_response": [
        {
            "en": "Damage Up",
            "de": "Schaden +",
            "ja": "ダメージ上昇",
            "fr": "Bonus de dégâts",
            "ko": "주는 피해량 증가",
            "zh": "伤害提高",
            "id": "61",
            "icon": "/i/215000/215519.png",
            "description": {
                "en": "Damage dealt is increased.",
                "de": "Ausgeteilter Schaden ist erhöht.",
                "ja": "与ダメージが上昇した状態。",
                "fr": "Les dégâts infligés sont augmentés.",
                "ko": "적에게 주는 피해량이 증가하는 상태.",
                "zh": "攻击所造成的伤害提高"
            },
            "type": "Status"
        },
        {
            "en": "Damage Down",
            "de": "Schaden -",
            "ja": "ダメージ低下",
            "fr": "Malus de dégâts",
            "ko": "주는 피해량 감소",
            "zh": "伤害降低",
            "id": "62",
            "icon": "/i/215000/215520.png",
            "description": {
                "en": "Damage dealt is reduced.",
                "de": "Ausgeteilter Schaden ist verringert.",
                "ja": "与ダメージが低下した状態。",
                "fr": "Les dégâts infligés sont réduits.",
                "ko": "적에게 주는 피해량이 감소하는 상태.",
                "zh": "攻击所造成的伤害降低"
            },
            "type": "Status"
        }
        // More entries exist here...
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

## **Using the Icon URLs**

The processed `api_path` field gives you a usable image URL from XIVapi:

```
https://xivapi.com/i/215000/215519.png
```

You can use this directly in frontends, bots, or reports.

---

## **status_list.txt Format**

Each line should be one status or action name. Example:
```
Damage Up
Down for the Count
Interject
Magic Vulnerability Up
```

Lines starting with `//` or empty lines will be ignored.

---

## **Contributing**

Contributions are welcome! Feel free to:
- Open issues for bugs or feature ideas
- Submit a pull request with enhancements

---

## **License**

MIT License — free to use, modify, and distribute.

---

## **Author**

[Luna](https://github.com/Luna-Salamanca)