#!/usr/bin/python
import os, json, argparse

from labkey.utils import create_server_context
from labkey.exceptions import QueryNotFoundError
from labkey.query import select_rows

def get_options():
    parser = argparse.ArgumentParser(description="Process the commandline arguments for labkey api")
    parser.add_argument("-i", "--input", type=str, required=True, help="input project name on Labkey")
    parser.add_argument("-o", "--output", type=str, required=True, help="output file name including path")

    return parser.parse_args()


def main():
    args = get_options()
    dictionaryFromFile = []

    with open('data/dictionary.txt', 'r') as inf:
        for line in inf:
            dictionaryFromFile.append(eval(line))

    labkeyDictionary = dictionaryFromFile[0]

    labkeyServer = 'labkey.uhnresearch.ca'
    contextPath = 'labkey'
    schema = 'study'

    projectName = args.input.lower()

    if projectName not in labkeyDictionary:
        print('Caught bad project name. Please pass in a project name that is on labkey.')
        exit()
    projectDatasets = labkeyDictionary[projectName]

    output_folder = "results"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file = os.path.join(output_folder, args.output)

    # Delete file if it already exists in the directory
    if os.path.isfile(output_file):
        os.remove(output_file)

    print("Create a server context")
    serverContext = create_server_context(labkeyServer, projectName, contextPath, use_ssl=True)
    file = open(output_file, "w")
    dict = {}

    print("Created a " + output_file + " file.")
    for table in projectDatasets:
        try:

            ###################
            # Test sort and select columns
            ###################

            # column1 = u'PATIENT_ID'
            # column2 = u'date'
            # column3 = u'REGISTRATION_DATE'
            #
            # result = select_rows(serverContext, schema, table, max_rows=5, offset=10, include_total_count=False,
            #                      columns=",".join([column1, column2, column3]),
            #                      sort=column1 + ', -' + column2 + ', -' + column3)  # use '-' to sort descending


            result = select_rows(serverContext, schema, table)

            if result is not None:
                row_to_add = result["rows"]

                # Delete Labkey identifier columns from rows
                for idx in range(len(row_to_add)):
                    row_to_add[idx].pop(u'_labkeyurl_PATIENT_ID', None)
                    row_to_add[idx].pop(u'_labkeyurl_ParticipantId', None)
                    row_to_add[idx].pop(u'lsid', None)

                # print type(row_to_add)
                # print(result["rows"])
                dict[table] = row_to_add

                print("From the dataset " + table + ", the number of rows returned: " + str(result['rowCount']))
            else:
                print('select_rows: Failed to load results from ' + schema + '.' + table)
        except QueryNotFoundError:
            print('Error: The table ' + table + " was not found.")

    # file.write(json.dumps((dict), indent=4, sort_keys=True))
    file.write(json.dumps((dict), indent=4)) #, sort_keys=True))
    file.close()


if __name__ == "__main__":
    main()
