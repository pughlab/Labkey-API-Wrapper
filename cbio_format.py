#!/usr/bin/python

import os, sys, ast
import json
import labkey
from labkey.utils import create_server_context
from labkey.query import select_rows

filename = sys.argv[1]



d = {}
with open(filename) as f:
   json_string = f.readline()

   print json_string

   json
# print(d)
# print(type(d))