from models.character import Character
from neomodel.exceptions import DoesNotExist


class CharacterService:
    def __init__(self, database):
        self.db = database

    def create(self, name, **kwargs):
        return Character(name=name, **kwargs).save()

    def get_all(self, name=None, house=None, blood_status=None, gender=None, born=None, died=None):
        filters = []
        parameters = {}

        if name:
            filters.append("c.name CONTAINS $name")
            parameters["name"] = name
        if blood_status:
            filters.append("c.blood_status = $blood_status")
            parameters["blood_status"] = blood_status
        if gender:
            filters.append("c.gender = $gender")
            parameters["gender"] = gender
        if born:
            filters.append("c.born = $born")
            parameters["born"] = born
        if died:
            filters.append("c.died = $died")
            parameters["died"] = died
        if house:
            filters.append("h.name = $house")
            parameters["house"] = house

        where_clause = " AND ".join(filters) if filters else "1=1"

        query = f"""
            MATCH (c:Character)
            OPTIONAL MATCH (c)-[:BELONGS_TO]->(h:House)
            OPTIONAL MATCH (c)-[:KNOWS]->(s:Spell)
            OPTIONAL MATCH (c)-[:BREWED]->(p:Poison)
            OPTIONAL MATCH (c)-[r:RELATIONSHIP]->(target:Character)
            WHERE {where_clause}
            RETURN c, h,
                   collect(DISTINCT s.name) AS spells,
                   collect(DISTINCT p.name) AS poisons,
                   collect(DISTINCT {{target: target.name, type: r.type}}) AS relationships
        """

        results, _ = self.db.execute_query(query, parameters)
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
