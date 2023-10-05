from fastapi import FastAPI
from pydantic import BaseModel

# Start server: from uvicorn users:app --reload
# Stop server:  ctrl+c

# Entity user
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    url: str
    
user_list = [
    User(id = 0, name = "Jorge", surname = "Agulló", age = 40, url = "https://github.com/JorgeAgulloM"),
    User(id = 1, name = "Yorch", surname = "Soft", age = 1, url = "https://softyorch.com")
]


app = FastAPI()

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Jorge", "surname": "Agullo", "age": 40, "url": "https://github.com/JorgeAgulloM"},
            {"name": "Yorch", "surname": "Soft", "age": 1, "url": "https://softyorch.com"}]
     
@app.get("/users")
async def users():
    return user_list
    
@app.get("/user/{id}")
async def user(id: int):
    user = filter(lambda user: user.id == id, user_list)
    try:
        return list(user)[0]
    except Exception:
        return {"error": "No se ha encontrado al usuario {}".format(id)}

    
    
