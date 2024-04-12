

from fastapi import Request, params

from fastapi_ext.session.session import SessionManager


def Session(name: str):
    async def dependant(request: Request):
        manager: SessionManager = request.state.session['manager']
        return await manager.get_session(session_name=name, request=request)

    return params.Depends(dependency=dependant, use_cache=True)
