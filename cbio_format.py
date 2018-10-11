import os, sys
import json
import labkey
from labkey.utils import create_server_context
from labkey.query import select_rows

filename = sys.argv[1]

with open(filename) as f:
    # lines = f.read().splitlines()
    lines = f.readline()
    rows = lines
    print lines
    print type(lines)
