from flask import request, jsonify
from neomodel import db

# конфиг связей
RELATION_CONFIG = {
    'Character': {
        'house': {
            'rel': 'BELONGS_TO', 'alias': 'h', 'label': 'House', 'prop': 'name', 'direction': 'out'
        },
    },
    'Spell': {
        'known_by': {
            'rel': 'KNOWS', 'alias': 'c', 'label': 'Character', 'prop': 'name', 'direction': 'in'
        }
    },
    'Poison': {
        'brewed_by': {
            'rel': 'BREWED', 'alias': 'c', 'label': 'Character', 'prop': 'name', 'direction': 'in'
        }
    }
}

def register_statistics_routes(app, db):
    @app.route('/api/statistics', methods=['POST'])
    def get_statistics():
        payload = request.json
        entity = payload.get("entity")
        filters = payload.get("filters", {})
        x_axis = payload.get("x_axis")
        y_axis = payload.get("y_axis")

        if entity not in RELATION_CONFIG:
            return jsonify({"error": f"Unsupported entity: {entity}"}), 400

        extra_matches = []
        where_clauses = []

        # обработка фильтров
        for key, value in filters.items():
            # диапазонные фильтры: born_min, born_max, died_min, died_max
            if key.endswith("_min") or key.endswith("_max"):
                field, typ = key.rsplit("_", 1)
                op = ">=" if typ == "min" else "<="
                # приводим текст в число
                where_clauses.append(f"toInteger(n.{field}) {op} {value}")
                continue

            # фильтры по связям из конфига
            rel_cfg = RELATION_CONFIG[entity].get(key)
            if rel_cfg:
                alias = rel_cfg['alias']
                rel   = rel_cfg['rel']
                label = rel_cfg['label']
                prop  = rel_cfg['prop']
                if rel_cfg['direction'] == 'out':
                    extra_matches.append(f"(n)-[:{rel}]->({alias}:{label})")
                else:
                    extra_matches.append(f"({alias}:{label})-[:{rel}]->(n)")
                where_clauses.append(f"{alias}.{prop} = '{value}'")
                continue

            # простые свойства узла
            where_clauses.append(f"n.{key} = '{value}'")

        # преобразование осей в части MATCH и RETURN
        def axis_to_cypher(axis):
            cfg = RELATION_CONFIG[entity].get(axis)
            if cfg:
                alias = cfg['alias']
                rel   = cfg['rel']
                label = cfg['label']
                prop  = cfg['prop']
                if cfg['direction'] == 'out':
                    match_part = f"(n)-[:{rel}]->({alias}:{label})"
                else:
                    match_part = f"({alias}:{label})-[:{rel}]->(n)"
                return match_part, f"{alias}.{prop} AS {axis}"
            else:
                return "", f"n.{axis} AS {axis}"

        x_match, x_ret = axis_to_cypher(x_axis)
        y_match, y_ret = axis_to_cypher(y_axis)

        # сборка MATCH
        all_matches = [f"(n:{entity})"] + extra_matches
        if x_match:
            all_matches.append(x_match)
        if y_match and y_match != x_match:
            all_matches.append(y_match)

        match_clause = "MATCH " + ", ".join(all_matches)
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        return_clause = f"{x_ret}, {y_ret}, COUNT(*) AS count"

        cypher = f"""
        {match_clause}
        {where_clause}
        RETURN {return_clause}
        ORDER BY {x_axis}, {y_axis}
        """

        try:
            results, _ = db.execute_query(cypher)
            data = [{"x": row[0], "y": row[1], "count": row[2]} for row in results]
            return jsonify({"data": data})

        except Exception as e:
            app.logger.exception("Statistics fetch error")
            return jsonify({"error": str(e)}), 500
