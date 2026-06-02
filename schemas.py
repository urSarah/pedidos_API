from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admim: Optional[bool]

    class Config:
        from_atributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_atributes = True

class OrderSchema(BaseModel):
    userId: int

    class Config:
        from_atributes = True