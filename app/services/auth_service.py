

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import jwt

from app.main import ACCESS_TOKEN_EXPIRE_MIN, ALGORITHM, SECRET_KEY, bcrypt_context
from models import User


def create_token(userId,duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)):
    date_exp = datetime.now(timezone.utc)+duracao_token
    dic_info = {"sub":str(userId),"exp":date_exp}
    encoded_jwt = jwt.encode(dic_info,SECRET_KEY,ALGORITHM)
    
    return encoded_jwt

def auth_user(email,senha,session):
    user = session.query(User).filter(User.email==email).first()

    if not user or not bcrypt_context.verify(senha,user.senha):        
        raise HTTPException(status_code=400,detail="Usuario não encontrado ou credenciais invalidas")
    
    return user

def create(user_schema,session,):
    user = auth_user(user_schema.email,user_schema.senha,session)

    if user:
        raise HTTPException(status_code=400,detail="Email ja cadastrado")
    
    senha_crypt = bcrypt_context.hash(user_schema.senha)
    new_user = User(user_schema.nome, user_schema.email, senha_crypt,user_schema.ativo,user_schema.admim)

    session.add(new_user)
    session.commit()

    return new_user