from models.character import Character, CharacterRelationship
from services.database import Neo4jDatabase


class CharacterService(Neo4jDatabase):
    def create_character(self, name, house=None, blood_status=None, gender=None, description=None):
        return Character(
            name=name,
            house=house,
            blood_status=blood_status,
            gender=gender,
            description=description
        ).save()

    def get_all_characters(self):
        return Character.nodes.all()

    def add_relationship(self, char1_id, char2_id, rel_type):
        char1 = Character.nodes.get(id=char1_id)
        char2 = Character.nodes.get(id=char2_id)

        if rel_type not in CharacterRelationship.type.choices:
            raise ValueError(
                f"Invalid relationship type. Allowed: {list(CharacterRelationship.type.choices.keys())}")

        char1.relationships.connect(char2, {'type': rel_type})
        return True

    def get_character_relationships(self, char_id, rel_type=None):
        char = Character.nodes.get(id=char_id)
        if rel_type:
            return [rel for rel in char.relationships.all()
                    if char.relationships.relationship(rel).type == rel_type]
        return char.relationships.all()

    def get_relationship_properties(self, char_id, related_char_id):
        char = Character.nodes.get(id=char_id)
        related = Character.nodes.get(id=related_char_id)
        return char.relationships.relationship(related)
