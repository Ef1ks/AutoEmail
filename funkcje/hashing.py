from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

# funkcja hashujaca haslo

def check_password(*,password: str,hashed_password):
    return pwd_context.verify(password, hashed_password)