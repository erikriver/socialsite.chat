import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import ForeignKey

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(30), unique=True, nullable=False)    

    def __init__(self, username):
        self.username = username

class Channels(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

class Logs(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    log = Column(Unicode, nullable=False)    
    user = Column(Integer, ForeignKey('user.id'))
    channel = Column(Integer, ForeignKey('channel.id'))

    def __init__(self, log, user, channel):
        self.log = log
        self.user = user
        self.channel = channel

def populate():
    session = DBSession()
    model = Channels(name=u'channel1')
    session.add(model)
    session.flush()
    transaction.commit()
    
def initialize_sql(engine):
    #DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        DBSession.rollback()
