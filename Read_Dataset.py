import os, sys

from labkey.utils import create_server_context
from labkey.query import select_rows


def format_row_for_header(row):
    column_names = []
    column_types = []
    list_of_ones = [1] * len(row)

    for key in row:

        if (type(key) == unicode):
            key = key.encode('ascii', 'ignore')
        column_names.append(key)

        value_type = "STRING"

        if (type(row[key]) == int):
            value_type = "INTEGER"
        column_types.append(value_type)

    # first row
    column_names[0] = "#" + str(column_names[0])
    first_row = '\t'.join(column_names) + "\n"
    output_string = first_row

    # second row - is a duplicate of the first row
    output_string += first_row

    # third row
    column_types[0] = "#" + str(column_types[0])
    third_row = '\t'.join(str(e) for e in column_types) + "\n"
    output_string += third_row

    # forth row
    list_of_ones[0] = "#" + str(list_of_ones[0])
    output_string += '\t'.join(str(e) for e in list_of_ones) + "\n"

    return output_string


def format_row(curr_row):
    curr_row_values = []

    for key in curr_row:



        val = curr_row[key]

        if (type(curr_row[key]) == unicode):
            val = val.encode('ascii', 'ignore')

        # print "-----------_:"
        # print val , type(val)


        curr_row_values.append(val)

    print curr_row_values, len(curr_row_values)
    for item in curr_row_values:

        print item, type(item)
        if ((type(item) == str) and ("labkey" in item)): #and ("urn" in item)):
            print item, type(item)
            curr_row_values.remove(item)

    print curr_row_values, len(curr_row_values)

    output_string = '\t'.join(str(e) for e in curr_row_values) + "\n"

    return output_string


def main():
    labkey_server = 'labkey.uhnresearch.ca'
    # project_name = 'Comparison'  # Project folder name
    contextPath = 'labkey'
    schema = 'study'
    # table = "Patients"

    print("Hello World!")
    try:
        project_name = sys.argv[1]
        table = sys.argv[2]
        filename = table + ".txt"

        # print("Project name: " + project_name + " Filename: " + filename)
        if not os.path.exists(project_name):
            os.makedirs(project_name)
    except:
        print("Please run the command, pass in the \"project name or path\" and the dataset you want to read.")
        print("python read_dataset.py \"Demo/Demo Study\" \"Demographics\"")

    # file = open(os.path.join(project_name, filename), "w")
    file = open(filename, "w")
    # Create output
    server_context = create_server_context(labkey_server, project_name, contextPath, use_ssl=True)

    result = select_rows(server_context, schema, table)
    if result is not None:

        rows_list = result['rows']


        rows_list = result['rows']

        header = 0

        for curr_row in rows_list:

            if (header < 1):

                output_string = format_row_for_header(curr_row)
                file.write(output_string)

                header += 1

            print curr_row
            print "\n"
            output_string = format_row(curr_row)

            print output_string
            print "\n"
            file.write(output_string)

        print("Created a text file named: " + str(filename))

        print("select_rows: Number of rows returned: " + str(result['rowCount']))
        # print("select_columns: Number of columns returned: " + str(result['columnCount']))
    else:
        print('Select_rows: Failed to load results from ' + schema + '.' + table)

    file.close()


if __name__ == '__main__':
    main()
