### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(
    prefix="/userdb",
    tags=["userdb"], 
    responses = {404: {"message": "No encontrado"}}
)


    
user_list = []

     
@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())
    

# Path /user/1 -> return user id == 1
@router.get("/{id}")
async def user(id: str):
    return _search_user("_id", ObjectId(id))
    
# Query /userquery/?id=1 -> return user id == 1
@router.get("/query")
async def user(id: str):
    return _search_user("_id", ObjectId(id))
    

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(_search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
 
    user_dict = dict(user)
    del user_dict["id"]

    user_id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": user_id})) #MongoDB crea el campo id como '_id'

    return User(**new_user)    


@router.put("/", response_model = User, status_code = status.HTTP_202_ACCEPTED)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se ha encontrado al usuario")
    
    return _search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
        
    print(found)
    
    if found == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se ha encontrado al usuario")    


####################################################################################
#################################### functions #####################################
####################################################################################


def _search_user(field: str, key: any):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado al usuario {}".format(key)}
    

# Especific search for
#def _search_user_by_email(email: int):
#    try:
#        user = db_client.local.users.find_one({"email": email})
#        return User(**user_schema(user))
#    except Exception:
#        return {"error": "No se ha encontrado al usuario {}".format(email)}
