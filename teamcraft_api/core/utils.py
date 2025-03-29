# teamcraft_api/core/utils.py
def extract_icon_number(icon_path: str) -> str:
    return icon_path.split('/')[-1].replace('.png', '')

def format_icon_path(icon_path: str) -> str:
    clean_path = icon_path.replace('/i/', '').replace('.png', '')
    return f"https://xivapi.com/i/{clean_path}.png"
