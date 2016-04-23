from datetime import datetime
from sqlalchemy.dialects.mysql import INTEGER, BLOB, DATETIME, TINYINT, TEXT
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from app.database import Base
from app.config import DEBUG, SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
db_session._model_changes = {}


class geoIPModel(Base):
    __tablename__ = "geoip"
    __table_args__ = {'extend_existing': True}
    ip = Column(INTEGER(unsigned=True), index=True, primary_key=True, autoincrement=False)
    tdstamp = Column(DATETIME, index=True, default=datetime.utcnow)
    country_code = Column(String(8), index=True)
    country_name = Column(String(64), index=True)

    def __init__(self):
        print "Geoip init"
