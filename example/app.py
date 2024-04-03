from typing import Any, Dict, List, cast
from pydantic import BaseModel, Field, create_model
from sqlalchemy import inspect
from sqlalchemy.orm import Mapper
from sqlalchemy.sql.schema import CallableColumnDefault
from example.models.users import User
from fastapi_ext.app import create_app
from fastapi_ext.sqla.model import M

app = create_app()


class ApiResourceAttribute(BaseModel):
    name: str
    attribute_type: str


class ApiResource(BaseModel):
    name: str
    attributes: Dict[str, ApiResourceAttribute]


def describe_model(model: type[M]):
    m: Mapper = inspect(model)
    attributes = dict()
    for column in m.columns:
        attributes[column.name] = ApiResourceAttribute(
            name=column.name, attribute_type=str(column.type.python_type)
        )
    resource = ApiResource(name=str(m.class_.__name__), attributes=attributes)
    print(resource)


def model_to_schema(model: type[M]) -> BaseModel:
    fields: Dict[str, Any] = dict()
    m:Mapper = inspect(model)

    for column in m.columns:
        python_type = column.type.python_type
        default = column.default
        field_args = dict()
        if isinstance(default, CallableColumnDefault):
            field_args['default_factory'] = default.arg
        elif default:
            field_args['default'] = default
        field_info = Field(**field_args)
        fields[column.name] = (python_type, field_info)
    return create_model(str(m.class_.__name__) + "Schema", **fields)


print(model_to_schema(User).schema_json())

@app.get("/info", response_model=model_to_schema(User))
async def get_service_info():
    return model_to_schema(User).schema_json()
