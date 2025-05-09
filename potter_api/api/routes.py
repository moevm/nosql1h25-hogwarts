from api.character_routes import register_character_routes
from api.house_routes import register_house_routes
from api.poison_routes import register_poison_routes
from api.spell_routes import register_spell_routes
from api.port_routes import register_port_routes
from api.graph_routes import register_graph_routes
from api.statistics_routes import register_statistics_routes


def register_all_routes(app, db):
    # маршруты для всех сущностей
    register_character_routes(app, db)
    register_house_routes(app, db)
    register_poison_routes(app, db)
    register_spell_routes(app, db)
    register_port_routes(app, db)
    register_graph_routes(app, db)
    register_statistics_routes(app, db)
