from fastapi_ext.sqla.model import IDMixin, CreatedUpdatedAtMixin, Base


class User(IDMixin, CreatedUpdatedAtMixin, Base):
    __tablename__ = "users"
