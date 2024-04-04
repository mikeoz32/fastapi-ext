from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

def get_hasher() -> PasswordHash:
    return PasswordHash([Argon2Hasher(), BcryptHasher()])

def hash_password(password: str) -> str:
    print(password)
    return get_hasher().hash(password)

def verify_password(password:str, hash: str) -> bool:
    return get_hasher().verify(password=password, hash=hash)
