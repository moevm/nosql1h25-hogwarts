from neomodel import StringProperty, RelationshipTo
from models.base_model import BaseModel
from models.character_relationship import CharacterRelationship
from models.house import House
from models.spell import Spell
from models.poison import Poison


class Character(BaseModel):
    name = StringProperty(required=True, unique_index=True)
    image_path = StringProperty()
    first_mention = StringProperty()
    last_mention = StringProperty()
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
    description = StringProperty()

    # Relationships
    belongs_to = RelationshipTo(House, 'BELONGS_TO')
    knows = RelationshipTo(Spell, 'KNOWS')
    brewed = RelationshipTo(Poison, 'BREWED')
    relationships = RelationshipTo('Character', 'HAS_RELATIONSHIP_WITH',
                                   model=CharacterRelationship)
