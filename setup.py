import os, sys
from os import path
from os.path import expanduser

MACHINE = "labkey.uhnresearch.ca"
LOGIN = ""
PASSWORD = ""
NEW_LINE = "\n"


# Two options to log in:
# 1. with the user's email and password stored in the netrc file eg. user@labkey.org mypassword
# 2. with an apikey eg. python setup.py apikey password apikey|8f28f044323412342ebb85a2cbab6a4

if len(sys.argv) == 3:
    LOGIN = sys.argv[1]
    PASSWORD = sys.argv[2]


def main():
    try:
        import labkey  # Checking if LabKey module is installed.
    except ImportError:
        print 'Error, Module ModuleName is required'

    if os.name == 'nt':  # for window machines
        filename = "_netrc"
    else:
        filename = ".netrc"

    # The file should be located in your home directory
    HOME = expanduser("~")
    filename = HOME + "/" + filename

    # Delete file if it already exists
    # if path.exists(filename):
    #     os.remove(filename)

    file = open(filename, "a")

    COMMA = ", "
    output_line = "machine " + MACHINE + COMMA + "login " + LOGIN + COMMA + "password " + PASSWORD + NEW_LINE;
    # print(output_line)

    # file.write(output_line)

    file.write("machine " + MACHINE + NEW_LINE)
    file.write("login " + LOGIN + NEW_LINE)
    file.write("password " + PASSWORD + NEW_LINE)

    file.close()

    # File set so that you are the only user who can read it
    os.chmod(filename, 0o700)

    return

if __name__ == '__main__':
    main()
