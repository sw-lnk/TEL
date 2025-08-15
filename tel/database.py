from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    return Session(engine)

def init_database() -> None:
    SQLModel.metadata.create_all(bind=engine)