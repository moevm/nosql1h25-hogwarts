from models.poison import Poison
from models.character import Character


class PoisonService:
    def __init__(self, database):
        self.db = database

    def create(self, name, effect=None, difficulty=None):
        return Poison(name=name, effect=effect, difficulty=difficulty).save()

    def get_all(self):
        return Poison.nodes.all()

    def add_brewed(self, char_id, poison_id):
        char = Character.nodes.get(id=char_id)
        poison = Poison.nodes.get(id=poison_id)
        char.brewed.connect(poison)
        return True
