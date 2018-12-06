#!/usr/bin/python
import os, argparse
from os import path
from os.path import expanduser
import shutil

HOME = expanduser("~")


def get_options():
    parser = argparse.ArgumentParser(description="Storing labkey credentials in a netrc file")
    parser.add_argument("-u", "--user_email", type=str, required=True,
                        help="input user's email address or the username: apikey")
    parser.add_argument("-p", "--user_password", type=str, required=True,
                        help="input user's password or unique apikey")

    return parser.parse_args()


def remove_labkey_info(filename, netrc_file):
    filename_temp = "temp.txt"

    with open(filename, 'r') as oldfile, open(filename_temp, 'w') as tempFile:
        for line in oldfile:
            if not ("labkey" in line):
                tempFile.write(line)

    os.remove(filename)

    filename = HOME + "/" + netrc_file
    shutil.copy(filename_temp, filename)
    os.remove(filename_temp)

    return filename


def main():
    MACHINE = "labkey.uhnresearch.ca"
    args = get_options()
    user_email = args.user_email
    user_password = args.user_password

    try:
        import labkey  # Checking if labkey module is installed.
    except ImportError:
        print 'Error, Module ModuleName is required'
        exit()

    if os.name == 'nt':  # for window machines.
        netrc_file = "_netrc"
    else:
        netrc_file = ".netrc"

    # The file should be located in your home directory.
    filename = HOME + "/" + netrc_file

    # If file exists, copy every line that doesn't have labkey info to temp file, delete file and rename temp file.
    if path.exists(filename):
        filename = remove_labkey_info(filename, netrc_file)

    file = open(filename, "a")

    output_line = "machine " + MACHINE + "\t" + "login " + user_email + "\t" + "password " + user_password + "\n"
    file.write(output_line)

    file.close()

    # Grant file's permission to only the user.
    os.chmod(filename, 0o700)


if __name__ == '__main__':
    main()
