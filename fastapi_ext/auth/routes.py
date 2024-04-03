from typing import Annotated, List
from fastapi import APIRouter, Depends
from fastapi_ext.auth.schemas import CreateIdentitySchema, IdentitySchema

from fastapi_ext.auth.services import AuthenticationService

router = APIRouter()

@router.post('/token')
async def get_auth_token():
    ...

@router.post('/register')
async def create_identity(identity: CreateIdentitySchema, service: Annotated[AuthenticationService, Depends()]):
    return await service.create_identity()

@router.post('/login')
async def login():
    ...

@router.get('/logout')
async def logout():
    ...

@router.get('/identities', response_model=List[IdentitySchema])
async def list_identities():
    ...

