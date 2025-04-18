from models.poison import Poison
from models.character import Character
from neomodel.exceptions import DoesNotExist


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

    def get_by_id(self, poison_id):
        try:
            return Poison.nodes.get(id=poison_id)
        except DoesNotExist:
            return None

