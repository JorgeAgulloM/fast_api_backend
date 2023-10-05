from fastapi import FastAPI
from pydantic import BaseModel

# Start server: from uvicorn users:app --reload
# Stop server:  ctrl+c

# Entity user
class User(BaseModel):
    name: str
    surname: str
    age: int
    url: str
    
user_list = [
    User(name = "Jorge", surname = "Agulló", age = 40, url = "https://github.com/JorgeAgulloM"),
    User(name = "Yorch", surname = "Soft", age = 1, url = "https://softyorch.com")
]


app = FastAPI()

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Jorge", "surname": "Agullo", "age": 40, "url": "https://github.com/JorgeAgulloM"},
            {"name": "Yorch", "surname": "Soft", "age": 1, "url": "https://softyorch.com"}]
    
    
@app.get("/users")
async def users():
    return user_list
    
