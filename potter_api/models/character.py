from neomodel import StringProperty, RelationshipTo, TextProperty
from .base_model import BaseModel
from .character_relationship import CharacterRelationship


class Character(BaseModel):
    name = StringProperty(required=True, unique_index=True)
    house = StringProperty()
    blood_status = StringProperty(choices={
        'pure-blood': 'Pure-blood',
        'half-blood': 'Half-blood',
        'muggle-born': 'Muggle-born',
        'unknown': 'Unknown'
    })
    gender = StringProperty(choices={
        'male': 'Male',
        'female': 'Female',
        'other': 'Other'
    })
    description = TextProperty()

    # Relationships
    belongs_to = RelationshipTo('House', 'BELONGS_TO')
    knows = RelationshipTo('Spell', 'KNOWS')
    brewed = RelationshipTo('Poison', 'BREWED')
    relationships = RelationshipTo('Character', 'HAS_RELATIONSHIP_WITH',
                                   model=CharacterRelationship)
