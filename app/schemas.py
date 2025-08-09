from pydantic import BaseModel
from datetime import date
from uuid import UUID

class LoginData(BaseModel):
    username: str
    password: str
    
class RegisterData(BaseModel):
    name: str
    username: str
    password: str
    
class SalesData(BaseModel):
    date: date
    cubos: int
    escamas: int
    pilet: int
    euros: float
    
    