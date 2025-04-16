from neomodel import StringProperty, TextProperty
from base_model import BaseModel


class Poison(BaseModel):
    name = StringProperty(required=True, unique_index=True)
    effect = TextProperty()
    difficulty = StringProperty()
