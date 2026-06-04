from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MIN"))
app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)


#para rodar o codigo 
#uvicorn main:app --reload
