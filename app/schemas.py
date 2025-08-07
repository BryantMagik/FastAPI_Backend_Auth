from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal
from uuid import UUID

class LoginData(BaseModel):
    username: str
    password: str
    
class RegisterData(BaseModel):
    name: str
    username: str
    password: str