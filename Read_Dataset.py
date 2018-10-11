#!/usr/bin/env python
import os, sys

from labkey.utils import create_server_context
from labkey.query import select_rows


def convert_unicode_to_str(list_of_rows):
    '''
    :param list_of_rows:
    :return: List of rows
    '''
    new_rows = []

    for row in list_of_rows:
        new_row = {}
        for i, v in row.items():
            key = i.encode('ascii', 'ignore')

            if (isinstance(v, unicode)):
                new_row[key] = v.encode('ascii', 'ignore')
            else:
                new_row[key] = v

        new_rows.append(new_row)

    return new_rows


print("Create a server context")

labkey_server = 'labkey.uhnresearch.ca'
contextPath = 'labkey'
schema = 'study'
project_name = sys.argv[1]  # Project folder name
table = sys.argv[2]  # Dataset name

table_name = table + ".txt"
filename = os.path.join(project_name, table_name)
print("Created a " + filename + " file.")

server_context = create_server_context(labkey_server, project_name, contextPath, use_ssl=True)
result = select_rows(server_context, schema, table)

if not os.path.exists(project_name):
    os.makedirs(project_name)

if result is not None:
    rows = result['rows']
    # print type(result)
    # print(result)

    new_rows = convert_unicode_to_str(rows)

    rows_dict = {}
    rows_dict["rows"] = new_rows

    # print(str(rows))
    file = open(filename, "w")
    # file.write(str(rows) + "\n")
    # file.write(str(new_rows) + "\n")
    file.write(str(rows_dict) + "\n")
    file.close()
    print("select_rows: Number of rows returned: " + str(result['rowCount']))
else:
    print('select_rows: Failed to load results from ' + schema + '.' + table)
