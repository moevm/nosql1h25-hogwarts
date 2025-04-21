from flask import jsonify, request


def register_house_routes(app, db):
    @app.route('/api/houses', methods=['GET'])
    def get_houses():
        houses = db.houses.get_all()
        return jsonify([{
            'id': str(h.id),
            'name': h.name,
            'founder': h.founder
        } for h in houses])
    
    @app.route('/api/houses', methods=['POST'])
    def create_houses():
        data = request.json
        try:
            house = db.houses.create(
                name=data['name'],
                founder=data.get('founder')
            )
            return jsonify({
                'name': str(house.name),
                'founder': house.founder
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    