import pytest
from sqlmodel import Field, Session, create_engine

from sqlmodel_plus import EngineException, SQLModelPlus


def test_set_engine_by_default_scope():
    engine = create_engine("sqlite:///:memory:")
    SQLModelPlus.set_engine(engine=engine)
    assert "default" in SQLModelPlus.__engines__
    assert SQLModelPlus.__engines__["default"] == engine


def test_get_scope():
    assert SQLModelPlus._SQLModelPlus__get_scope == "default"

    class ORMTable(SQLModelPlus, table=True):
        __scope__ = "custom_scope"
        id: int = Field(primary_key=True)

    assert ORMTable._SQLModelPlus__get_scope == "custom_scope"


def test_raise_engine_exception():
    SQLModelPlus.__engines__ = {}
    with pytest.raises(EngineException):
        SQLModelPlus.find_by_id(1)
