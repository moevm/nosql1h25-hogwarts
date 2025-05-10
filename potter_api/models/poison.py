from neomodel import StringProperty
from models.base_model import BaseModel


class Poison(BaseModel):
    name = StringProperty(required=True, unique_index=True)
    image_path = StringProperty()
    effect = StringProperty()
    difficulty = StringProperty()
    ingredients = StringProperty()
    updated_at = StringProperty()
