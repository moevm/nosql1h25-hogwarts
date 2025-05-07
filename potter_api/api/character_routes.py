from flask import jsonify, request


def register_character_routes(app, db):
    @app.route('/api/characters', methods=['GET'])
    def get_characters():
        raw = {k: request.args.get(k) for k in [
            'name', 'house', 'blood_status', 'gender', 'born', 'died']}
        filters = {k: v.strip() for k, v in raw.items()
                   if v and v.strip().lower() != 'none'}

        # Диапазоны по born и died
        born_min = request.args.get('born_min')
        born_max = request.args.get('born_max')
        died_min = request.args.get('died_min')
        died_max = request.args.get('died_max')

        try:
            characters = db.characters.get_all(
                **filters,
                born_min=born_min, born_max=born_max,
                died_min=died_min, died_max=died_max
            )
        except Exception as e:
            app.logger.error(e)
            return jsonify({'error': 'Internal server error'}), 500

        return jsonify(characters), 200

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
            'id': character.id,
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
                'id': character.id,
                'name': character.name
            }), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/characters/<character_id>', methods=['PUT'])
    def update_character(character_id):
        data = request.json
        try:
            from models.spell import Spell
            from models.poison import Poison
            from models.house import House
            from models.character import Character

            # Получаем персонажа
            character = db.characters.get_by_id(character_id)
            if not character:
                return jsonify({'error': 'Character not found'}), 404

            # Обновляем основные атрибуты
            character.name = data.get('name', character.name)
            character.born = data.get('born', character.born)
            character.died = data.get('died', character.died)
            character.blood_status = data.get('blood_status', character.blood_status)
            character.gender = data.get('gender', character.gender)
            character.description = data.get('description', character.description)
            character.save()

            # Обновляем дом
            if 'house' in data:
                # Удаляем текущую связь с домом
                for house in character.belongs_to.all():
                    character.belongs_to.disconnect(house)

                # Добавляем новую связь, если указан дом
                if data['house']:
                    house_node = House.nodes.get_or_none(name=data['house'])
                    if house_node:
                        character.belongs_to.connect(house_node)

            # Обновляем заклинания
            if 'spells' in data:
                # Удаляем все текущие связи с заклинаниями
                for spell in character.knows.all():
                    character.knows.disconnect(spell)

                # Добавляем новые связи
                for spell_name in data['spells']:
                    spell = Spell.nodes.get_or_none(name=spell_name)
                    if spell:
                        character.knows.connect(spell)

            # Обновляем яды
            if 'poisons' in data:
                # Удаляем все текущие связи с ядами
                for poison in character.brewed.all():
                    character.brewed.disconnect(poison)

                # Добавляем новые связи
                for poison_name in data['poisons']:
                    poison = Poison.nodes.get_or_none(name=poison_name)
                    if poison:
                        character.brewed.connect(poison)

            # Обновляем отношения
            if 'relationships' in data:
                # Удаляем все текущие отношения
                for target_character in character.relationships.all():
                    character.relationships.disconnect(target_character)

                # Добавляем новые отношения
                for relationship in data['relationships']:
                    target_character_name = relationship['target_character']
                    relationship_type = relationship['type']

                    target_character = Character.nodes.get_or_none(
                        name=target_character_name)
                    if target_character:
                        character.relationships.connect(
                            target_character,
                            {'type': relationship_type}
                        )

            return jsonify({
                'id': character.id,
                'name': character.name,
                'message': 'Character updated successfully'
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400