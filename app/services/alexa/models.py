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
from StringIO import StringIO
from struct import unpack

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

def int2ip(addr):                                                               
    return inet_ntoa(pack("!I", addr))    

def ip2int(addr):                                                               
    return unpack("!I", inet_aton(addr))[0]  




class alexaModel(Base):
    __tablename__ = "alexa"
    ip = Column(INTEGER(unsigned = True), index=True, primary_key=True, autoincrement=False)
    domain = Column(String(256), index = True, primary_key=True)
    updated = Column(DATETIME, index = True, default=datetime.utcnow)
    rank = Column(INTEGER(unsigned = True), index=True, default = 0)
    
    def getIP(self):
        return int2ip(int(self.ip))
    
    def __repr__(self): 
        return "<domain: %s, ip: %s>" % (self.domain, self.getIP())
    
    def isTop(self, str_ip):
        ip = ip2int(str_ip)
        result = self.query.filter_by(ip = ip ).first()
        return result != None
        
    def __init__(self, ip = None, domain = None, rank = None):
        self.url = url
        
        if ip != None:
            self.ip = ip2int(ip)

        if domain != None: 
            self.domain = domain
            
        if rank != None:
            self.rank = rank  
            
        self.updated = datetime.utcnow()
        
        
        
    def insert(self, ip, domain, rank = 0):
        self.ip = ip
        self.domain = domain
        self.updated = datetime.utcnow()
        self.rank = rank
        
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
        print "Updating Alexa database"
        domain_list = self.fetch()
        
        for rank, domain in domain_list:
            try:
                (hostname, aliaslist, ipaddrlist) = gethostbyname_ex(domain)
                for ip in ipaddrlist:
                    if DEBUG:
                        print "INSERT: %s, %s, %s" % (ip, domain, rank)
                        
                    ip = ip.strip()
                    self.insert(ip2int(ip), domain, rank)
                
                #look up for domain and www.domain (but store the record only as domain)
                www = "www." + domain
                (hostname, aliaslist, ipaddrlist) = gethostbyname_ex(www)
                for ip in ipaddrlist:
                    if DEBUG:
                        print "INSERT: %s, %s, %s" % (ip, domain, rank)
                    
                    ip = ip.strip()
                    self.insert(ip2int(ip), domain, rank)
                    
            except AttributeError:
                continue
                    
            except RuntimeError:
                traceback.print_exc(file=sys.stderr)
                sys.exit(-1)
                
            except gaierror:
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
            zipData = response.read()
            zipFLO = BytesIO(zipData)
            
            zf = zipfile.ZipFile(zipFLO)
            filename = zf.namelist()[0]
            
            topCSV = zf.read(filename)
            topCSVFLO = BytesIO(topCSV)
            
            reader = csv.reader(topCSVFLO, delimiter=',')
            for row in reader:
                rank = str(row[0])
                domain = str(row[1]).strip()
                results.append((rank, domain))
                
            
        except csv.Error:
            traceback.print_exc(file=sys.stderr)
            
        except URLError:
            traceback.print_exc(file=sys.stderr)        
            
        except:
            traceback.print_exc(file=sys.stderr)
    
        return results
            

if __name__ == "__main__":
    ax = alexaModel()
    ax.update()


