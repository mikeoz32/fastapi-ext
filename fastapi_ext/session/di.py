

from fastapi import Request, params

from fastapi_ext.session.session import SessionManager
from fastapi_ext.auth.settings import auth_settings


def Session(name: str):
    async def dependant(request: Request):
        manager: SessionManager = request.state.session['manager']
        return await manager.get_session(session_name=name, request=request)

    return params.Depends(dependency=dependant, use_cache=True)

def AuthSession():
    name = auth_settings.auth_session_name
    return Session(name=name)
