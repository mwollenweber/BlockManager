'''
database.py

Copyright Matthew Wollenweber 2015
mjw@insomniac.technology

'''

import config

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker


SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI

 
engine = create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
db_session._model_changes = {}

Base = declarative_base()
Base.query = db_session.query_property()


def get_session():
    return db_session

def init_db():
    import models
    #import services.alexa.models
    import services.mdl.models
    import services.et.models
    import services.phishtank.models
    
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
