
from pydantic import BaseModel, EmailStr, Field
from fastapi_ext.auth.models import Identity


IdentitySchema = Identity.schema()
CreateIdentitySchema = Identity.create_model_schema()
UpdateIdentitySchema = Identity.update_model_schema()

class RegisterIdentity(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
