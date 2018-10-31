#!/usr/bin/python
import os, json, argparse

from labkey.utils import create_server_context
from labkey.exceptions import QueryNotFoundError
from labkey.query import select_rows


def obj_dict(obj):
    return obj.__dict__


def get_options():
    parser = argparse.ArgumentParser(description="Process the commandline arguments for labkey api")
    parser.add_argument("-i", "--input", type=str, required=True, help="input project name on Labkey")
    parser.add_argument("-o", "--output", type=str, required=True, help="output file name including path")

    return parser.parse_args()


def main():
    args = get_options()
    dicts_from_file = []

    with open('data/dictionary.txt', 'r') as inf:
        for line in inf:
            dicts_from_file.append(eval(line))

    Labkey_dictionary = dicts_from_file[0]

    labkey_server = 'labkey.uhnresearch.ca'
    contextPath = 'labkey'
    schema = 'study'
    output_folder = "results"
    project_name = args.input.lower()

    if project_name not in Labkey_dictionary:
        print('Caught bad project name. Please pass in a project name that is on labkey.')
        exit()
    project_datasets = Labkey_dictionary[project_name]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file = os.path.join(output_folder, args.output)

    # Delete file if it already exists in the directory
    if os.path.isfile(output_file):
        os.remove(output_file)

    print("Create a server context")
    server_context = create_server_context(labkey_server, project_name, contextPath, use_ssl=True)
    file = open(output_file, "w")
    dict = {}

    print("Created a " + output_file + " file.")
    for table in project_datasets:
        try:
            result = select_rows(server_context, schema, table)

            if result is not None:
                dict[table] = result["rows"]
                print("From the dataset " + table + ", the number of rows returned: " + str(result['rowCount']))
            else:
                print('select_rows: Failed to load results from ' + schema + '.' + table)
        except QueryNotFoundError:
            print('Error: The table ' + table + " was not found.")

    file.write(json.dumps(dict))
    file.close()


if __name__ == "__main__":
    main()