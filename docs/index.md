## Fastapi Extensions

Small library that provides utils for common cases in app development with fastapi

**Repository**: [github](https://github.com/mikeoz32/fastapi-ext)

---

Some features

* **SQLAlchemy** helpers for SQLAlchemy
* **Sessions** session manager
* **Authentication** Identity management and authentication

---

## Requirements

Python 3.9+

---

## Installation

```console
$ pip install fapi-ext
```

---

## Example

* Create regular FastAPI application

```Python
from fastapi import FastAPI

app = FastAPI()
```

To add sqlalchemy support install SQLAlchemy and add it to lifespan. First define lifespan function.


```Python
from fastapi-ext.sqla.lifespan import sqla_init, sqla_dispose

async def lifespan(app: FastAPI):
    sqla_lifespan = await sqla_init(app)

    yield {
        "sqla": sqla_lifespan
    }

    await sqla_dispose(sqla_lifespan)

```
* Note: key in yielded dict MUST be `sqla` for sqlalchemy

Now you could create models and repositories

```Python
from fastapi-ext.sqla.model import Base, IDMixin, CreatedUpdatedAtMixin

class Post(IDMixin, CreatedUpdatedAtMixin, Base):
    title: Mapped[str]
    text: Mapped[str]

```
