from neomodel import StructuredNode, StringProperty, RelationshipTo, config, db
import os
from dotenv import load_dotenv


# загружаем переменные окружения
load_dotenv()

config.DATABASE_URL = os.getenv("DATABASE_URL")


class Hero(StructuredNode):
    name = StringProperty()
    house = StringProperty()
    friends = RelationshipTo('Hero', 'FRIENDS_WITH')


def clear_data():
    db.cypher_query("MATCH (n:Hero) DETACH DELETE n")


def create_data():
    clear_data()

    harry = Hero(name='Harry Potter', house='Gryffindor').save()
    hermione = Hero(name='Hermione Granger', house='Gryffindor').save()

    # взаимосвязь между героями
    harry.friends.connect(hermione)


def read_data():
    heroes = Hero.nodes.all()
    for hero in heroes:
        print(f"Hero: {hero.name} | House: {hero.house}")


if __name__ == "__main__":
    create_data()
    read_data()
