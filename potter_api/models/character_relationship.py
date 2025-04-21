from neomodel import StructuredRel, StringProperty


class CharacterRelationship(StructuredRel):
    type = StringProperty(required=True)
