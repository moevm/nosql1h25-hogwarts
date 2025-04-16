from neomodel import StringProperty
from models.base_model import BaseModel


class Poison(BaseModel):
    name = StringProperty(required=True, unique_index=True)
    effect = StringProperty()
    difficulty = StringProperty()
