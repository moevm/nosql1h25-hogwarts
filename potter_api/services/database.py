from neomodel import config, db
from config import Config
from character_service import CharacterService
from house_service import HouseService
from poison_service import PoisonService
from spell_service import SpellService


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
