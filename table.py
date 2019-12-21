from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///usersDb.db', echo=True)
Base = declarative_base()

########################################################################
class User(Base):
    """"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password

# create tables
Base.metadata.create_all(engine)