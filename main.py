from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Jujutsu Kaisen Character Manager")
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jujutsu-caracter-comparison.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class caracter(BaseModel):
    HP :int
    name : str
    type : str
    attack : int 
    defence : int 
    image_url: str
caracters=[caracter(HP=3000,name="Gojo",type="sorcer",attack=5000,defence=4000,image_url="https://pinkcrow.net/wp-content/uploads/2025/09/Satoru_Gojo_arrives_on_the_battlefield_29-1.jpg")]
@app.get("/caracters/")
def readcaracters():
    return caracters
@app.post("/caracters/")
def createcaracter(new_caracter : caracter):
    caracters.append(new_caracter)
    return caracters
@app.put("/caracters/{caracter_name}")
def caracter_comparison( caracter_name:str):
    attac=0
    for caracter in caracters:
        if caracter.name==caracter_name:
            attac=caracter.attack
    for caracter in caracters:
        if caracter.attack>attac:
            return f"ops {caracter_name} is not the stronger in your liste:("
    return f"hoho {caracter_name} is the stronger in your liste :)"
@app.delete("/caracters/{caracter_name}")
def remove_caracter(caracter_name :str):
    for index ,caracter in enumerate(caracters):
        if caracter.name==caracter_name:
            del caracters[index]
            return f"caracter deleted"
    return f"caracter not found"
@app.get("/")
async def serve_home():
    return FileResponse('index.html')






