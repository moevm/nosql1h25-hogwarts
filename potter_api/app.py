from flask import Flask
from services.database import Neo4jDatabase
from api.routes import register_all_routes
from services.faker_seed import faker_seed
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    db = Neo4jDatabase()

    # сидирование
    db.seeding()

    # регистрация всех маршрутов
    register_all_routes(app, db)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)
