from flask import jsonify
from neomodel import db

def register_graph_routes(app, _):
    @app.route('/api/relations/<node_type>', methods=['GET'])
    def get_relation_types(node_type):
        try:
            query_types = f"""
            MATCH (n:`{node_type.capitalize()}`)-[r]-()
            RETURN DISTINCT type(r) AS relation_type
            """

            type_results, _ = db.cypher_query(query_types)
            relation_types = [row[0] for row in type_results]

            flat_types = []

            for rel_type in relation_types:
                if rel_type == "HAS_RELATIONSHIP_WITH":
                    sub_query = f"""
                    MATCH (n:`{node_type.capitalize()}`)-[r:`{rel_type}`]-()
                    WHERE exists(r.type)
                    RETURN DISTINCT r.type AS subtype
                    """
                    subtypes_result, _ = db.cypher_query(sub_query)
                    subtypes = [row[0] for row in subtypes_result]
                    flat_types.extend(subtypes)
                else:
                    flat_types.append(rel_type)

            return jsonify({
                'node_type': node_type,
                'relation_types': flat_types
            })

        except Exception as e:
            app.logger.exception("Relation type fetch error")
            return jsonify({'error': str(e)}), 500
