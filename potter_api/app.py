from flask import Flask
from services.database import Neo4jDatabase
from api.routes import register_all_routes


def create_app():
    app = Flask(__name__)
    db = Neo4jDatabase()

    # для дебага
    db.clear_data()

    # регистрация всех маршрутов
    register_all_routes(app, db)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)
