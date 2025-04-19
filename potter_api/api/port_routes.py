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
        characters = []
        for c in db.characters.get_all():
            house_node = c.belongs_to.single()
            house_name = house_node.name if house_node else None

            spells = [spell.name for spell in c.knows.all()]
            poisons = [poison.name for poison in c.brewed.all()]

            relationships = []
            for target_character in c.relationships.all():
                rel = c.relationships.relationship(target_character)
                relationships.append({
                    'target_character': target_character.name,
                    'type': rel.type
                })

            characters.append({
                'id': str(c.id),
                'name': c.name,
                'image_path': c.image_path,
                'born': c.born,
                'died': c.died,
                'house': house_name,
                'blood_status': c.blood_status,
                'gender': c.gender,
                'description': c.description,
                'spells': spells,
                'poisons': poisons,
                'relationships': relationships
            })

        spells = [{
            'id': str(spell.id),
            'name': spell.name,
            'image_path': spell.image_path,
            'effect': spell.effect,
            'type': spell.type
        } for spell in db.spells.get_all()]

        poisons = [{
            'id': str(poison.id),
            'name': poison.name,
            'image_path': poison.image_path,
            'effect': poison.effect,
            'difficulty': poison.difficulty
        } for poison in db.poisons.get_all()]

        return jsonify({
            'characters': characters,
            'spells': spells,
            'poisons': poisons
        })

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
                'effect'), type=s.get('type')).save()
            spell_map[spell.name] = spell

        for p in data.get('poisons', []):
            poison = Poison(name=p['name'], effect=p.get(
                'effect'), difficulty=p.get('difficulty')).save()
            poison_map[poison.name] = poison

        for c in data.get('characters', []):
            char = Character(
                name=c['name'],
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
