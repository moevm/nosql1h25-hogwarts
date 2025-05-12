from models.poison import Poison
from models.character import Character
from neomodel.exceptions import DoesNotExist
from datetime import datetime


class PoisonService:
    def __init__(self, database):
        self.db = database

    def create(self, name, **kwargs):
        kwargs['updated_at'] = datetime.now()
        return Poison(name=name, **kwargs).save()

    def get_all(self, name=None, effect=None, ingredients=None, difficulty=None):
        query = """
                MATCH (p:Poison)
                WHERE ($name IS NULL OR toLower(p.name) CONTAINS toLower($name))
                  AND ($effect IS NULL OR toLower(p.effect) CONTAINS toLower($effect))
                  AND ($ingredients IS NULL OR toLower(p.ingredients) CONTAINS toLower($ingredients))
                  AND ($difficulty IS NULL OR toLower(p.difficulty) = toLower($difficulty))
                OPTIONAL MATCH (p)<-[:BREWED]-(c:Character)
                RETURN p, 
                       collect(DISTINCT c.name) AS brewers
                """

        parameters = {
            'name': name,
            'effect': effect,
            'ingredients': ingredients,
            'difficulty': difficulty
        }

        results, _ = self.db.execute_query(query, parameters)
        return results

    def add_brewed(self, char_id, poison_id):
        char = Character.nodes.get(id=char_id)
        poison = Poison.nodes.get(id=poison_id)
        char.brewed.connect(poison)
        return True

    def get_by_id(self, poison_id):
        try:
            return Poison.nodes.get(id=poison_id)
        except DoesNotExist:
            return None

    def get_unique_ingredients_values(self):
        query = """
            MATCH (s:Poison)
            WHERE s.ingredients IS NOT NULL
            RETURN DISTINCT s.ingredients
            ORDER BY s.ingredients
        """
        results, _ = self.db.execute_query(query)
        return [result[0] for result in results]

    def get_unique_difficulty_values(self):
        query = """
            MATCH (s:Poison)
            WHERE s.difficulty IS NOT NULL
            RETURN DISTINCT s.difficulty
            ORDER BY s.difficulty
        """
        results, _ = self.db.execute_query(query)
        return [result[0] for result in results]