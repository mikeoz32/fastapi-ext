from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

def get_hasher() -> PasswordHash:
    return PasswordHash([Argon2Hasher, BcryptHasher])

def hash_password(password: str) -> str:
    return get_hasher().hash(password)
