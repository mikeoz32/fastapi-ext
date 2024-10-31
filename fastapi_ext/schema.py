
from typing import Generic, List, TypeVar
from pydantic import BaseModel

RT = TypeVar("SchemaType", bound=BaseModel)

class ApiResponse(Generic[RT], BaseModel):
    schema_type: str
    data: List[RT] | RT
