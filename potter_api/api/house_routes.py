from flask import jsonify, request


def register_house_routes(app, db):
    @app.route('/api/houses', methods=['GET'])
    def get_houses():
        houses = db.houses.get_all()
        return jsonify([{
            'id': h.id,
            'name': h.name,
            'founder': h.founder,
            'image_path': h.image_path,
        } for h in houses])
    
    @app.route('/api/houses', methods=['POST'])
    def create_houses():
        data = request.json
        try:
            house = db.houses.create(
                name=data['name'],
                founder=data.get('founder'),
                image_path=data.get('image_path')
            )
            return jsonify({
                'name': house.name,
                'founder': house.founder,
                'image_path': house.image_path
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    