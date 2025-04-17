from models.spell import Spell
from models.character import Character


class SpellService:
    def __init__(self, database):
        self.db = database

    def create(self, name, effect=None, type=None):
        return Spell(name=name, effect=effect, type=type).save()

    def get_all(self):
        return Spell.nodes.all()

    def add_knows(self, char_id, spell_id):
        char = Character.nodes.get(id=char_id)
        spell = Spell.nodes.get(id=spell_id)
        char.knows.connect(spell)
        return True

    def get_by_id(self, spell_id):
        spell = Spell.nodes.get(id=spell_id)
        return spell