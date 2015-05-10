'''
services/alexa/models.py


Copyright Matthew Wollenweber 2014
mjw@cyberwart.com

'''


import sys
import traceback
import zipfile
import csv
from config import url, DEBUG, SQLALCHEMY_DATABASE_URI

sys.path.append("../../")
sys.path.append("../../app")

from datetime import datetime
from socket import inet_aton, inet_ntoa, gethostbyname_ex, gethostbyaddr, getfqdn, gaierror
from sqlalchemy.dialects.mysql import INTEGER, BLOB, DATETIME, TINYINT, TEXT
from sqlalchemy import ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, Column, String
from urllib2 import urlopen, Request, URLError
from io import BytesIO
from urlparse import urlparse
from netaddr import IPNetwork

from app.models import  int2ip, ip2int


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False , autoflush=True, bind=engine))
db_session._model_changes = {}  

from app.database import Base

class etModel(Base):
    __tablename__ = "et"
    start = Column(INTEGER(unsigned = True), index=True, primary_key=True, autoincrement=False)
    end = Column(INTEGER(unsigned = True), index=True, primary_key=True, autoincrement=False)
    tdstamp = Column(DATETIME, index = True, default=datetime.utcnow)

    

    def insert_raw(self, start, end):
        self.start = start
        self.end = end
        self.tdstamp = datetime.utcnow()
                
        try:
            db_session.flush()
            db_session.merge(self)
            db_session.commit()
            
        except AttributeError:
            #traceback.print_exc(file=sys.stderr)
            meh = "meh"
            
        except:
            traceback.print_exc(file=sys.stderr)  
        
        
    def insert(self, str_start, str_end):
        self.start = ip2int(str_start)  
        self.end = ip2int(str_end)
        self.tdstamp = datetime.utcnow()
                
        try:
            db_session.flush()
            db_session.merge(self)
            db_session.commit()
            
        except AttributeError:
            #traceback.print_exc(file=sys.stderr)
            meh = "meh"
            
        except:
            traceback.print_exc(file=sys.stderr)
            
            
    
    def update(self):
        print "Updating ET database"
        for line in self.fetch():
            try:
                
                ip_range = IPNetwork(line)
                self.insert_raw(ip_range.first, ip_range.last)

            except AttributeError:
                traceback.print_exc(file=sys.stderr)
                continue
                    
            except RuntimeError:
                traceback.print_exc(file=sys.stderr)
                continue
                #sys.exit(-1)
                
                
            except gaierror:
                traceback.print_exc(file=sys.stderr)
                continue
                
            except KeyboardInterrupt:
                sys.exit(0)
                
                
            except:
                traceback.print_exc(file=sys.stderr)
                continue
    
    def fetch(self):
        results = []
        try:
            req = Request(url)
            response = urlopen(req)
            data = response.read()
            
            for line in BytesIO(data):
                if str(line).startswith("#") != True and len(line) > 8:
                    results.append(str(line).strip())
                     
                
        except KeyboardInterrupt:
            traceback.print_exc(file=sys.stderr)           
            sys.exit(0)        


        except URLError:
            traceback.print_exc(file=sys.stderr)        
            
        except:
            traceback.print_exc(file=sys.stderr)
    
        return results

        
    def isET(self, ip_str):
        target_ip = ip2int(ip_str)
        result = etModel.query.filter(target_ip >= etModel.start).filter(target_ip <= et.end).first() 
        if result:
            return True
        
        return False
    
    def isKnown(self, ip_str):
        return self.isET(self, ip_str)
    
if __name__ == "__main__":
    et = etModel()
    et.update()


