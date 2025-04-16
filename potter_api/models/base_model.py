from neomodel import StructuredNode, UniqueIdProperty
from uuid import uuid4


class BaseModel(StructuredNode):
    __abstract_node__ = True
    id = UniqueIdProperty(default=uuid4)
