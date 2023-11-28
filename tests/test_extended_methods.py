import pytest
from sqlmodel import Field, Session, create_engine, text

from sqlmodel_plus import SQLModelPlus

SQLModelPlus.set_engine(create_engine("sqlite:///:memory:"))


class Hero(SQLModelPlus, table=True):
    __tablename__ = "hero"
    id: int = Field(primary_key=True)
    name: str


SQLModelPlus.create_tables()


def test_session():
    assert isinstance(Hero.Session, Session)
    with Hero.Session as session:
        assert session.exec(text("SELECT 1")).first() == (1,)


def test_save():
    assert Hero(id=1, name="hero_1").save() == Hero(id=1, name="hero_1")
    hero = Hero.find_by_id(1)
    assert hero == Hero(id=1, name="hero_1")
    hero.name = "hero_2"
    assert hero.save() == Hero(id=1, name="hero_2")
    assert Hero.find_by_id(1) == Hero(id=1, name="hero_2")


def test_create():
    assert Hero(id=2, name="hero_1").create() == Hero(id=2, name="hero_1")
    assert Hero.find_by_id(2) == Hero(id=2, name="hero_1")


def test_update():
    assert Hero(id=3, name="hero_3").save() == Hero(id=3, name="hero_3")
    hero = Hero.find_by_id(3)
    assert hero == Hero(id=3, name="hero_3")
    hero.name = "hero_4"
    assert hero.update() == Hero(id=3, name="hero_4")
    assert Hero.find_by_id(3) == Hero(id=3, name="hero_4")


def test_find_by_id():
    hero = Hero(id=4, name="hero_5").save()
    assert Hero.find_by_id(4) == hero
    assert Hero.find_by_id(10) is None


def test_delete():
    hero_1 = Hero(id=1, name="hero_1").save()
    assert Hero.find_by_id(1) == hero_1
    assert hero_1.delete() == hero_1
    assert Hero.find_by_id(1) is None


def test_query():
    hero_1 = Hero(id=1, name="hero_1").save()
    hero_2 = Hero(id=2, name="hero_2").save()

    query = Hero.query(Hero.select.where(Hero.id.in_([1, 2])).order_by(Hero.id))
    assert query.first == hero_1
    assert query.all == [hero_1, hero_2]

    query = Hero.query("SELECT id FROM hero WHERE id = :id", {"id": 1})
    assert query.first == (1,)
    assert query.all == [(1,)]
