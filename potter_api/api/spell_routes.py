from flask import jsonify, request


def register_spell_routes(app, db):
    @app.route('/api/spells', methods=['GET'])
    def get_spells():
        name = request.args.get('name')
        effect = request.args.get('effect')
        category = request.args.get('category')
        light = request.args.get('light')

        name = None if not name else name
        effect = None if not effect else effect
        category = None if not category else category
        light = None if not light else light

        page = int(request.args.get('page'))
        per_page = 50
        results = db.spells.get_all(
            name=name,
            effect=effect,
            category=category,
            light=light
        )

        spells = []
        for record in results:
            s = record[0]
            known_by = record[1]

            spells.append({
                'id': s['id'],
                'name': s['name'],
                'image_path': s['image_path'],
                'effect': s['effect'],
                'category': s['category'],
                'light': s.get('light'),
                'known_by': known_by,
                'updated_at': s['updated_at']
            })

        total_count = len(spells)

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_spells = spells[start_idx:end_idx]

        response = {
            'data': paginated_spells,
            'pagination': {
                'total': total_count,
                'page': page,
                'per_page': per_page,
                'total_pages': (total_count + per_page - 1) // per_page
            }
        }

        return jsonify(response), 200   

    @app.route('/api/spells/<spell_id>', methods=['GET'])
    def get_spell(spell_id):
        spell = db.spells.get_by_id(spell_id)
        if not spell:
            return jsonify({'error': 'Spells not found'}), 404
        return jsonify({
            'id': spell.id,
            'name': spell.name,
            'image_path': spell.image_path,
            'effect': spell.effect,
            'category': spell.category,
            'light': spell.light
        })

    @app.route('/api/spells', methods=['POST'])
    def create_spell():
        data = request.json
        try:
            spell = db.spells.create(
                name=data['name'],
                effect=data.get('effect'),
                category=data.get('category'),
                light=data.get('light')
            )
            return jsonify({
                'id': spell.id,
                'name': spell.name
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/spells/<spell_id>', methods=['PUT'])
    def update_spell(spell_id):
        data = request.json
        try:
            from datetime import datetime

            spell = db.spells.get_by_id(spell_id)
            if not spell:
                return jsonify({'error': 'Spell not found'}), 404

            spell.name = data.get('name')
            spell.effect = data.get('effect')
            spell.category = data.get('category')
            spell.light = data.get('light')
            spell.updated_at = datetime.now()
            spell.save()

            return jsonify({
                'id': spell.id,
                'name': spell.name,
                'message': 'Spell updated successfully'
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/spells/filters', methods=['GET'])
    def get_spell_filters_arr():
        try:
            light_values = db.spells.get_unique_light_values()
            category_values = db.spells.get_unique_category_values()

            return jsonify({
                'light': light_values,
                'category': category_values
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
