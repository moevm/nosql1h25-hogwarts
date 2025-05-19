from flask import request, jsonify


def register_statistics_routes(app, db):
    @app.route('/api/statistics', methods=['POST'])
    def get_statistics():
        try:
            payload = request.json
            entity = payload.get("entity")
            filters = payload.get("filters", {})
            x_axis = payload.get("x_axis")
            y_axis = payload.get("y_axis")

            if entity not in ["Character", "Spell", "Poison"]:
                return jsonify({"error": f"Unsupported entity: {entity}"}), 400

            where_clauses = []
            for key, value in filters.items():
                clause = f"n.{key} = '{value}'"
                where_clauses.append(clause)

            where_str = "WHERE " + \
                " AND ".join(where_clauses) if where_clauses else ""

            query = f"""
            MATCH (n:{entity})
            {where_str}
            RETURN n.{x_axis} AS x, n.{y_axis} AS y, COUNT(*) AS count
            ORDER BY x, y
            """

            results, _ = db.execute_query(query)
            data = [{"x": row[0], "y": row[1], "count": row[2]}
                    for row in results]

            return jsonify({"data": data})

        except Exception as e:
            app.logger.exception("Statistics fetch error")
            return jsonify({"error": str(e)}), 500
