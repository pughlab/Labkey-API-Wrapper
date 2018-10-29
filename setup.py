#!/usr/bin/python

import os, sys
from os import path
from os.path import expanduser

MACHINE = "labkey.uhnresearch.ca"
LOGIN = ""
PASSWORD = ""
HOME = expanduser("~")

# Two options to log in:
# 1. with the user's email address and password eg. python setup.py user@labkey.org mypassword
# 2. with an apikey eg. python setup.py apikey "apikey|8f28f0423434323412cbaw45242342342db6a4"

if len(sys.argv) == 3:
    LOGIN = sys.argv[1]
    PASSWORD = sys.argv[2]

# python setup.py apikey apikey|c4716e2076b57b1dce5d7a5f3c7d2d8a
# LOGIN = "apikey"
# PASSWORD = "apikey|c4716e2076b57b1dce5d7a5f3c7d2d8a"

def main():
    try:
        import labkey  # Checking if LabKey module is installed.
    except ImportError:
        print 'Error, Module ModuleName is required'

    if os.name == 'nt':  # for window machines
        netrc_file = "_netrc"
    else:
        netrc_file = ".netrc"

    # The file should be located in your home directory
    filename = HOME + "/" + netrc_file

    # If file exists, copy every line that doesn't have labkey info to temp file, delete filename and replace it.
    if path.exists(filename):
        remove_labkey_info(filename, netrc_file)

    file = open(filename, "a")

    output_line = "machine " + MACHINE + "\t" + "login " + LOGIN + "\t" + "password " + PASSWORD + "\n"
    file.write(output_line)

    file.close()

    # Grant file's full permission to only the user.
    os.chmod(filename, 0o700)


def remove_labkey_info(filename, netrc_file):
    filename_temp = "temp.txt"

    with open(filename, 'r') as oldfile, open(filename_temp, 'w') as tempFile:
        for line in oldfile:
            if not ("labkey" in line):
                tempFile.write(line)

    os.remove(filename)
    filename = HOME + "/" + netrc_file

    with open(filename_temp, 'r') as tempFile:
        with open(filename, 'w') as newfile:
            for line in tempFile:
                newfile.write(line)

    os.remove(filename_temp)


if __name__ == '__main__':
    main()
