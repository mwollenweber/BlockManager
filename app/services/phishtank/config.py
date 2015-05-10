#http://data.phishtank.com/data/<your app key>/online-valid.json
#http://www.phishtank.com/api_info.php
#http://checkurl.phishtank.com/checkurl/
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://blockmanager:bmanager@localhost/BlockManager'
apikey = "bac65dd7654f60d62770d1ed726f0d9aa5ef5596fe402d3de605c64b6039e7ed"
base_url = "http://data.phishtank.com/data/"
page = "/online-valid.json"
url = base_url + apikey + page
