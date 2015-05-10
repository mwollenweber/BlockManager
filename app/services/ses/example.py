#!/usr/bin/python

import cif
import argparse
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

# CIF_BIN = '../cif-v1/libcif/bin/cif'

if __name__ == '__main__':
    # Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="example interface to CIF v1+ APIs")

    parser.add_argument('-c', '--confidence', help="specify the default confidence")
    parser.add_argument('-r', '--restriction', help='specify the default restriction')
    parser.add_argument("-C", "--config", default=os.path.expanduser("~/.cif"))
    parser.add_argument("-B", "--cif_binary", default="/opt/cif/bin/cif")

    args = parser.parse_args()

    rclient = cif.ClientINI(path=args.config, cif_binary=args.cif_binary)
    data = {}
    data['assessment'] = 'botnet'
    data['description'] = 'unknown'
    data['confidence'] = 50
    data['address'] = 'example.com'
    data['guid'] = 'everyone'

    ret = rclient.POST(data)
    ret = rclient.GET('example.com')
    pp.pprint(ret)

