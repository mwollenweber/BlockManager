#!env/bin/python
# coding: utf-8
'''

Copyright Matthew Wollenweber 2015
mjw@insomniac.technology
All Rights Reserved.

'''

__description__ = ''
__author__ = 'Matthew Wollenweber'
__email__ = 'mjw@insomniac.technology'
__version__ = '0.0.1'
__date__ = '2015/01/06'

import sys
import os
import traceback
from app import create_app

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5000))
        myapp = create_app("development")
        myapp.run(debug=True, host='0.0.0.0', port=8000)

    except KeyboardInterrupt:
        print "KeyboardInterrupt! Exiting."
        sys.exit(0)

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=5, file=sys.stderr)
        sys.exit(-1)
