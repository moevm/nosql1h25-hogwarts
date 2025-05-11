from models.spell import Spell
from models.character import Character
from neomodel.exceptions import DoesNotExist
from datetime import datetime


class SpellService:
    def __init__(self, database):
        self.db = database

    def create(self, name, **kwargs):
        kwargs['updated_at'] = datetime.now()
        return Spell(name=name, **kwargs).save()

    def get_all(self, name=None, effect=None, category=None, light=None):
        query = """
            MATCH (s:Spell)
            WHERE ($name IS NULL OR toLower(s.name) CONTAINS toLower($name))
              AND ($effect IS NULL OR toLower(s.effect) CONTAINS toLower($effect))
              AND ($category IS NULL OR toLower(s.category) = toLower($category))
              AND ($light IS NULL OR toLower(s.light) = toLower($light))
            OPTIONAL MATCH (s)<-[:KNOWS]-(c:Character)
            RETURN s, collect(DISTINCT c.name) AS known_by
        """

        parameters = {
            'name': name,
            'effect': effect,
            'category': category,
            'light': light
        }

        results, _ = self.db.execute_query(query, parameters)
        return results

    def add_knows(self, char_id, spell_id):
        char = Character.nodes.get(id=char_id)
        spell = Spell.nodes.get(id=spell_id)
        char.knows.connect(spell)
        return True

    def get_by_id(self, spell_id):
        try:
            return Spell.nodes.get(id=spell_id)
        except DoesNotExist:
            return None

    def get_unique_light_values(self):
        query = """
            MATCH (s:Spell)
            WHERE s.light IS NOT NULL
            RETURN DISTINCT s.light
            ORDER BY s.light
        """
        results, _ = self.db.execute_query(query)
        return [result[0] for result in results]
