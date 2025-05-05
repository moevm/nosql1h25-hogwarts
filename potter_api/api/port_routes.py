from flask import request, jsonify
from neomodel.exceptions import DoesNotExist
from models.poison import Poison
from models.spell import Spell
from models.house import House
from models.character import Character
from flask import jsonify, request


def register_port_routes(app, db):
    @app.route('/api/export', methods=['GET'])
    def export_database():
        try:
            # Characters
            characters_json = []
            characters = Character.nodes.all()
            for c in characters:
                house = c.belongs_to.single()
                characters_json.append({
                    'name': c.name,
                    'born': c.born,
                    'died': c.died,
                    'blood_status': c.blood_status,
                    'gender': c.gender,
                    'description': c.description,
                    'house': house.name if house else None,
                    'spells': [s.name for s in c.knows.all()],
                    'poisons': [p.name for p in c.brewed.all()],
                    'relationships': [
                        {
                            'target_character': target.name,
                            'type': c.relationships.relationship(target).type
                        }
                        for target in c.relationships.all()
                    ],
                    'image_path': c.image_path
                })

            # Potions
            potions = db.poisons.get_all()
            potions_json = [{
                'name': p[0]['name'],
                'effect': p[0]['effect'],
                'difficulty': p[0]['difficulty'],
                'ingredients': p[0]['ingredients'],
                'image_path': p[0]['image_path']
            } for p in potions]

            # Spells
            spells = db.spells.get_all()
            spells_json = [{
                'name': s[0]['name'],
                'effect': s[0]['effect'],
                'category': s[0]['category'],
                'light': s[0]['light'],
                'image_path': s[0]['image_path']
            } for s in spells]

            # Houses
            houses = db.houses.get_all()
            houses_json = [{
                'name': h.name,
                'founder': h.founder
            } for h in houses]

            return jsonify({
                'characters': characters_json,
                'potions': potions_json,
                'spells': spells_json,
                'houses': houses_json
            })

        except Exception as e:
            app.logger.error(f"Export error: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/import', methods=['POST'])
    def import_database():
        data = request.get_json()

        # очистка
        db.clear_data()

        house_map = {}
        character_map = {}
        spell_map = {}
        poison_map = {}

        for h in data.get('houses', []):
            house = House(name=h['name'], traits=h.get('traits', [])).save()
            house_map[house.name] = house

        for s in data.get('spells', []):
            spell = Spell(name=s['name'], effect=s.get(
                'effect'), category=s.get('category'), light=s.get('light')).save()
            spell_map[spell.name] = spell

        for p in data.get('potions', []):
            poison = Poison(name=p['name'], effect=p.get(
                'effect'), difficulty=p.get('difficulty'), ingredients=p.get('ingredients')).save()
            poison_map[poison.name] = poison

        for c in data.get('characters', []):
            char = Character(
                name=c['name'],
                born=c['born'],
                died=c['died'],
                blood_status=c.get('blood_status'),
                gender=c.get('gender'),
                description=c.get('description')
            ).save()
            character_map[char.name] = char

            house_name = c.get('house')
            if house_name and house_name in house_map:
                char.belongs_to.connect(house_map[house_name])

        for c in data.get('characters', []):
            char = character_map[c['name']]

            for spell_name in c.get('spells', []):
                if spell_name in spell_map:
                    char.knows.connect(spell_map[spell_name])

            for poison_name in c.get('poisons', []):
                if poison_name in poison_map:
                    char.brewed.connect(poison_map[poison_name])

        for c in data.get('characters', []):
            char = character_map[c['name']]
            for rel in c.get('relationships', []):
                target_name = rel['target_character']
                rel_type = rel['type']
                if target_name in character_map:
                    char.relationships.connect(
                        character_map[target_name], {'type': rel_type})

        return jsonify({'status': 'imported successfully'})
