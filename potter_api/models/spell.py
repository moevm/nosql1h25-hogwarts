from neomodel import StringProperty
from models.base_model import BaseModel


class Spell(BaseModel):
    name = StringProperty(required=True, unique_index=True)
    effect = StringProperty()
    type = StringProperty()
