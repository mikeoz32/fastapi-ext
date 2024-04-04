from typing import Annotated, List
from fastapi import APIRouter, Depends
from fastapi_ext.auth.schemas import CreateIdentitySchema, IdentitySchema, RegisterIdentity

from fastapi_ext.auth.services import AuthenticationService

router = APIRouter()

@router.post('/token')
async def get_auth_token():
    ...

@router.post('/register')
async def create_identity(identity: RegisterIdentity, service: Annotated[AuthenticationService, Depends()]):
    return await service.create_identity(email=identity.email, password=identity.password)

@router.post('/login')
async def login():
    ...

@router.get('/logout')
async def logout():
    ...

@router.get('/identities', response_model=List[IdentitySchema])
async def list_identities():
    ...

