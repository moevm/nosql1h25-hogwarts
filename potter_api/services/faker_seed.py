from faker import Faker
import random
from services.database import Neo4jDatabase

fake = Faker()


def faker_seed(
    db,
    num_characters=10,
    num_houses=4,
    num_spells=10,
    num_poisons=5,
):
    print("очистка бд...")
    db.clear_data()

    print(f"создание {num_houses} факультетов...")
    house_ids = []
    houses_names = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
    for i in range(num_houses):
        name = houses_names[i]
        founder = fake.name()
        house = db.houses.create(name=name, founder=founder)
        house_ids.append(house.id)

    print(f"создание {num_spells} заклинаний...")
    spell_ids = []
    for _ in range(num_spells):
        name = fake.unique.word().capitalize()
        effect = fake.sentence()
        category = random.choice(['Charm', 'Hex', 'Curse', 'Spell'])
        light = random.choice(['red', 'blue', 'green', 'none'])
        spell = db.spells.create(
            name=name, effect=effect, category=category, light=light)
        spell_ids.append(spell.id)

    print(f"создание {num_poisons} зелий...")
    poison_ids = []
    for _ in range(num_poisons):
        name = fake.unique.word().capitalize() + " Poison"
        effect = fake.sentence()
        difficulty = random.choice(['Easy', 'Medium', 'Hard'])
        ingredients = ", ".join(fake.words(nb=3))
        poison = db.poisons.create(
            name=name, effect=effect, difficulty=difficulty, ingredients=ingredients)
        poison_ids.append(poison.id)

    print(f"создание {num_characters} персонажей...")
    blood_statuses = ['Pure-blood', 'Half-blood', 'Muggle-born']
    genders = ['Male', 'Female']

    char_ids = []
    for _ in range(num_characters):
        name = fake.name()
        description = fake.sentence(10)
        gender = random.choice(genders)
        blood_status = random.choice(blood_statuses)
        born = fake.year()
        died = None if random.random() > 0.2 else fake.year()

        character = db.characters.create(
            name=name,
            description=description,
            gender=gender,
            blood_status=blood_status,
            born=born,
            died=died
        )
        char_ids.append(character.id)

        if house_ids:
            db.houses.assign_character(character.id, random.choice(house_ids))

        for _ in range(random.randint(0, 3)):
            db.spells.add_knows(character.id, random.choice(spell_ids))

        for _ in range(random.randint(0, 2)):
            db.poisons.add_brewed(character.id, random.choice(poison_ids))

    print("создание связей между персонажами...")
    rel_types = ['friend', 'enemy', 'sibling', 'teacher', 'student']
    for _ in range(num_characters):
        c1, c2 = random.sample(char_ids, 2)
        if c1 != c2:
            db.characters.add_relationship(c1, c2, random.choice(rel_types))

    print("сид завершен")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="сидирование бд")
    parser.add_argument("--characters", type=int,
                        default=10, help="количество персонажей")
    parser.add_argument("--houses", type=int, default=4,
                        help="количество факультетов")
    parser.add_argument("--spells", type=int, default=10,
                        help="количество заклинаний")
    parser.add_argument("--poisons", type=int, default=5,
                        help="количество зелий")

    args = parser.parse_args()

    faker_seed(
        num_characters=args.characters,
        num_houses=args.houses,
        num_spells=args.spells,
        num_poisons=args.poisons
    )
