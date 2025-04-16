from flask import jsonify, request


def register_character_routes(app, db):
    @app.route('/api/characters', methods=['GET'])
    def get_characters():
        characters = db.characters.get_all()
        return jsonify([{
            'id': str(c.id),
            'name': c.name,
            'house': (c.belongs_to.single().name if c.belongs_to.single() else None),
            'blood_status': c.blood_status
        } for c in characters])

    @app.route('/api/characters/<character_id>', methods=['GET'])
    def get_character(character_id):
        character = db.characters.get_by_id(character_id)
        if not character:
            return jsonify({'error': 'Character not found'}), 404
        house_node = character.belongs_to.single()
        return jsonify({
            'id': str(character.id),
            'name': character.name,
            'house': house_node.name if house_node else None,
            'blood_status': character.blood_status,
            'description': character.description
        })

    @app.route('/api/characters', methods=['POST'])
    def create_character():
        data = request.json
        try:
            character = db.characters.create(
                name=data['name'],
                blood_status=data.get('blood_status'),
                gender=data.get('gender'),
                description=data.get('description')
            )

            if data.get('house'):
                from models.house import House
                house_node = House.nodes.get_or_none(name=data['house'])
                if house_node:
                    character.belongs_to.connect(house_node)

            return jsonify({
                'id': str(character.id),
                'name': character.name
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
