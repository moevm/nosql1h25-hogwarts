from neomodel import config, db
from config import Config
from character_services import CharacterService


class Neo4jDatabase:
    def __init__(self):
        config.DATABASE_URL = Config.DATABASE_URL
        self.db = db
        self.characters = CharacterService(self)

    def clear_data(self):
        self.db.cypher_query("MATCH (n) DETACH DELETE n")

    def execute_query(self, query, params=None):
        return self.db.cypher_query(query, params)
