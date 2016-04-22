'''

Copyright Matthew Wollenweber 2015
mjw@cyberwart.com
All Rights Reserved.

'''

__description__ = ''
__author__ = 'Matthew Wollenweber'
__email__ = 'mjw@cyberwart.com'
__version__ = '0.1'
__date__ = '2012/09/22'

import sys
import argparse
import traceback
import app.database as db
from app.models import int2ip

DEBUG = True


def main():
    parser = argparse.ArgumentParser(prog='template', usage='%(prog)s [options]')
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--version', action='version', version='%(prog)s -1.0')
    parser.add_argument('--debug', '-D', type=bool, dest='DEBUG', default=False)

    mydb = db.db(config_file="server.cfg")
    cur = mydb.get_cur()
    con = mydb.get_con()

    query = '''SELECT DISTINCT(ip) FROM logins'''
    cur.execute(query)
    rows = cur.fetchall()
    for r in rows:
        try:
            ip = long(r[0])

            #filter the special snowflakes 10.0.0.0/8
            if ip > 167772160 and ip < 184549375:
                #print "DEBUG: passing on a 10/8"
                continue

            #192.168.0.0/16
            if ip > 3232235520 and ip < 3232301055:
                #print "DEBUG: passing on 192.168/8"
                continue

            query = '''SELECT code FROM geoip WHERE %s BETWEEN start AND end LIMIT 1''' % str(ip)
            cur.execute(query)
            code = cur.fetchone()[0]

            query = '''REPLACE INTO ip2country (ip, code) VALUES ('%s', '%s')''' % (str(ip), code)
            cur.execute(query)

        except TypeError:
            print "ERROR: Unable to execute query %s" % query
            traceback.print_exc()
            continue

    # fixme, does the orderby do anything useful?
    query = '''REPLACE INTO user2country
               SELECT logins.username, logins.domain, ip2country.code
               FROM logins
               JOIN ip2country on logins.ip = ip2country.ip
               GROUP BY logins.username, logins.domain, ip2country.code'''

    cur.execute(query)
    con.commit()

if __name__ == "__main__":
    main()
