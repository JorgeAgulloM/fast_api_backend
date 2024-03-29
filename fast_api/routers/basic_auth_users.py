from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Entity user
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool
    
class UserDb(User):
    password: str
    
users_db = {
    "sryorch": {
        "username": "sryorch",
        "full_name": "Jorge Agulló",
        "email": "agulloj@mail.com",
        "disable": False,
        "password": "12345678"
    },
    "mryorch": {
        "username": "mryorch",
        "full_name": "Super Yorch",
        "email": "sryorchmail@mail.com",
        "disable": True,
        "password": "87654321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDb(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación invalidas", 
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
        
    return user
    
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if form.password != user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
    