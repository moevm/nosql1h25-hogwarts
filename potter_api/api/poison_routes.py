from flask import jsonify, request


def register_poison_routes(app, db):
    @app.route('/api/potions', methods=['GET'])
    def get_poisons():
        name = request.args.get('name')
        effect = request.args.get('effect')
        ingredients = request.args.get('ingredients')
        difficulty = request.args.get('difficulty')

        name = None if not name else name
        effect = None if not effect else effect
        ingredients = None if not ingredients else ingredients
        difficulty = None if not difficulty else difficulty

        results = db.poisons.get_all(
            name=name,
            effect=effect,
            ingredients=ingredients,
            difficulty=difficulty
        )

        poisons = []
        for record in results:
            p = record[0]
            brewers = record[1]

            poisons.append({
                'id': p['id'],
                'name': p['name'],
                'image_path': p['image_path'],
                'effect': p['effect'],
                'brewers': brewers,
                'ingredients': p['ingredients'],
                'difficulty': p['difficulty'],
                'updated_at': p['updated_at']
            })

        return jsonify(poisons)

    @app.route('/api/potions/<potion_id>', methods=['GET'])
    def get_poison(potion_id):
        poison = db.poisons.get_by_id(potion_id)
        if not poison:
            return jsonify({'error': 'Potion not found'}), 404
        return jsonify({
            'id': poison.id,
            'name': poison.name,
            'image_path': poison.image_path,
            'effect': poison.effect,
            'difficulty': poison.difficulty,
            'ingredients': poison.ingredients,
            'updated_at': poison.updated_at
        })

    @app.route('/api/potions', methods=['POST'])
    def create_poison():
        data = request.json
        try:
            poison = db.poisons.create(
                name=data['name'],
                effect=data.get('effect'),
                difficulty=data.get('difficulty'),
                ingredients=data.get('ingredients'),
            )
            return jsonify({
                'id': poison.id,
                'name': poison.name
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/potions/<potion_id>', methods=['PUT'])
    def update_poisons(potion_id):
        data = request.json
        try:
            from datetime import datetime

            poison = db.poisons.get_by_id(potion_id)
            if not poison:
                return jsonify({'error': 'Potion not found'}), 404

            poison.name = data.get('name')
            poison.effect = data.get('effect')
            poison.difficulty = data.get('difficulty')
            poison.ingredients = data.get('ingredients')
            poison.updated_at = datetime.now()
            poison.save()

            return jsonify({
                'id': poison.id,
                'name': poison.name,
                'message': 'Potion updated successfully'
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400