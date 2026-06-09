from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services.auth_service import auth_user, create, create_token
from models import User
from app.dependencies import pegar_session, verify_token
from schemas import LoginSchema, UserSchema
from datetime import timedelta
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/list")
async def list_user(session: Session = Depends(pegar_session)):
    user = session.query(User).all()
    return{"user":user}

@auth_router.post("/create_user")
async def create_user(user_schema: UserSchema,session: Session = Depends(pegar_session)):    
    new_user = create(user_schema,session)
    return {"Mensagem": f"Email {new_user.email} cadastrado"}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_session)):
    user = auth_user(login_schema.email,login_schema.senha,session)
    
    access_token = create_token(user.id)
    refresh_token = create_token(user.id,duracao_token=timedelta(days=7))
    return{"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"}

@auth_router.post("/login_form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_session)):
    user = auth_user(dados_formulario.username,dados_formulario.password,session)
    
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