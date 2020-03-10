from sqlalchemy import create_engine, Column, Integer, String, UnicodeText, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import datetime

engine = create_engine('sqlite:///dips1.db', connect_args={'check_same_thread': False})

Base = declarative_base()

class UserData(Base):
    __tablename__ = 'userdata'
    id = Column(Integer, primary_key=True)
    email = Column(String(40), unique=True, nullable=False)
    password = Column(String(40), nullable=False)
    realname = Column(String(40), nullable=False)
    token = Column(String(36), nullable=False)
    creation = Column(String(30), nullable=False)
    lastlogin = Column(String(30), nullable=False)

Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base.metadata.create_all(engine)
session.commit()

def CreateAccount(User):
    newtoken = str(uuid.uuid4())
    insertUser = UserData(email = User.email, password = User.password, realname = User.realname, token = newtoken, creation = str(datetime.datetime.now()), lastlogin = str(datetime.datetime.now()))
    session.add(insertUser)
    session.commit()
    session.close()
    return newtoken

def CheckIfAccountExists(email):
    isItUnique = session.query(UserData).filter_by(email = email).first()
    if str(isItUnique) == 'None':
        return False
    else:
        return True

def CredentialsGood(User):
    credentials = session.query(UserData).filter_by(email = User.email).filter_by(password = User.password).first()
    if str(credentials) == 'None':
        return False
    else:
        return True