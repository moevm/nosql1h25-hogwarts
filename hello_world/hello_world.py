from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, IntegerProperty, config, db
import os
from dotenv import load_dotenv


# загружаем переменные окружения
load_dotenv()

config.DATABASE_URL = os.getenv("DATABASE_URL")


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

    friends = RelationshipTo('Character', 'FRIEND')
    enemies = RelationshipTo('Character', 'ENEMY')


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

    harry.brewed_poison.connect(veritaserum)

    harry.friends.connect(hermione)
    harry.friends.connect(ron)
    ron.friends.connect(hermione)
    voldemort.enemies.connect(harry)


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

        friends = char.friends.all()
        if friends:
            print("  Friends:")
            for friend in friends:
                print(f"    - {friend.name}")

        enemies = char.enemies.all()
        if enemies:
            print("  Enemies:")
            for enemy in enemies:
                print(f"    - {enemy.name}")


if __name__ == "__main__":
    create_data()
    read_data()
