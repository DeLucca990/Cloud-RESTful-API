from fastapi import FastAPI, Depends, HTTPException, Query #type: ignore
from pydantic import BaseModel
from sqlalchemy.orm import Session #type: ignore
from sqlalchemy import Column, Integer, String, create_engine #type: ignore
from sqlalchemy.ext.declarative import declarative_base #type: ignore
from sqlalchemy.orm import sessionmaker #type: ignore
import requests
import random
from dotenv import load_dotenv
import os
from utils import get_password_hash, verify_password, create_access_token, get_current_user, load_countries, load_names

load_dotenv()

# Conexão com o banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo do banco de dados
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Criação das tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Projeto1 - Cloud",
    description="API para autenticação de usuários e consulta de API externa utilizando Docker",
    version="0.1",
    docs_url="/",
)

# Models para validação
class UserCreate(BaseModel):
    nome: str
    email: str
    senha: str
class UserLogin(BaseModel):
    email: str
    senha: str
class Token(BaseModel):
    jwt: str

# Dependência para obter sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.post("/registrar", response_model=Token, tags=["Registrar Usuários"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    hashed_password=get_password_hash(user.senha)
    new_user = User(nome=user.nome, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    acces_token = create_access_token(data={"sub": new_user.email})
    return {"jwt": acces_token}

@app.post("/login", response_model=Token, tags=["Login Usuários"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Email não encontrado")
    if not verify_password(user.senha, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    acces_token = create_access_token(data={"sub": db_user.email})
    return {"jwt": acces_token}

@app.get("/consultar", tags=["Consultar API Externa"])
def consultar(
    name: str = Query(None, description="Nome para pesquisa na API"), 
    current_user: str = Depends(get_current_user)):

    names = load_names("./data/names.txt")
    if name is None:
        name = random.choice(names)
    
    response = requests.get(f"https://api.nationalize.io", params={"name": name})
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao consultar a API externa")
    else:
        data = response.json()
        country_mapping = load_countries("./data/countries.csv")
        for country in data['country']:
            country_id = country['country_id']
            country['country_id'] = country_mapping.get(country_id, country_id)
        return data