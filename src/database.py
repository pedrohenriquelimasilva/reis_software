from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.settings import Settings


engine = create_engine(
    Settings().DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=40,
    pool_timeout=30,
    pool_recycle=1800 
)

SessionLocal = sessionmaker(bind=engine)

def get_session():
    """
    Retorna uma sessão do SQLAlchemy para uso no FastAPI.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
