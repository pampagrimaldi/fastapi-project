from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# set up database url
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/fastapi"
# set engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# define base class
Base = declarative_base()


# dependency to get database session
# this is responsible to talk to the database
# it will create a session every time a request is made and then close it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
