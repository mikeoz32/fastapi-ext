# Session 

Sessions are identified by session_id

Session data could be json or signed json (as JWS/JWT)

one app could have multiple session objects with separate cookies

```python
class LoginSession(BaseModel):
    code: Optional[UUID] = None
    
login_session = Session[LoginSession](name="login_session", auto_create=True, model=LoginSession)

@app.get('/')
async def session_info(session: Annotated[Session, Depends(login_session)]):
    assert session.initialized()
    assert session.session_id() is not None
    assert session.data.code is None
```

this will automatically create session cookie and empty session object in session storage

# Storages 

## InMemory

## Memcached

## Redis

## Sqlalchemy
