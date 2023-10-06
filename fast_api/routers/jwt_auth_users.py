from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM ="HS256"
ACCES_TOKEN_DURATION = 1
SECRET = "075bcee72a66899888d94248ea24ba44f821eb8a1452ce44c3679b3687bc796c"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes="bcrypt")


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
        "password": "$2a$12$J3iaijL3xlMukrevlbxII.B0bh3ZKaq9LxzplTIlpxelchJc0HQs2"
    },
    "mryorch": {
        "username": "mryorch",
        "full_name": "Super Yorch",
        "email": "sryorchmail@mail.com",
        "disable": True,
        "password": "$2a$12$o5J71pAFYO1Sk1zf1teB3eDP/NDt5Gx9ZZsjPHxpF5tXYi0g4IP0y"
    }
} 


def search_user_db(username: str):
    if username in users_db:
        return UserDb(**users_db[username])
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación invalidas", 
            headers={"WWW-Authenticate": "Bearer"}
        ) 

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
         raise exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):    
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
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)

    access_token = jwt.encode(
        {"sub":user.username, "exp":expire}, 
        SECRET, 
        algorithm=ALGORITHM
    )

    return {"access_token":access_token, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
