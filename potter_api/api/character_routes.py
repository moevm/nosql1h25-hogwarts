from flask import jsonify, request


def register_character_routes(app, db):
    @app.route('/api/characters', methods=['GET'])
    def get_characters():
        characters = db.characters.get_all()
        return jsonify([{
            'id': str(c.id),
            'name': c.name,
            'house': c.house,
            'blood_status': c.blood_status
        } for c in characters])

    @app.route('/api/characters/<character_id>', methods=['GET'])
    def get_character(character_id):
        character = db.characters.get_by_id(character_id)
        if not character:
            return jsonify({'error': 'Character not found'}), 404
        return jsonify({
            'id': str(character.id),
            'name': character.name,
            'house': character.house,
            'blood_status': character.blood_status,
            'description': character.description
        })

    @app.route('/api/characters', methods=['POST'])
    def create_character():
        data = request.json
        try:
            character = db.characters.create(
                name=data['name'],
                house=data.get('house'),
                blood_status=data.get('blood_status'),
                gender=data.get('gender'),
                description=data.get('description')
            )
            return jsonify({
                'id': str(character.id),
                'name': character.name
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
