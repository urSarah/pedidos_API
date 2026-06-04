from os import access

from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import User
from dependencies import pegar_session, verify_token
from main import SECRET_KEY, bcrypt_context,ALGORITHM,ACCESS_TOKEN_EXPIRE_MIN
from schemas import LoginSchema, UserSchema
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(userId,duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)):
    date_exp = datetime.now(timezone.utc)+duracao_token
    dic_info = {"sub":str(userId),"exp":date_exp}
    encoded_jwt = jwt.encode(dic_info,SECRET_KEY,ALGORITHM)
    
    return encoded_jwt

def auth_user(email,senha,session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(senha,user.senha):
        return False
    
    return user

@auth_router.get("/")
async def home():
    """
    Essa rota precisa ta autenticado
    """
    return{"mensagem":"rota de auth","autenticado":False}

@auth_router.post("/create_user")
async def create_user(user_schema: UserSchema,session: Session = Depends(pegar_session)):    
    user = session.query(User).filter(User.email == user_schema.email).first()

    if user:
        raise HTTPException(status_code=400,detail="Email ja cadastrado")
    else:
        senha_crypt = bcrypt_context.hash(user_schema.senha)
        new_user = User(user_schema.nome, user_schema.email, senha_crypt,user_schema.ativo,user_schema.admim)
        session.add(new_user)
        session.commit()
        return {"Mensagem": f"Email {user_schema.email} cadastrado"}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_session)):
    user = auth_user(login_schema.email,login_schema.senha,session)

    if not user:
        raise HTTPException(status_code=400,detail="Usuario não encontrado ou credenciais invalidas")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id,duracao_token=timedelta(days=7))
        return{"access_token": access_token,
               "refresh_token": refresh_token,
               "token_type": "Bearer"}

@auth_router.post("/login_form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_session)):
    user = auth_user(dados_formulario.username,dados_formulario.password,session)

    if not user:
        raise HTTPException(status_code=400,detail="Usuario não encontrado ou credenciais invalidas")
    else:
        access_token = create_token(user.id)
        return{"access_token": access_token,
               "token_type": "Bearer"}

@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(verify_token)):
    # user = verify_token(token)
    # verificar o token
    access_token = create_token(user.id)
    return{"access_token": access_token,
           "token_type": "Bearer"}