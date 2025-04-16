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
