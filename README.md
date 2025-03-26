# Teamcraft API Fetcher

## Overview
This Python script interacts with the FFXIV Teamcraft API to fetch information about status effects (debuffs, buffs, etc.). It allows users to search for a status by name and retrieves relevant data, including ID, type, icon, and description.

## Features
- Fetches status information from the Teamcraft API
- Saves API responses in structured directories (`raw`, `processed`, `errors`)
- Logs important details for debugging and tracking requests
- Handles API rate limits and exceptions gracefully

## Requirements
- Python 3.7+
- The following dependencies:
  - `requests`
  - `logging`
  - `json`
  - `os`
  - `time`
  - `datetime`

## Install dependencies:
   ```sh
   pip install requests
   ```

## Usage
Run the script and input the name of the status you want to search for:

```sh
python main.py
```

The script will:
1. Prompt for a status name.
2. Query the Teamcraft API.
3. Display the retrieved information.
4. Save responses to the `api_responses/` directory.

## Example Output
```
Enter the status name to search: Boiling
INFO:root:Fetching data from: https://api.ffxivteamcraft.com/search?query=Boiling&type=Status
INFO:root:Type: Debuff
INFO:root:Status ID: 12345
INFO:root:Icon: 215459
INFO:root:Name: Boiling
INFO:root:API Path: https://xivapi.com/i/215000/215459.png
INFO:root:Description: Increases damage taken.
```
## Raw Output
```json
    "request_url": "https://api.ffxivteamcraft.com//search?query=boiling&type=Status",
    "timestamp": "2025-03-26T05:49:03.906864",
    "raw_response": [
        {
            "en": "Boiling",
            "de": "Nagende Hitze",
            "ja": "徐々にヒート",
            "fr": "Chaleur graduelle",
            "ko": "서서히 열병",
            "zh": "逐渐升温",
            "id": "2898",
            "icon": "/i/215000/215459.png",
            "description": {
                "en": "Body is slowly heating up. Will become <span style=\"color:#ffffff\">Pyretic</span> when this effect expires.",
                "de": "Nach Ablauf der Wirkungsdauer tritt der Status <span style=\"color:#ffffff\">Pyretisch</span> ein.",
                "ja": "徐々に熱せられつつある状態。効果終了時にヒート状態になる。",
                "fr": "Le corps chauffe petit à petit. Lorsque l'effet prend fin, la victime subit Chaleur.",
                "ko": "서서히 열이 오르는 상태. 효과가 끝날 때 열병 상태가 된다.",
                "zh": "逐渐变热，效果结束时会陷入过热状态"
            },
            "type": "Status"
```

## Processed Output
```json
{
    "processed_data": {
        "name": "Boiling",
        "icon": "215459",
        "type": "Status",
        "id": "2898",
        "api_path": "https://xivapi.com/i/215000/215459.png",
        "description": "Body is slowly heating up. Will become <span style=\"color:#ffffff\">Pyretic</span> when this effect expires."
    }
}
```

## License

This project is open-source under the MIT License.

## Contributions
Feel free to submit issues or pull requests to improve functionality.

