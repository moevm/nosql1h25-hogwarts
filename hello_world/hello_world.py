from neomodel import StructuredNode, StringProperty, RelationshipTo, config, db
import os
from dotenv import load_dotenv
import time


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


def wait_for_db():
    retries = 10
    delay = 5  # задержка между попытками в секундах

    for attempt in range(retries):
        try:
            # пытаемся выполнить простой запрос к базе данных
            db.cypher_query("RETURN 1")
            return True
        except Exception as e:
            time.sleep(delay)

    return False


if __name__ == "__main__":
    wait_for_db()
    create_data()
    read_data()
