from flask import jsonify
from neomodel import db

def register_relations_routes(app, _):
    @app.route('/api/relations/<node_type>', methods=['GET'])
    def get_relation_types(node_type):
        try:
            query = f"""
            MATCH (n:`{node_type.capitalize()}`)-[r]-(m)
            WITH type(r) AS rel_type, labels(m) AS labels, r
            UNWIND labels AS label
            WITH 
                CASE 
                    WHEN rel_type = 'HAS_RELATIONSHIP_WITH' AND r.type IS NOT NULL THEN r.type
                    ELSE rel_type
                END AS final_type,
                label
            RETURN label, collect(DISTINCT final_type) AS relation_types
            """

            results, _ = db.cypher_query(query)
            relation_map = {}

            for label, rel_types in results:
                relation_map[label] = rel_types

            return jsonify({
                "node_type": node_type,
                "relation_map": relation_map
            })

        except Exception as e:
            app.logger.exception("Relation type fetch error")
            return jsonify({'error': str(e)}), 500
