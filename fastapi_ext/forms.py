from typing import List
from fastapi import Request
from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails


class FormValidationException(Exception):
    def __init__(self, errors: List[ErrorDetails]) -> None:
        self.errors = error_details_to_dict(errors)

def error_details_to_dict(errors: List[ErrorDetails]) -> dict:
    error_dict = dict()
    for error in errors:
        location = error.get("loc")
        message = error.get("msg")
        error_dict[location[0]] = message
    return error_dict


class FormBase(BaseModel):
    _errors: dict = None

    def is_valid(self):
        return self._errors is None

    def errors(self, field: str = None):
        errors = self._errors or {}
        if field:
            return errors.get(field)
        return errors

    def set_errors(self, errors):
        self._errors = errors


    @classmethod
    async def validate_request(cls, request: Request):
        form = await request.form()
        model = None
        try: 
            model = cls(**form)
        except ValidationError as e:
            model = cls.model_construct(**form)
            model.set_errors(error_details_to_dict(e.errors()))
        return model
