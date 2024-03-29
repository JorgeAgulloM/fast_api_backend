from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"], 
    responses = {404: {"message": "No encontrado"}}
)

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

@router.get("/json")
async def usersjson():
    return [{"name": "Jorge", "surname": "Agullo", "age": 40, "url": "https://github.com/JorgeAgulloM"},
            {"name": "Yorch", "surname": "Soft", "age": 1, "url": "https://softyorch.com"}]
     
@router.get("/")
async def users():
    return user_list
    
# Path /user/1 -> return user id == 1
@router.get("/{id}")
async def user(id: int):
    return _search_user(id)
    
# Query /userquery/?id=1 -> return user id == 1
@router.get("/query")
async def user(id: int):
    return _search_user(id)
    
@router.post("/", response_model = User, status_code = 201)
async def user(user: User):
    if type(_search_user(user.id)) == User:
        raise HTTPException(409, detail="El usuario ya existe")
    user_list.append(user)
    return user    

@router.put("/", response_model = User, status_code = 201)
async def user(user: User):
    for idx, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[idx] = user
            return user
    raise HTTPException(404, detail="No se ha encontrado al usuario")

@router.delete("/{id}", status_code = 202)
async def delete(id: int):
    for idx, user in enumerate(user_list):
        if user.id == id:
            del user_list[idx]
            return {"message": "Usuario eliminado"}
    raise HTTPException(404, detail="No se ha encontrado al usuario")

#####################
##### functions #####
#####################

def _search_user(id: int):
    user = filter(lambda user: user.id == id, user_list)
    try:
        return list(user)[0]
    except Exception:
        return {"error": "No se ha encontrado al usuario {}".format(id)}

