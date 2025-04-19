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
