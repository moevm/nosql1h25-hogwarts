from models.spell import Spell
from models.character import Character
from neomodel.exceptions import DoesNotExist


class SpellService:
    def __init__(self, database):
        self.db = database

    def create(self, name, **kwargs):
        return Spell(name=name, **kwargs).save()

    def get_all(self, name=None, effect=None, category=None, light=None):
        query = """
                MATCH (s:Spell)
                OPTIONAL MATCH (s)<-[:KNOWS]-(c:Character)
                WHERE ($name IS NULL OR s.name CONTAINS $name)
                  AND ($effect IS NULL OR s.effect CONTAINS $effect)
                  AND ($category IS NULL OR s.category = $category)
                  AND ($light IS NULL OR s.light = $light)
                RETURN s, 
                       collect(DISTINCT c.name) AS known_by
                """

        parameters = {
            'name': name,
            'effect': effect,
            'category': category,
            'light': light
        }

        results, _ = self.db.cypher_query(query, parameters)
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