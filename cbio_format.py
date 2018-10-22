#!/usr/bin/python

import os, sys, ast
import json
import labkey
from labkey.utils import create_server_context
from labkey.query import select_rows

filename = sys.argv[1]



d = {}
with open(filename) as f:
    for line in f:

        new_line =  ast.literal_eval(line)
        print type(line)
        print type(new_line)

# print(d)
# print(type(d))
print(new_line.keys())
print (new_line["rows"][0])