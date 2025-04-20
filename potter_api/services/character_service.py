from models.character import Character
from neomodel.exceptions import DoesNotExist


class CharacterService:
    def __init__(self, database):
        self.db = database

    def create(self, name, **kwargs):
        return Character(name=name, **kwargs).save()

    def get_all(self, name=None, house=None, blood_status=None, gender=None, born=None, died=None):
        query = """
                MATCH (c:Character)
                OPTIONAL MATCH (c)-[:BELONGS_TO]->(h:House)
                OPTIONAL MATCH (c)-[:KNOWS]->(s:Spell)
                OPTIONAL MATCH (c)-[:BREWED]->(p:Poison)
                OPTIONAL MATCH (c)-[r:RELATIONSHIP]->(target:Character)
                WHERE ($name IS NULL OR c.name CONTAINS $name)
                  AND ($house IS NULL OR h.name = $house)
                  AND ($blood_status IS NULL OR c.blood_status = $blood_status)
                  AND ($gender IS NULL OR c.gender = $gender)
                  AND ($born IS NULL OR c.born = $born)
                  AND ($died IS NULL OR c.died = $died)
                RETURN c, h, 
                       collect(DISTINCT s.name) AS spells, 
                       collect(DISTINCT p.name) AS poisons, 
                       collect(DISTINCT {target: target.name, type: r.type}) AS relationships
                """

        parameters = {
            'name': name,
            'house': house,
            'blood_status': blood_status,
            'gender': gender,
            'born': born,
            'died': died
        }

        results, _ = self.db.cypher_query(query, parameters)
        return results

    def get_by_id(self, char_id):
        try:
            return Character.nodes.get(id=char_id)
        except DoesNotExist:
            return None

    def add_relationship(self, char1_id, char2_id, rel_type):
        char1 = Character.nodes.get(id=char1_id)
        char2 = Character.nodes.get(id=char2_id)
        char1.relationships.connect(char2, {'type': rel_type})
        return True

    def get_relationships(self, char_id, rel_type=None):
        char = Character.nodes.get(id=char_id)
        if rel_type:
            return [rel for rel in char.relationships.all()
                    if char.relationships.relationship(rel).type == rel_type]
        return char.relationships.all()
