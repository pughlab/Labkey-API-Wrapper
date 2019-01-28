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

            result = select_rows(serverContext, schema, table)

            if result is not None:
                row_to_add = result["rows"]

                for idx in range(len(row_to_add)):
                    row_to_add[idx] = removeUnnecessaryColumns(row_to_add[idx], idx)
                    row_to_add[idx] = changeDateTimeFormat(row_to_add[idx])
                    row_to_add[idx] = convertKeyToUpperCase(row_to_add[idx])
                    row_to_add[idx] = renameSpecificColumns(row_to_add[idx], table)
                dict[table] = row_to_add

                print("From the dataset " + table + ", the number of rows returned: " + str(result['rowCount']))
            else:
                print('select_rows: Failed to load results from ' + schema + '.' + table)
        except QueryNotFoundError:
            print('Error: The table ' + table + " was not found.")

    file.write(json.dumps((dict), indent=4, sort_keys=True))
    file.close()


def removeUnnecessaryColumns(row_to_add, idx):
    row_to_add.pop(u'_labkeyurl_PATIENT_ID', None)
    row_to_add.pop(u'_labkeyurl_ParticipantId', None)
    row_to_add.pop(u'lsid', None)

    return row_to_add


def changeDateTimeFormat(myDict):
    for key in myDict.keys():
        if ((type(myDict[key]) == str) and ("00:00:00" in myDict[key])):
            myDict[key] = myDict[key].split(" ")[0]

    return myDict


def convertKeyToUpperCase(myDict):
    result = {}
    for key, value in myDict.items():
        newKey = '_'.join(key.split()).upper()
        result[newKey] = value

    return result


def renameSpecificColumns(rowDict, datasetName):
    if datasetName == "Patients":
        rowDict["DATE_OF_BIRTH"] = rowDict.pop("DATE")

    return rowDict


if __name__ == "__main__":
    main()
