from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    userID: str
    user_passwd: str
    user_type: Optional[str]


class User2(BaseModel):
    userID: str
    user_passwd: str