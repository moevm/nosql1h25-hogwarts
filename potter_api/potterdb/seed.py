import requests
import json

API_URL = "https://api.potterdb.com/v1"
IMPORT_ENDPOINT = "http://localhost:5000/api/import"

HEADERS = {"Accept": "application/json"}

def fetch_all(endpoint):
    results = []
    page = 1
    while True:
        url = f"{API_URL}/{endpoint}?page[number]={page}&page[size]=100"
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print(f"Ошибка запроса: {url}")
            break
        data = resp.json().get("data", [])
        if not data:
            break
        results.extend(data)
        page += 1
    return results

def transform_data(characters, spells, potions):
    def safe_attr(attr, default=None):
        return attr if attr is not None else default

    transformed = {
        "houses": [],
        "spells": [],
        "poisons": [],
        "characters": []
    }

    for s in spells:
        attr = s['attributes']
        transformed["spells"].append({
            "name": attr["name"],
            "effect": attr.get("effect"),
            "category": attr.get("type"),
            "light": attr.get("light")
        })

    for p in potions:
        attr = p['attributes']
        transformed["poisons"].append({
            "name": attr["name"],
            "effect": attr.get("effect"),
            "difficulty": attr.get("difficulty"),
            "ingredients": attr.get("ingredients", [])
        })

    for c in characters:
        attr = c['attributes']
        transformed["characters"].append({
            "name": attr["name"],
            "born": attr.get("born"),
            "died": attr.get("died"),
            "blood_status": attr.get("blood_status"),
            "gender": attr.get("gender"),
            "description": attr.get("description"),
            "house": attr.get("house"),
            "spells": [],
            "poisons": [],
            "relationships": []
        })

    return transformed

def main():
    characters = fetch_all("characters")
    spells = fetch_all("spells")
    potions = fetch_all("potions")

    data = transform_data(characters, spells, potions)

    # на /api/import
    resp = requests.post(IMPORT_ENDPOINT, json=data)
    print("Status:", resp.status_code)
    print("Response text:", resp.text)

    try:
        print(resp.json())
    except Exception as e:
        print("Ошибка парсинга JSON:", e)


if __name__ == "__main__":
    main()
