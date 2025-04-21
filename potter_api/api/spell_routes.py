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
                'id': str(s.id),
                'name': s['name'],
                'image_path': s['image_path'],
                'effect': s['effect'],
                'category': s['category'],
                'light': s.get('light'),
                'known_by': known_by
            })

        return jsonify(spells)

    @app.route('/api/spells/<spell_id>', methods=['GET'])
    def get_spell(spell_id):
        spell = db.spells.get_by_id(spell_id)
        if not spell:
            return jsonify({'error': 'Spells not found'}), 404
        return jsonify({
            'id': str(spell.id),
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
                'id': str(spell.id),
                'name': spell.name
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
