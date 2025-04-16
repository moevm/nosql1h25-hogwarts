from character_routes import register_character_routes
from house_routes import register_house_routes
from poison_routes import register_poison_routes
from spell_routes import register_spell_routes


def register_all_routes(app, db):
    # маршруты для всех сущностей
    register_character_routes(app, db)
    register_house_routes(app, db)
    register_poison_routes(app, db)
    register_spell_routes(app, db)
