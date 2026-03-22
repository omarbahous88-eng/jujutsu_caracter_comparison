from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# --- CONFIGURATION BASE DE DONNÉES ---
# Remplace XXXXX par ton vrai lien (ex: mysql+pymysql://user:pass@host/db)
DATABASE_URL = "mysql+pymysql://3LpbZJwNF2CTBD7.root:J43PUXtxIIAK7eVf@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/jujutsukaisen?ssl_ca=/etc/ssl/certs/ca-certificates.crt"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle de la Table SQL
class CharacterModel(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    type = Column(String(50))
    HP = Column(Integer)
    attack = Column(Integer)
    defence = Column(Integer)
    image_url = Column(Text)

# Création de la table au démarrage
Base.metadata.create_all(bind=engine)

# --- CONFIGURATION API ---
app = FastAPI(title="JJK Manager avec TiDB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle Pydantic pour la validation des données entrantes
class CaracterSchema(BaseModel):
    name: str
    type: str
    HP: int
    attack: int
    defence: int
    image_url: str

    class Config:
        from_attributes = True

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROUTES ---

@app.get("/")
async def serve_home():
    # Assure-toi que le nom du fichier HTML sur GitHub est bien index.html
    return FileResponse('index.html')

@app.get("/caracters/")
def read_caracters(db: Session = Depends(get_db)):
    return db.query(CharacterModel).all()

@app.post("/caracters/")
def create_caracter(obj: CaracterSchema, db: Session = Depends(get_db)):
    new_c = CharacterModel(**obj.dict())
    db.add(new_c)
    db.commit()
    db.refresh(new_c)
    return new_c

@app.put("/caracters/{name}")
def compare_caracter(name: str, db: Session = Depends(get_db)):
    target = db.query(CharacterModel).filter(CharacterModel.name == name).first()
    if not target:
        return "Personnage non trouvé"
    
    max_atk = db.query(CharacterModel).order_by(CharacterModel.attack.desc()).first()
    
    if target.attack >= max_atk.attack:
        return f"hoho {name} est le plus fort de ta liste ! ⛩"
    else:
        return f"ops {name} n'est pas le plus fort... {max_atk.name} le dépasse."

@app.delete("/caracters/{name}")
def delete_caracter(name: str, db: Session = Depends(get_db)):
    target = db.query(CharacterModel).filter(CharacterModel.name == name).first()
    if target:
        db.delete(target)
        db.commit()
        return "Supprimé avec succès"
    return "Non trouvé"





