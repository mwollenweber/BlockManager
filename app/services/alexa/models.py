'''
services/alexa/models.py

Copyright Matthew Wollenweber 2014
mjw@insomniac.technology


1. Fetch the Alexa Top 1M list
2. Resolve the domain and www.domain to IP addresses
3. Insert those IPs into a database using SQLAlechemy

'''

import sys
import traceback
import zipfile
import csv
import threading
import time
import logging

from config import url
from datetime import datetime
from socket import inet_aton, inet_ntoa, gethostbyname_ex, gethostbyaddr, getfqdn, gaierror
from sqlalchemy.dialects.mysql import INTEGER, DATETIME
from urllib2 import urlopen, Request, URLError
from io import BytesIO
from struct import unpack, pack
from sqlalchemy.exc import IntegrityError, InvalidRequestError, OperationalError
from sqlalchemy import Column, String

# ensure SQLALchemy pool_size is increased to handle several threads
# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
from app.database import Base, db_session


# Store IP (v4) addresses as INTs
def int2ip(addr):
    return inet_ntoa(pack("!I", addr))


def ip2int(addr):
    return unpack("!I", inet_aton(addr))[0]


class alexaModel(Base):
    __tablename__ = "alexa"
    __table_args__ = {'extend_existing': True}

    ip = Column(INTEGER(unsigned=True), index=True, primary_key=True, autoincrement=False)
    # Domain should be larger, but limited by my cheap database instance
    domain = Column(String(128), index=True, primary_key=True)
    updated = Column(DATETIME, index=True, default=datetime.utcnow)
    rank = Column(INTEGER(unsigned=True), index=True, default=0)

    def __init__(self, ip=None, domain=None, max_rank=10000, max_threads=16):
        if ip is not None:
            self.ip = ip2int(ip)

        if domain is not None:
            self.domain = domain

        self.max_rank = max_rank
        self.max_threads = max_threads
        if self.max_threads > self.max_rank:
            self.max_threads = self.max_rank - 1

        self.url = url
        self.updated = datetime.utcnow()

    def __repr__(self):
        return "<domain: %s, ip: %s>" % (self.domain, self.getIP())

    def getIP(self):
        return int2ip(int(self.ip))

    def isTop(self, str_ip):
        ip = ip2int(str_ip)
        result = self.query.filter_by(ip=ip).first()
        return (result is not None)

    def dumpAsCSV(self, topN=0):
        if topN == 0:
            topN = self.max_rank

        data = self.query \
            .filter(alexaModel.rank <= topN) \
            .order_by(alexaModel.rank) \
            .all()

        print "rank, domain, ip, updated"
        for d in data:
            print "%s, %s, %s, %s" % (d.rank, d.domain, int2ip(d.ip), d.updated)

        return False

    def insert(self, ip, domain, rank=0):
        self.ip = ip
        self.domain = domain
        self.updated = datetime.utcnow()
        self.rank = rank

        try:
            db_session.merge(self)
            db_session.commit()

        except AttributeError:
            # traceback.print_exc(file=sys.stderr)
            pass

        except IntegrityError:
            pass

        except InvalidRequestError:
            db_session.rollback()

        except OperationalError:
            traceback.print_exc(file=sys.stderr)

    def updateRecord(self, domain, rank):
        (hostname, aliaslist, ipaddrlist) = gethostbyname_ex(domain)
        for ip in ipaddrlist:
            ip = ip.strip()
            self.insert(ip2int(ip), domain, rank)

        # look up for domain and www.domain (but store the record only as domain)
        www = "www." + domain
        (hostname, aliaslist, ipaddrlist) = gethostbyname_ex(www)
        for ip in ipaddrlist:
            ip = ip.strip()
            self.insert(ip2int(ip), domain, rank)

        return True

    def update(self):
        domain_list = self.fetch()
        domain_list.reverse()
        domain_list = domain_list[0:self.max_rank]

        print "Len of domains = %s" % len(domain_list)

        self.thread_list = []
        (rank, domain) = domain_list.pop()
        while len(domain_list) > 0:
            try:
                for i in xrange(0, self.max_threads - len(self.thread_list)):
                    t = threading.Thread(target=self.updateRecord, args=(domain, rank))
                    t.daemon = True
                    t.start()
                    self.thread_list.append(t)

                    (rank, domain) = domain_list.pop()
                    if int(rank) % 10 == 0:
                        print "Processing Alexa Rank=%s" % rank

                time.sleep(2)
                new_thread_list = []
                for t in self.thread_list:
                    if not t.isAlive():
                        t.handled = True

                    else:
                        new_thread_list.append(t)

                self.thread_list = new_thread_list
                db_session.commit()

            except AttributeError:
                continue

            except RuntimeError:
                traceback.print_exc(file=sys.stderr)
                sys.exit(-1)

            except gaierror:
                continue

            except IndexError:
                continue

            except KeyboardInterrupt:
                sys.exit(0)

        for t in self.thread_list:
            t.join(10)

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

        return results


if __name__ == "__main__":
    ax = alexaModel(max_rank=10000, max_threads=8)
    ax.update()
    ax.dumpAsCSV()
