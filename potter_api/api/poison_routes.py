from flask import jsonify, request


def register_poison_routes(app, db):
    @app.route('/api/poisons', methods=['GET'])
    def get_poisons():
        name = request.args.get('name')
        effect = request.args.get('effect')
        ingredients = request.args.get('ingredients')
        difficulty = request.args.get('difficulty')

        results = db.poisons.get_all(
            name=name,
            effect=effect,
            ingredients=ingredients,
            difficulty=difficulty
        )

        poisons = []
        for record in results:
            p, brewers = record

            poisons.append({
                'id': str(p.id),
                'name': p.name,
                'image_path': p.image_path,
                'effect': p.effect,
                'brewers': brewers,
                'ingredients': p.ingredients,
                'difficulty': p.difficulty
            })

        return jsonify(poisons)

    # def get_poisons():
    #     poisons = db.poisons.get_all()
    #     return jsonify([{
    #         'id': str(poison.id),
    #         'name': poison.name,
    #         'image_path': poison.image_path,
    #         'effect': poison.effect,
    #         'difficulty': poison.difficulty
    #     } for poison in poisons])

    @app.route('/api/poisons/<poison_id>', methods=['GET'])
    def get_poison(poison_id):
        poison = db.poisons.get_by_id(poison_id)
        if not poison:
            return jsonify({'error': 'Poison not found'}), 404
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
                ingredients=data.get('ingredients')
            )
            return jsonify({
                'id': str(poison.id),
                'name': poison.name
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
