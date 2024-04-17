from typing import Optional
from fastapi import HTTPException, Request, status
from fastapi.security.base import SecurityBase

from fastapi_ext.auth.settings import auth_settings

class HTTPSession(SecurityBase):

    def __init__(self, 
                 *, 
                 redirect_to_login: Optional[bool] = None,
                 login_route: Optional[str] = None
    ) -> None:
        self._redirect_to_login = redirect_to_login or False
        self._login_route = login_route

    async def __call__(self, request: Request):
        name = auth_settings.auth_session_name

        manager: SessionManager = request.state.session['manager']
        session: Dict = await manager.get_session(session_name=name, request=request)
        
        identity_id = session.get('identity_id')

        if not identity_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        return identity_id
