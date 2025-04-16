from flask import jsonify, request


def register_poison_routes(app, db):
    @app.route('/api/poisons', methods=['GET'])
    def get_poisons():
        pass

    @app.route('/api/poisons/<poison_id>', methods=['GET'])
    def get_poison(poison_id):
        pass

    @app.route('/api/poisons', methods=['POST'])
    def create_poison():
        pass
