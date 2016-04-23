import traceback
import sys
import csv
import pprint
import zipfile
import StringIO
import requests
from app.config import DEBUG


def main():
    csvZipURL = 'http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip'
    csvzip = requests.get(csvZipURL).content

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
            name = name.replace('"', '').replace("'", '')

            # mydb.insertGeoIP(start, end, code, name)
            print "%s, %s, %s, %s" % (start, end, code, name)

        except RuntimeError:
            traceback.print_exc()
            print "Exiting!"
            sys.exit(-1)

        except:
            pprint.pprint("ERROR: Unknown error inserting ROW = %s\n" % row, stream=sys.stderr)
            traceback.print_exc()
            print "ERROR: Exiting"
            sys.exit(-1)


if __name__ == "__main__":
    main()
