from typing import Annotated
from typing_extensions import Doc
from fastapi_ext.sqla.model import Base, CreatedUpdatedAtMixin
from sqlalchemy.orm import Mapped, mapped_column


class Account(CreatedUpdatedAtMixin, Base):
    __tablename__ = "accounts"

    identity_id: Mapped[
        Annotated[
            str,
            mapped_column(primary_key=True, nullable=False),
            Doc("""
                Id of keycloak user (external to this api identity) 
                                                                                            """),
        ]
    ]
    name: Mapped[
        Annotated[
            str,
            mapped_column(unique=True, index=True),
            Doc("""
                Profile name displayed in url, not taken from username in external id, 
                could be changed by user, must be unique
                                                                            """),
        ]
    ]
    active: Mapped[
        Annotated[
            bool,
            mapped_column(default=True),
            Doc("""
                Is account active, could be disabled by user (deleted, suspended) or by system or 
                administrators
                                                                    """),
        ]
    ]
