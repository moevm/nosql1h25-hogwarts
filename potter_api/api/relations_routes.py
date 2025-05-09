from flask import jsonify
from neomodel import db

def register_graph_routes(app, _):
    @app.route('/api/relations/<node_type>', methods=['GET'])
    def get_relation_types(node_type):
        try:
            query = f"""
            MATCH (n:`{node_type.capitalize()}`)-[r]-()
            RETURN DISTINCT type(r) AS relation_type
            """

            results, _ = db.cypher_query(query)

            relations = [row[0] for row in results]

            return jsonify({
                'node_type': node_type,
                'relation_types': relations
            })

        except Exception as e:
            app.logger.exception("Relation type fetch error")
            return jsonify({'error': str(e)}), 500
