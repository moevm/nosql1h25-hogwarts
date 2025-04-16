from neomodel import config, db
from config import Config


class Neo4jDatabase:
    def __init__(self):
        config.DATABASE_URL = Config.DATABASE_URL
        self.db = db

    def clear_all_data(self):
        self.db.cypher_query("MATCH (n) DETACH DELETE n")

