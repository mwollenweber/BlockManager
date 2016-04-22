#!/usr/bin/python
'''

Copyright Matthew Wollenweber 2012
mjw@insomniac.technology
All Rights Reserved.

'''
__description__ = ''
__author__ = 'Matthew Wollenweber'
__email__ = 'mjw@cyberwart.com'
__version__ = '0.1'
__date__ = '2012/09/22'

import traceback
import sys
import argparse
import csv
import pprint
import ConfigParser
import urllib2
import zipfile
import StringIO
import app.database as db

DEBUG = True


def main():
    parser = argparse.ArgumentParser(prog='template', usage='%(prog)s [options]')
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--version', action='version', version='%(prog)s -1.0')
    parser.add_argument('--debug', '-D', type=bool, dest='DEBUG', default=False)

    args = parser.parse_args()


    config_file = "server.cfg"
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    csvZipURL = config.get('geoip', 'file')
    response = urllib2.urlopen(csvZipURL)
    csvzip = response.read()


    mydb = db.db(config_file="server.cfg")

    # fixme - this is really what I'm doing?
    # Turn geop.csv.gz to geop.csv
    zipStream = StringIO.StringIO(csvzip)
    zipf = zipfile.ZipFile(zipStream)
    csvbuf = zipf.read(name='GeoIPCountryWhois.csv')
    buf = StringIO.StringIO(buf=csvbuf)

    reader = csv.reader(buf)
    for row in reader:
        try:
            start = row[2]
            end = row[3]
            code = row[4]
            name = row[5]
            name = name.replace('"', '')
            name = name.replace("'", '')

            mydb.insertGeoIP(start, end, code, name)

        except RuntimeError:
            traceback.print_exc()
            print "Exiting!"
            sys.exit(-1)

        except:
            pprint.pprint("ERROR: Unknown error inserting ROW = %s\n" % row, stream=sys.stderr)
            traceback.print_exc()
            print "ERROR: Exiting"
            sys.exit(-1)

    print "Finis"


if __name__ == "__main__":
    main()
