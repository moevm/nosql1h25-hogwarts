from flask import jsonify, request


def register_spell_routes(app, db):
    @app.route('/api/spells', methods=['GET'])
    def get_spells():
        pass

    @app.route('/api/spells/<spell_id>', methods=['GET'])
    def get_spell(spell_id):
        pass

    @app.route('/api/spells', methods=['POST'])
    def create_spell():
        pass
