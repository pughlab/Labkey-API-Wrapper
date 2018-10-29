#!/usr/bin/python
import os, sys, json

from labkey.utils import create_server_context
from labkey.query import select_rows

def obj_dict(obj):
    return obj.__dict__

print("Create a server context")

labkey_server = 'labkey.uhnresearch.ca'
contextPath = 'labkey'
schema = 'study'
project_name = sys.argv[1]  # Project folder name
table = sys.argv[2]  # Dataset name

table_name = table + ".json"
filename = os.path.join(project_name, table_name)
print("Created a " + filename + " file.")

server_context = create_server_context(labkey_server, project_name, contextPath, use_ssl=True)
result = select_rows(server_context, schema, table)

if not os.path.exists(project_name):
    os.makedirs(project_name)

file = open(filename, "w")
if result is not None:

    json_string = json.dumps(result["rows"], default=obj_dict)
    file.write(json_string)
    print("select_rows: Number of rows returned: " + str(result['rowCount']))
else:
    print('select_rows: Failed to load results from ' + schema + '.' + table)


# file.write(json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4, separators=(',', ': ')))

file.close()