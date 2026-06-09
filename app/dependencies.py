from fastapi import Depends, HTTPException
from jose import JWTError, jwt

from app.main import ALGORITHM, SECRET_KEY,oauth2_schema
from models import User, db
from sqlalchemy.orm import Session, sessionmaker

def pegar_session():
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        yield session
    finally:
        session.close()

def verify_token(token: str = Depends(oauth2_schema),session: Session = Depends(pegar_session)):
    try:
        dic_info = jwt.decode(token,SECRET_KEY,ALGORITHM)
        id_user = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401,detail="Acesso Negado! Verifique a validade do token")
    # verificar se token é valido
    # extrair o ID do usuario do token
    user = session.query(User).filter(User.id == id_user).first()
    
    if not user:
        raise HTTPException(status_code=401,detail="Acesso Invalido")
    
    return user