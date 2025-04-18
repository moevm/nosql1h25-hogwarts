from flask import jsonify, request


def register_poison_routes(app, db):
    @app.route('/api/poisons', methods=['GET'])
    def get_poisons():
        poisons = db.poisons.get_all()
        return jsonify([{
            'id': str(poison.id),
            'name': poison.name,
            'effect': poison.effect,
            'difficulty': poison.difficulty
        } for poison in poisons])

    @app.route('/api/poisons/<poison_id>', methods=['GET'])
    def get_poison(poison_id):
        poison = db.poisons.get_by_id(poison_id)
        if not poison:
            return jsonify({'error': 'Character not found'}), 404
        return jsonify({
            'id': str(poison.id),
            'name': poison.name,
            'effect': poison.effect,
            'difficulty': poison.difficulty
        })

    @app.route('/api/poisons', methods=['POST'])
    def create_poison():
        data = request.json
        try:
            poison = db.poisons.create(
                name=data['name'],
                effect=data.get('effect'),
                difficulty=data.get('difficulty'),
            )
            return jsonify({
                'id': str(poison.id),
                'name': poison.name
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
