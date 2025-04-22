from models.character import Character
from neomodel.exceptions import DoesNotExist


class CharacterService:
    def __init__(self, database):
        self.db = database

    def create(self, name, **kwargs):
        return Character(name=name, **kwargs).save()

    def get_all(self, name=None, house=None, blood_status=None, gender=None,
                born=None, died=None, born_min=None, born_max=None, died_min=None, died_max=None):
        qs = Character.nodes

        if name:
            qs = qs.filter(name__icontains=name)
        if blood_status:
            qs = qs.filter(blood_status=blood_status)
        if gender:
            qs = qs.filter(gender=gender)
        if born:
            qs = qs.filter(born=born)
        if died:
            qs = qs.filter(died=died)
        if born_min:
            qs = qs.filter(born__gte=born_min)
        if born_max:
            qs = qs.filter(born__lte=born_max)
        if died_min:
            qs = qs.filter(died__gte=died_min)
        if died_max:
            qs = qs.filter(died__lte=died_max)
        if house:
            qs = qs.filter(belongs_to__name=house)

        characters = []
        for c in qs:
            house_node = c.belongs_to.single()
            spells = [s.name for s in c.knows.all()]
            poisons = [p.name for p in c.brewed.all()]
            relationships = [
                {'target_character': t.name,
                 'type': c.relationships.relationship(t).type}
                for t in c.relationships.all()
            ]
            characters.append({
                'id': c.id,
                'name': c.name,
                'image_path': c.image_path,
                'born': c.born,
                'died': c.died,
                'house': house_node.name if house_node else None,
                'blood_status': c.blood_status,
                'gender': c.gender,
                'description': c.description,
                'spells': spells,
                'poisons': poisons,
                'relationships': relationships
            })
        return characters

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
