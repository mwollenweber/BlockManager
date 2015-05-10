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
import traceback
from app import create_app

if __name__ == '__main__':
    app = create_app("production")
    try:
        app.run(debug=True, host='0.0.0.0', port=80)

    except:
        traceback.print_exc(file=sys.stderr)
        app.run(debug=True, host='0.0.0.0', port=8000)