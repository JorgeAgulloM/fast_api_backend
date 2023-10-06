### Model User ###
from typing import Optional
from pydantic import BaseModel

# Entity user
class User(BaseModel):
    id: str = Optional[str] | None
    username: str
    email: str