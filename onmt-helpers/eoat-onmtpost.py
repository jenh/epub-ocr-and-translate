#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import requests
import sys
import os

arglength = len(sys.argv)

if arglength <= 2:
    ruleid = str(100)
else:
    ruleid = sys.argv[2]

if arglength <= 1:
    print('Please enter the string to translate!')
    sys.exit(0)
else:
    req = sys.argv[1]
    pass

ip = os.environ['HOST']
port = os.environ['PORT']
url_root = os.environ['URL_ROOT']

url='http://' + ip + ':' + port + url_root + '/translate'
data='[{"src": "' + req +'", "id": ' + ruleid +'}]'

output = requests.post(url, data=data.encode('utf-8')).text

myjson = json.loads(output)
input = myjson[0][0]['src']
output = myjson[0][0]['tgt']

print(input)
print(output)
