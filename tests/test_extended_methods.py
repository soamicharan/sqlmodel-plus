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
    assert (
        Hero(id=1, name="hero_1").save().model_dump()
        == Hero(id=1, name="hero_1").model_dump()
    )
    hero = Hero.find_by_id(1)
    assert hero.model_dump() == Hero(id=1, name="hero_1").model_dump()
    hero.name = "hero_2"
    assert hero.save().model_dump() == Hero(id=1, name="hero_2").model_dump()
    assert Hero.find_by_id(1).model_dump() == Hero(id=1, name="hero_2").model_dump()


def test_create():
    assert (
        Hero(id=2, name="hero_1").create().model_dump()
        == Hero(id=2, name="hero_1").model_dump()
    )
    assert Hero.find_by_id(2).model_dump() == Hero(id=2, name="hero_1").model_dump()


def test_update():
    assert (
        Hero(id=3, name="hero_3").save().model_dump()
        == Hero(id=3, name="hero_3").model_dump()
    )
    hero = Hero.find_by_id(3)
    assert hero.model_dump() == Hero(id=3, name="hero_3").model_dump()
    hero.name = "hero_4"
    assert hero.update().model_dump() == Hero(id=3, name="hero_4").model_dump()
    assert Hero.find_by_id(3).model_dump() == Hero(id=3, name="hero_4").model_dump()


def test_find_by_id():
    hero = Hero(id=4, name="hero_5").save()
    assert Hero.find_by_id(4).model_dump() == hero.model_dump()
    assert Hero.find_by_id(10) is None


def test_delete():
    hero_1 = Hero(id=1, name="hero_1").save()
    assert Hero.find_by_id(1).model_dump() == hero_1.model_dump()
    assert hero_1.delete().model_dump() == hero_1.model_dump()
    assert Hero.find_by_id(1) is None


def test_query():
    hero_1 = Hero(id=1, name="hero_1").save()
    hero_2 = Hero(id=2, name="hero_2").save()

    query = Hero.query(Hero.select.where(Hero.id.in_([1, 2])).order_by(Hero.id))
    assert query.first.model_dump() == hero_1.model_dump()
    assert [row.model_dump() for row in query.all] == [
        hero_1.model_dump(),
        hero_2.model_dump(),
    ]

    query = Hero.query("SELECT id FROM hero WHERE id = :id", {"id": 1})
    assert query.first == (1,)
    assert query.all == [(1,)]
