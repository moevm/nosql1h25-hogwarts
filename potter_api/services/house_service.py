from models.house import House
from models.character import Character


class HouseService:
    def __init__(self, database):
        self.db = database

    def create(self, name, **kwargs):
        return House(name=name, **kwargs).save()

    def get_all(self):
        return House.nodes.all()

    def assign_character(self, char_id, house_id):
        char = Character.nodes.get(id=char_id)
        house = House.nodes.get(id=house_id)
        char.belongs_to.connect(house)
        return True
