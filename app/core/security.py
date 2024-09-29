from passlib.context import CryptContext


CRYPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, password_hash: str) -> bool:
    return CRYPTO.verify(password, password_hash)

def generate_password_hash(password: str) -> str:
    return CRYPTO.hash(password)