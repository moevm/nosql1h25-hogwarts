from neomodel import StringProperty, TextProperty
from base_model import BaseModel


class Spell(BaseModel):
    name = StringProperty(required=True, unique_index=True)
    effect = TextProperty()
    type = StringProperty()
