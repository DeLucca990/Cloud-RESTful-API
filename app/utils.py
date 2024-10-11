from passlib.context import CryptContext # type: ignore
import jwt # type: ignore
from fastapi import Header, HTTPException, Depends # type: ignore
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials #type: ignore
from datetime import datetime, timedelta
import pandas as pd

SECRET_KEY = "b4e7b3b1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Criptografia para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Autenticação com Bearer Token (JWT) no header
bearer_scheme = HTTPBearer()

# Funções auxiliares
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_code = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_code.update({"exp": expire})
    encoded_jwt = jwt.encode(to_code, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Email ou senha inválidas")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido, tente um novo login")

# Função para transformar siglas de países em nomes completos
def load_countries(file):
    df = pd.read_csv(file)
    return dict(zip(df['Code'], df['Name']))