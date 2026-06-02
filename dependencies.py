from models import db
from sqlalchemy.orm import sessionmaker

def pegar_session():
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        yield session
    finally:
        session.close()