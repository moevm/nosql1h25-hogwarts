from flask import request, jsonify
from neomodel.exceptions import DoesNotExist
from models.poison import Poison
from models.spell import Spell
from models.house import House
from models.character import Character
from flask import jsonify, request


def run_import(data, db, app=None):
    try:
        # Импорт заклинаний
        for s in data.get('spells', []):
            if not Spell.nodes.get_or_none(name=s['name']):
                db.spells.create(
                    name=s['name'],
                    effect=s.get('effect'),
                    category=s.get('category'),
                    light=s.get('light'),
                    image_path=s.get('image_path')
                )

        # Импорт зелий
        for p in data.get('potions', []):
            if not Poison.nodes.get_or_none(name=p['name']):
                db.poisons.create(
                    name=p['name'],
                    effect=p.get('effect'),
                    difficulty=p.get('difficulty'),
                    ingredients=p.get('ingredients'),
                    image_path=p.get('image_path')
                )

        # Импорт факультетов
        for h in data.get('houses', []):
            if not House.nodes.get_or_none(name=h['name']):
                db.houses.create(
                    name=h['name'],
                    founder=h.get('founder')
                )

        # Импорт персонажей
        for c in data.get('characters', []):
            if not Character.nodes.get_or_none(name=c['name']):
                character = db.characters.create(
                    name=c['name'],
                    born=c.get('born'),
                    died=c.get('died'),
                    blood_status=c.get('blood_status'),
                    gender=c.get('gender'),
                    description=c.get('description'),
                    image_path=c.get('image_path')
                )

                if c.get('house'):
                    house = House.nodes.get_or_none(name=c['house'])
                    if house:
                        character.belongs_to.connect(house)

                for spell_name in c.get('spells', []):
                    spell = Spell.nodes.get_or_none(name=spell_name)
                    if spell:
                        character.knows.connect(spell)

                for poison_name in c.get('poisons', []):
                    poison = Poison.nodes.get_or_none(name=poison_name)
                    if poison:
                        character.brewed.connect(poison)

        # Обработка связей после всех персонажей
        for c in data.get('characters', []):
            source = Character.nodes.get_or_none(name=c['name'])
            if source and c.get('relationships'):
                for rel in c['relationships']:
                    target = Character.nodes.get_or_none(
                        name=rel['target_character'])
                    if target:
                        source.relationships.connect(
                            target, {'type': rel['type']})
        return True
    except Exception as e:
        if app:
            app.logger.error(f"Import error: {e}")
        else:
            print(f"[ERROR] Import error: {e}")
        return False

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
        db.clear_data()
        data = request.json
        success = run_import(data, db, app)
        if success:
            return jsonify({'message': 'Data imported successfully'}), 201
        else:
            return jsonify({'error': 'Import failed'}), 400
