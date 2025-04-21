from models.character import Character
from neomodel.exceptions import DoesNotExist


class CharacterService:
    def __init__(self, database):
        self.db = database

    def create(self, name, **kwargs):
        return Character(name=name, **kwargs).save()

    def get_all(self):
        return Character.nodes.all()

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
