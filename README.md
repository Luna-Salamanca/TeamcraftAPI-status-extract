# **Teamcraft API Fetcher**  

## **Overview**  
This Python script interacts with the *Final Fantasy XIV Teamcraft API* to fetch information about status effects (buffs, debuffs, etc.). It allows users to search for a status by name and retrieves relevant data such as ID, type, icon, and description.  

## **Features**  
✅ Fetches status information from the Teamcraft API  
✅ Saves API responses in structured directories (`raw/`, `processed/`)  
✅ Handles API rate limits and retries automatically  
✅ Logs requests and responses for debugging  
✅ Processes and formats retrieved data for easy use  
✅ Provides a direct *xivapi* link for the status effect icon for easy usage in applications  

## **Requirements**  

- **Python** `3.7+`  
- Install dependencies with:  
  ```sh
  pip install requests
  ```

## **Usage**  

Run the script and enter the status name you want to search for:  

```sh
python main.py
```
```sh
Enter the status name to search: Damage
```

The script will:  
1. Query the Teamcraft API  
2. Display the retrieved status information  
3. Save API responses in structured JSON format  

### **Example Output:**  

```
INFO: Searching for status: Damage
INFO: Fetching data from: https://api.ffxivteamcraft.com/search?query=Damage&type=Status
INFO: Status ID: 61
INFO: Type: Status
INFO: Name: Damage Up
INFO: Icon: 215519
INFO: API Path: https://xivapi.com/i/215000/215519.png
INFO: Description: Damage dealt is increased.
INFO: Data saved successfully.
```

---

## **Data Structure**  

### **Raw API Response (`raw/` directory)**  
- Able to see all queries made with the user input
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

### **Processed Data (`processed/` directory)**  

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

### **Icon Usage with XIVAPI**  

The `icon` field in the API response provides a path like `/i/215000/215519.png`. You can use this to get the full URL of the icon by appending it to `https://xivapi.com`, resulting in:  

```
https://xivapi.com/i/215000/215519.png
```

This URL can be used directly in applications to display the status effect's icon.  

---

## **Contributing**  
Contributions are welcome! Feel free to submit an issue or pull request to improve functionality.  

## **License**  
This project is open-source under the **MIT License**.  

---
