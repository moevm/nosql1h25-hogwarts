from flask import jsonify
from models.character import Character
from models.spell import Spell
from models.poison import Poison


def register_graph_routes(app, db):
    @app.route('/api/graph/<node_type>/<id>', methods=['GET'])
    def get_graph_by_id(node_type, id):
        try:
            node = None
            if node_type == 'character':
                node = Character.nodes.get_or_none(id=id)
            elif node_type == 'spell':
                node = Spell.nodes.get_or_none(id=id)
            elif node_type == 'poison':
                node = Poison.nodes.get_or_none(id=id)
            else:
                return jsonify({'error': f'Unknown node type: {node_type}'}), 400

            if not node:
                return jsonify({'error': f'{node_type} with id {id} not found'}), 404

            nodes = []
            edges = []
            seen = set()

            def add_node(obj, node_type):
                if obj.id in seen:
                    return
                seen.add(obj.id)
                nodes.append({
                    'id': obj.id,
                    'name': obj.name,
                    'type': node_type,
                    'image_path': obj.image_path if node_type != 'House' else None
                })

            add_node(node, node_type.capitalize())

            if node_type == 'character':
                for spell in node.knows.all():
                    add_node(spell, 'Spell')
                    edges.append({'source': node.id, 'target': spell.id, 'type': 'knows'})

                for poison in node.brewed.all():
                    add_node(poison, 'Poison')
                    edges.append({'source': node.id, 'target': poison.id, 'type': 'brewed'})

                house = node.belongs_to.single()
                if house:
                    add_node(house, 'House')
                    edges.append({'source': node.id, 'target': house.id, 'type': 'belongs_to'})

                for rel_target in node.relationships.all():
                    rel = node.relationships.relationship(rel_target)
                    add_node(rel_target, 'Character')
                    edges.append({'source': node.id, 'target': rel_target.id, 'type': rel.type})

            elif node_type in ['spell', 'poison']:
                for character in Character.nodes.all():
                    if node_type == 'spell' and node in character.knows.all():
                        add_node(character, 'Character')
                        edges.append({'source': character.id, 'target': node.id, 'type': 'knows'})
                    elif node_type == 'poison' and node in character.brewed.all():
                        add_node(character, 'Character')
                        edges.append({'source': character.id, 'target': node.id, 'type': 'brewed'})

            return jsonify({'nodes': nodes, 'edges': edges})

        except Exception as e:
            app.logger.exception("Graph fetch error")
            return jsonify({'error': str(e)}), 500
