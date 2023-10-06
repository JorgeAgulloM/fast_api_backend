### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema
from db.client import db_client

router = APIRouter(
    prefix="/userdb",
    tags=["userdb"], 
    responses = {404: {"message": "No encontrado"}}
)


    
user_list = []

     
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
    

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
 
    user_dict = dict(user)
    del user_dict["id"]

    user_id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id": user_id})) #MongoDB crea el campo id como '_id'

    return User(**new_user)    


@router.put("/", response_model = User, status_code = status.HTTP_201_CREATED)
async def user(user: User):
    for idx, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[idx] = user
            return user
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se ha encontrado al usuario")


@router.delete("/{id}", status_code = status.HTTP_202_ACCEPTED)
async def delete(id: int):
    for idx, user in enumerate(user_list):
        if user.id == id:
            del user_list[idx]
            return {"message": "Usuario eliminado"}
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se ha encontrado al usuario")


####################################################################################
#################################### functions #####################################
####################################################################################

def _search_user(id: int):
    user = filter(lambda user: user.id == id, user_list)
    try:
        return list(user)[0]
    except Exception:
        return {"error": "No se ha encontrado al usuario {}".format(id)}

