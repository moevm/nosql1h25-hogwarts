from flask import jsonify, request


def register_poison_routes(app, db):
    @app.route('/api/poisons', methods=['GET'])
    def get_poisons():
        poisons = db.poisons.get_all()
        return jsonify([{
            'id': str(poison.id),
            'name': poison.name,
            'image_path': poison.image_path,
            'effect': poison.effect,
            'difficulty': poison.difficulty,
            'ingredients': poison.ingredients
        } for poison in poisons])

    @app.route('/api/poisons/<poison_id>', methods=['GET'])
    def get_poison(poison_id):
        poison = db.poisons.get_by_id(poison_id)
        if not poison:
            return jsonify({'error': 'Character not found'}), 404
        return jsonify({
            'id': str(poison.id),
            'name': poison.name,
            'image_path': poison.image_path,
            'effect': poison.effect,
            'difficulty': poison.difficulty,
            'ingredients': poison.ingredients
        })

    @app.route('/api/poisons', methods=['POST'])
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
                'id': str(poison.id),
                'name': poison.name
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
