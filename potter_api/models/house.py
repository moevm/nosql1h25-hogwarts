from neomodel import StringProperty
from models.base_model import BaseModel


class House(BaseModel):
    name = StringProperty(required=True, unique_index=True)
    founder = StringProperty()
    image_path = StringProperty()
