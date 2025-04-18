from flask import jsonify, request


def register_port_routes(app, db):
    @app.route('/api/export', methods=['GET'])
    def export_database():
        characters = [{
            'id': str(c.id),
            'name': c.name,
            'house': (c.belongs_to.single().name if c.belongs_to.single() else None),
            'blood_status': c.blood_status
        } for c in db.characters.get_all()]

        poisons = [{
            'id': str(poison.id),
            'name': poison.name,
            'effect': poison.effect,
            'difficulty': poison.difficulty
        } for poison in db.poisons.get_all()]

        spells = [{
            'id': str(spell.id),
            'name': spell.name,
            'effect': spell.effect,
            'type': spell.type
        } for spell in db.spells.get_all()]

        return jsonify({
            'characters': characters,
            'poisons': poisons,
            'spells': spells
        })
