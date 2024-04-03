from typing import Annotated
from fastapi import APIRouter, Depends

from fastapi_ext.auth.services import AuthenticationService

router = APIRouter()

@router.post('/token')
async def get_auth_token():
    ...

@router.post('/register')
async def create_identity(service: Annotated[AuthenticationService, Depends()]):
    return await service.create_identity()

@router.post('/login')
async def login():
    ...

@router.get('/logout')
async def logout():
    ...
