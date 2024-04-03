from typing import Annotated, Any, Dict, Optional
from typing_extensions import Doc
from pydantic import BaseModel, Field, create_model
from sqlalchemy import inspect
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.schema import CallableColumnDefault, ScalarElementColumnDefault

from fastapi_ext.sqla.model import M


def model_to_schema(
    model: type[M],
    *,
    include_primary: Annotated[
        bool, Doc("If false will exclude primary key field from schema")
    ] = True,
    all_optional: Annotated[bool, Doc("If true all fields will be optional")] = False,
    postfix: Annotated[str, Doc("Will be added in model name before Schema")] = "",
) -> BaseModel:
    fields: Dict[str, Any] = dict()
    m: Mapped = inspect(model)

    for column in m.columns:
        if include_primary is False:
            if column.primary_key:
                continue
        python_type = column.type.python_type
        default = column.default
        field_args = dict()
        if isinstance(default, CallableColumnDefault):
            field_args["default_factory"] = default.arg
        elif isinstance(default, ScalarElementColumnDefault):
            default = default.arg
        elif default:
            field_args["default"] = default
        field_info = Field(**field_args)
        if default is None or all_optional is True:
            python_type = Optional[python_type]
        fields[column.name] = (python_type, field_info)
    return create_model(str(m.class_.__name__) + postfix + "Schema", **fields)


class AutoSchemaMixin:
    @classmethod
    def schema(cls):
        return model_to_schema(cls)

    @classmethod
    def create_model_schema(cls):
        return model_to_schema(cls, include_primary=False, postfix="Create")

    @classmethod
    def update_model_schema(cls):
        return model_to_schema(
            cls, include_primary=False, all_optional=True, postfix="Update"
        )

    @classmethod
    def base_schema(cls):
        return model_to_schema(cls)
