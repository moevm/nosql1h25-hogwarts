from flask import Flask
from services.database import Neo4jDatabase
from api.routes import register_all_routes
from services.faker_seed import faker_seed


def create_app():
    app = Flask(__name__)
    db = Neo4jDatabase()

    # для дебага
    db.clear_data()

    # сидирование
    faker_seed(db=db, num_characters=20, num_houses=4,
               num_poisons=25, num_spells=10)

    # регистрация всех маршрутов
    register_all_routes(app, db)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)
