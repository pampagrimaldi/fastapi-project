from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# this file contains all the tables that we want to create in the database
# note classes are uppercase, and extend Base
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE',
                       nullable=False,  default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("now()"))


