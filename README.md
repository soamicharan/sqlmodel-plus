# SQLModel Plus

[![GitHub license badge](https://raw.githubusercontent.com/soamicharan/sqlmodel-plus/main/badges/badge-license.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![Coverage](https://raw.githubusercontent.com/soamicharan/sqlmodel-plus/main/badges/coverage.svg)]()
[![pypi](https://img.shields.io/pypi/v/sqlmodel-plus.svg)](https://pypi.python.org/pypi/sqlmodel-plus)

## Installation

Install package using pip -> `pip install sqlmodel-plus`

## Usage

Use `SQLModelPlus` class to define data models and tables as it inherits `SQLModel`. \
To use in-built functions, an engine needs to set using `set_engine` method.

```python
from sqlmodel_plus import SQLModelPlus, EngineException
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

class Hero(SQLModelPlus, table=True):
    __tablename__ = "hero"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

SQLModelPlus.set_engine(create_engine(f"sqlite:///database.db"))
```

If engine is not set it will raise `EngineException`

By using `SQLModelPlus` class, it provide following classmethods available to all inherited classes -

#### find_by_id

```python
Hero.find_by_id(1)
Hero.find_by_id("uuid")
Hero.find_by_id((1, 2,))
Hero.find_by_id({"id": 1, "version": 3})
```

#### save

Create or Update Record in database.
```python
hero = Hero(id=1, name="hero_1", secret_name="Secret_hero").save()
hero.name = "hero_2"
hero.save()

```

#### create

Create new record in database.
```python
Hero(id=1, name="hero_1", secret_name="Secret_hero").create()
```

#### update

Update record in database.
```python
hero = Hero(id=1, name="hero_1", secret_name="Secret_hero")
hero.name = "hero_2"
hero.update()
```

#### delete

Delete record from database
```python
hero = Hero(id=1, name="hero_1", secret_name="Secret_hero").save()
hero.delete()
```

#### select

```python
statement = Hero.select  # This is equivalant to select(Hero)
statement.where(Hero.id == 1)
```

#### query

```python
statement = Hero.select.where(Hero.id == 1)
Hero.query(statement).all
Hero.query("SELECT id FROM hero").first
```

#### Session

```python
session = Hero.Session # Return Session object
session.exec(Hero.select).all()

with Hero.Session as session:
    session.exec(Hero.select.where(Hero.id == 1)).first()
```

#### create_tables

Create tables in database. \
It is equivalant of `SQLModel.metadata.create_all` method where you don't need to provide bind parameter.
```python
SQLModelPlus.create_tables()
```

## Handle multiple database

If you have multiple databases ORM models, then you use `__scope__` class attribute to define database scopes. \
Set `__scope__` variable to any unique identifier string to identify databases.

```python
from sqlalchemy.orm import registry
from sqlmodel_plus import SQLModelPlus
from typing import Optional
from sqlmodel import Field
class DatabaseA(SQLModelPlus, registry=registry()):
    __scope__ = "db1"

class DatabaseB(SQLModelPlus, registry=registry()):
    __scope__ = "db2"

DatabaseA.set_engine(create_engine(f"sqlite:///database_A.db"))

DatabaseB.set_engine(create_engine(f"sqlite:///database_B.db"))

# This uses DatabaseA as base ORM model and interacts with database_A
class TableA(DatabaseA, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# This uses DatabaseB as base ORM model and interacts with database_B
class TableB(DatabaseB, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
```
