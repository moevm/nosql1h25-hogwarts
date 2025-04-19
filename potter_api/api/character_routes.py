from flask import jsonify, request


def register_character_routes(app, db):
    @app.route('/api/characters', methods=['GET'])
    def get_characters():
        from models.character import Character

        characters = db.characters.get_all()
        result = []

        for c in characters:
            house_node = c.belongs_to.single()
            house_name = house_node.name if house_node else None

            spells = [spell.name for spell in c.knows.all()]
            poisons = [poison.name for poison in c.brewed.all()]

            relationships = []
            for target_character in c.relationships.all():
                rel = c.relationships.relationship(target_character)
                relationships.append({
                    'target_character': target_character.name,
                    'type': rel.type
                })

            result.append({
                'id': str(c.id),
                'name': c.name,
                'image_path': c.image_path,
                'born': c.born,
                'died': c.died,
                'house': house_name,
                'blood_status': c.blood_status,
                'gender': c.gender,
                'description': c.description,
                'spells': spells,
                'poisons': poisons,
                'relationships': relationships
            })

        return jsonify(result)

    @app.route('/api/characters/<character_id>', methods=['GET'])
    def get_character(character_id):
        character = db.characters.get_by_id(character_id)
        if not character:
            return jsonify({'error': 'Character not found'}), 404
        house_node = character.belongs_to.single()

        spells = [spell.name for spell in character.knows.all()]
        poisons = [poison.name for poison in character.brewed.all()]

        relationships = []
        for target_character in character.relationships.all():
            rel = character.relationships.relationship(target_character)
            relationships.append({
                'target_character': target_character.name,
                'type': rel.type
            })

        return jsonify({
            'id': str(character.id),
            'name': character.name,
            'image_path': character.image_path,
            'born': character.born,
            'died': character.died,
            'house': house_node.name if house_node else None,
            'blood_status': character.blood_status,
            'gender': character.gender,
            'description': character.description,
            'spells': spells,
            'poisons': poisons,
            'relationships': relationships
        })

    @app.route('/api/characters', methods=['POST'])
    def create_character():
        data = request.json
        try:
            from models.spell import Spell
            from models.poison import Poison
            from models.house import House
            from models.character import Character

            character = db.characters.create(
                name=data['name'],
                born=data['born'],
                died=data['died'],
                blood_status=data.get('blood_status'),
                gender=data.get('gender'),
                description=data.get('description')
            )

            if data.get('house'):
                house_node = House.nodes.get_or_none(name=data['house'])
                if house_node:
                    character.belongs_to.connect(house_node)

            if data.get('spells'):
                for spell_name in data['spells']:
                    spell = Spell.nodes.get_or_none(name=spell_name)
                    if spell:
                        character.knows.connect(spell)

            if data.get('poisons'):
                for poison_name in data['poisons']:
                    poison = Poison.nodes.get_or_none(name=poison_name)
                    if poison:
                        character.brewed.connect(poison)

            if data.get('relationships'):
                for relationship in data['relationships']:
                    target_character_name = relationship['target_character']
                    relationship_type = relationship['type']

                    target_character = Character.nodes.get_or_none(
                        name=target_character_name)
                    if target_character:
                        character.relationships.connect(target_character,
                                                        {'type': relationship_type})

            return jsonify({
                'id': str(character.id),
                'name': character.name
            }), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 400
