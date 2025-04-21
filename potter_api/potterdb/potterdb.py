import requests
import json

BASE_URL = "https://api.potterdb.com/v1"
HEADERS = {"Accept": "application/json"}

def fetch_all(endpoint):
    results = []
    page = 1
    while True:
        url = f"{BASE_URL}/{endpoint}?page[number]={page}&page[size]=100"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Ошибка при запросе {url}: {response.status_code}")
            break
        
        data = response.json().get("data", [])
        if not data:
            break

        results.extend(data)
        print(f"Загружено {len(data)} элементов с {endpoint}, страница {page}")
        page += 1
    
    return results

# все данные
characters = fetch_all("characters")
potions = fetch_all("potions")
spells = fetch_all("spells")

all_data = {
    "characters": characters,
    "potions": potions,
    "spells": spells
}

# в json-файл
with open("./potter_data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print("\nданные сохранены в ./potter_data.json")
