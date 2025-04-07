from neomodel import StructuredNode, StringProperty, Relationship, RelationshipTo, StructuredRel, config, db
import os
from dotenv import load_dotenv
from collections import defaultdict


# загружаем переменные окружения
load_dotenv()

config.DATABASE_URL = os.getenv("DATABASE_URL")


class CharacterRelationship(StructuredRel):
    type = StringProperty(required=True)


class House(StructuredNode):
    name = StringProperty(unique_index=True)


class Spell(StructuredNode):
    uid = StringProperty(unique_index=True)
    name = StringProperty()
    effect = StringProperty()
    type = StringProperty()


class Poison(StructuredNode):
    uid = StringProperty(unique_index=True)
    name = StringProperty()
    effect = StringProperty()
    difficulty = StringProperty()


class Character(StructuredNode):
    uid = StringProperty(unique_index=True)
    name = StringProperty()
    house = StringProperty()
    bloodStatus = StringProperty()
    gender = StringProperty()
    description = StringProperty()

    belongs_to = RelationshipTo('House', 'BELONGS_TO')
    knows_spell = RelationshipTo('Spell', 'KNOWS')
    brewed_poison = RelationshipTo('Poison', 'BREWED')

    relationships = RelationshipTo('Character', 'HAS_RELATIONSHIP_WITH',
                                   model=CharacterRelationship)


def clear_data():
    db.cypher_query("MATCH (n) DETACH DELETE n")


def create_data():
    clear_data()

    gryffindor = House(name='Gryffindor').save()
    slytherin = House(name='Slytherin').save()

    harry = Character(
        uid='1',
        name='Harry Potter',
        house='Gryffindor',
        bloodStatus='Half-blood',
        gender='Male',
        description='The Boy Who Lived'
    ).save()

    hermione = Character(
        uid='2',
        name='Hermione Granger',
        house='Gryffindor',
        bloodStatus='Muggle-born',
        gender='Female',
        description='The brightest witch of her age'
    ).save()

    ron = Character(
        uid='3',
        name='Ron Weasley',
        house='Gryffindor',
        bloodStatus='Pure-blood',
        gender='Male',
        description='Harry’s best friend'
    ).save()

    voldemort = Character(
        uid='4',
        name='Lord Voldemort',
        house='Slytherin',
        bloodStatus='Half-blood',
        gender='Male',
        description='The Dark Lord'
    ).save()

    expelliarmus = Spell(
        uid='1',
        name='Expelliarmus',
        effect='Disarms opponent',
        type='Charm'
    ).save()

    avada_kedavra = Spell(
        uid='2',
        name='Avada Kedavra',
        effect='Kills instantly',
        type='Unforgivable Curse'
    ).save()

    veritaserum = Poison(
        uid='1',
        name='Veritaserum',
        effect='Truth serum',
        difficulty='Hard to brew'
    ).save()

    harry.belongs_to.connect(gryffindor)
    hermione.belongs_to.connect(gryffindor)
    ron.belongs_to.connect(gryffindor)
    voldemort.belongs_to.connect(slytherin)

    harry.knows_spell.connect(expelliarmus)
    hermione.knows_spell.connect(expelliarmus)
    voldemort.knows_spell.connect(avada_kedavra)
    voldemort.knows_spell.connect(expelliarmus)

    harry.brewed_poison.connect(veritaserum)

    harry.relationships.connect(hermione, {'type': 'Friend'})
    harry.relationships.connect(ron, {'type': 'Friend'})
    ron.relationships.connect(hermione, {'type': 'Friend'})
    ron.relationships.connect(voldemort, {'type': 'Friend'})
    hermione.relationships.connect(voldemort, {'type': 'Enemy'})

    voldemort.relationships.connect(harry, {'type': 'Enemy'})


def read_data():
    print("\nCharacters:")
    characters = Character.nodes.all()
    for char in characters:
        print(f"\n{char.name} ({char.house}) - {char.description}")

        house = char.belongs_to.all()
        if house:
            print(f"  Belongs to: {house[0].name}")

        spells = char.knows_spell.all()
        if spells:
            print("  Knows spells:")
            for spell in spells:
                print(f"    - {spell.name} ({spell.type}): {spell.effect}")

        poisons = char.brewed_poison.all()
        if poisons:
            print("  Brewed poisons:")
            for poison in poisons:
                print(
                    f"    - {poison.name}: {poison.effect} (Difficulty: {poison.difficulty})")

        print("  Relationships:")
        for rel in char.relationships.all():
            rel_props = char.relationships.relationship(rel)
            print(f"    - {rel_props.type} with {rel.name}")


def find_conflicting_friendships():
    """
    Враг моего врага - мой друг
    """
    query = """
    MATCH (a:Character)-[r1:HAS_RELATIONSHIP_WITH {type: 'Friend'}]-(b:Character),
          (b)-[r2:HAS_RELATIONSHIP_WITH {type: 'Enemy'}]-(c:Character),
          (a)-[r3:HAS_RELATIONSHIP_WITH {type: 'Friend'}]-(c)
    RETURN a.name AS person1, b.name AS person2, c.name AS person3
    """
    results, meta = db.cypher_query(query)

    print("\nConflicting friendships (enemy of my friend is my friend too):")
    for row in results:
        print(f"{row[0]} is friends with {row[1]}, who is enemies with {row[2]}, but {row[0]} is also friends with {row[2]}")


def find_least_conflicted_house():
    """
    Находит факультет с наименьшим количеством вражеских отношений
    """
    query = """
    MATCH (h:House)<-[:BELONGS_TO]-(c:Character)-[r:HAS_RELATIONSHIP_WITH {type: 'Enemy'}]-(other:Character)
    WITH h, COUNT(r) AS conflict_count
    ORDER BY conflict_count ASC
    RETURN h.name AS house_name, conflict_count
    """
    results, meta = db.cypher_query(query)

    if results:
        print(
            f"\nHouse with least conflicts: {results[0][0]} ({results[0][1]} conflicts)")
    else:
        print("\nNo conflicts found between houses")


def find_unique_spells_by_house():
    """
    Находит уникальные заклинания по факультетам (которые или совсем не представлены
    у учащихся других факультетов, или данный факультет чаще всех их использует)
    """
    query = """
    MATCH (h:House)<-[:BELONGS_TO]-(c:Character)-[:KNOWS]->(s:Spell)
    WITH h, s, COUNT(c) AS house_count
    OPTIONAL MATCH (other:Character)-[:KNOWS]->(s) 
    WHERE NOT (other)-[:BELONGS_TO]->(h)
    WITH h, s, house_count, COUNT(other) AS other_count
    WHERE other_count = 0 OR house_count > other_count
    RETURN h.name AS house, s.name AS spell, 
           CASE WHEN other_count = 0 THEN 'Уникальное' ELSE 'Чаще всего используется' END AS type
    ORDER BY house, type, spell
    """

    results, meta = db.cypher_query(query)

    house_spells = defaultdict(list)
    for house, spell, spell_type in results:
        house_spells[house].append((spell, spell_type))

    print("\nUnique or mostly used spells by house:")
    for house, spells in house_spells.items():
        print(f"\n{house}:")
        for spell, spell_type in spells:
            print(f"  - {spell} ({spell_type})")


if __name__ == "__main__":
    create_data()
    read_data()

    find_conflicting_friendships()
    find_least_conflicted_house()
    find_unique_spells_by_house()
