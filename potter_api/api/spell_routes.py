from flask import jsonify, request


def register_spell_routes(app, db):
    @app.route('/api/spells', methods=['GET'])
    def get_spells():
        spells = db.spells.get_all()
        return jsonify([{
            'id': str(spell.id),
            'name': spell.name,
            'image_path': spell.image_path,
            'effect': spell.effect,
            'type': spell.type
        } for spell in spells])

    @app.route('/api/spells/<spell_id>', methods=['GET'])
    def get_spell(spell_id):
        spell = db.poisons.get_by_id(spell_id)
        if not spell:
            return jsonify({'error': 'Character not found'}), 404
        return jsonify({
            'id': str(spell.id),
            'name': spell.name,
            'image_path': spell.image_path,
            'effect': spell.effect,
            'type': spell.type
        })

    @app.route('/api/spells', methods=['POST'])
    def create_spell():
        data = request.json
        try:
            spell = db.spells.create(
                name=data['name'],
                effect=data.get('effect'),
                type=data.get('type'),
            )
            return jsonify({
                'id': str(spell.id),
                'name': spell.name
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
