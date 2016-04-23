'''
services/alexa/models.py


Copyright Matthew Wollenweber 2014
mjw@cyberwart.com

'''

import sys
import traceback
import zipfile
import csv
from app.config import DEBUG, SQLALCHEMY_DATABASE_URI
from app.config import MDL_URL as url

from datetime import datetime
from socket import inet_aton, inet_ntoa, gethostbyname_ex, gethostbyaddr, getfqdn, gaierror
from sqlalchemy.dialects.mysql import INTEGER, BLOB, DATETIME, TINYINT, TEXT
from sqlalchemy import ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, Column, String
from urllib2 import urlopen, Request, URLError
from io import BytesIO
from urlparse import urlparse

from app.models import int2ip, ip2int

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
db_session._model_changes = {}

from app.database import Base


class mdlModel(Base):
    __tablename__ = "mdl"
    __table_args__ = {'extend_existing': True}
    ip = Column(INTEGER(unsigned=True), index=True, primary_key=True, autoincrement=False)
    url = Column(String(256), index=True)
    domain = Column(String(128), index=True, primary_key=True)
    date = Column(DATETIME, index=True, default=datetime.utcnow)
    reverseLookup = Column(String(128), index=True)
    description = Column(String(256), index=False)
    registrant = Column(String(128), index=True)

    def getIP(self):
        return int2ip(int(self.ip))

    def __repr__(self):
        return "<domain: %s, ip: %s>" % (self.domain, self.getIP())

    def isKnown(self, str_ip):
        ip = ip2int(str_ip)
        result = self.query.filter_by(ip=ip).first()
        return result != None

    def __init__(self, ip=None, domain=None, url=None, date=None, reverseLookup=None, description=None,
                 registrant=None):
        self.url = url

        if ip != None:
            self.ip = ip2int(ip)

    def insert(self, ip_str, domain, reverseLookup=None, date=None, registrant=None, description=None, url=None):
        self.ip = ip2int(ip_str)

        # MDL usually provides a URL without "http://" and calls it "domain"; we separate
        if url == None:
            self.url = "http://" + domain
            urlResults = urlparse(self.url)
            self.domain = urlResults[1]
        # if I passed the URL argument I'm going to assume I preprocessed
        else:
            self.url = url
            self.domain = domain

        # their date is weird
        date = str(date).replace("_", " ")
        self.date = date
        self.registrant = registrant
        self.reverseLookup = reverseLookup

        try:
            db_session.flush()
            db_session.merge(self)
            db_session.commit()

        except AttributeError:
            # traceback.print_exc(file=sys.stderr)
            meh = "meh"

        except:
            traceback.print_exc(file=sys.stderr)

    def update(self):
        print "Updating MDL database"
        mdlDictList = self.fetch()

        for mdlDict in mdlDictList:
            try:
                self.insert(mdlDict["ip_str"], mdlDict["domain"], mdlDict["reverseLookup"], mdlDict["date"],
                            mdlDict["registrant"], mdlDict["description"])

            except AttributeError:
                continue

            except RuntimeError:
                traceback.print_exc(file=sys.stderr)
                continue
                # sys.exit(-1)


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
            data = response.read()

            mdlCSVFLO = BytesIO(data)

            reader = csv.reader(mdlCSVFLO, delimiter=',')
            for row in reader:
                date = str(row[0]).strip()
                domain = str(row[1]).strip()
                ip_str = str(row[2]).strip()
                reverseLookup = str(row[3]).strip()
                description = str(row[4]).strip()
                registrant = str(row[5]).strip()
                print "IP = %s" % ip_str
                results.append({"date": date, "domain": domain, "ip_str": ip_str, "reverseLookup": reverseLookup,
                                "description": description, "registrant": registrant})


        except csv.Error:
            traceback.print_exc(file=sys.stderr)

        except URLError:
            traceback.print_exc(file=sys.stderr)

        except:
            traceback.print_exc(file=sys.stderr)

        return results


if __name__ == "__main__":
    mdl = mdlModel()
    mdl.update()
