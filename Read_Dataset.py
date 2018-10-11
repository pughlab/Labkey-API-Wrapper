#!/usr/bin/env python
# coding=utf-8

import os, sys

from labkey.utils import create_server_context
from labkey.query import select_rows

def convert_unicode_to_str(list_of_rows):
    new_rows = []

    for row in list_of_rows:
        My_Dicts = {}
        for i, v in row.items():
            key = i.encode('ascii', 'ignore')

            if (isinstance(v, unicode)):
                My_Dicts[key] = v.encode('ascii', 'ignore')
            else:
                My_Dicts[key] = v

        new_rows.append(My_Dicts)

    return new_rows


print("Create a server context")

labkey_server = 'labkey.uhnresearch.ca'
project_name = 'ModuleAssayTest'  # Project folder name
contextPath = 'labkey'
schema = 'study'

project_name = sys.argv[1]
table = sys.argv[2]

table_name = table + ".txt"
filename = os.path.join(project_name, table_name)
print("Created a " + filename + " file.")


server_context = create_server_context(labkey_server, project_name, contextPath, use_ssl=True)

result = select_rows(server_context, schema, table)

if not os.path.exists(project_name):
    os.makedirs(project_name)


if result is not None:
    rows = result['rows']

    new_rows = convert_unicode_to_str(rows)

    # print(str(new_rows))
    # file = open(filename, 'w')
    file = open(filename, "w")
    file.write(str(new_rows) + "\n")
    file.close()
    print("select_rows: Number of rows returned: " + str(result['rowCount']))
else:
    print('select_rows: Failed to load results from ' + schema + '.' + table)



