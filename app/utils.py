from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def pwd_hash(password):
    hash_password = pwd_context.hash(password)
    return hash_password


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
