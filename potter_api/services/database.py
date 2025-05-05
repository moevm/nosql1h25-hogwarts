import json
import os
from neomodel import config, db
from config import Config
from services.character_service import CharacterService
from services.house_service import HouseService
from services.poison_service import PoisonService
from services.spell_service import SpellService
from api.port_routes import run_import


class Neo4jDatabase:
    def __init__(self):
        config.DATABASE_URL = Config.DATABASE_URL
        self.db = db
        self.characters = CharacterService(self)
        self.houses = HouseService(self)
        self.poisons = PoisonService(self)
        self.spells = SpellService(self)

    def clear_data(self):
        self.db.cypher_query("MATCH (n) DETACH DELETE n")

    def execute_query(self, query, params=None):
        return self.db.cypher_query(query, params)

    def is_db_empty(self):
        result, _ = self.db.cypher_query("MATCH (n) RETURN COUNT(n) AS count")
        return result[0][0] == 0

    def seeding(self, path='data/data_dump.json', port=5000):
        if not os.path.exists(path):
            print(f"Dump file not found: {path}")
            return

        if not self.is_db_empty():
            print("Database already populated. Skipping import.")
            return

        print("Database is empty. Importing data from dump...")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            success = run_import(data, self)

            if not success:
                print("Import failed.")
            else:
                print("Import completed successfully.")
        except Exception as e:
            print(f"Import error: {e}")
