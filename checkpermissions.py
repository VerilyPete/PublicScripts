#!/usr/bin/env python

"""I built this script after an incident where another engineer had dragged an OS X .app
through a windows share and damaged the permissions, thereby making the .app only run when
logged in as the installed user. BeyondCompare for OS X doesn't yet support permission
comparison, so I threw this script together.
This script simply compares two folder locations, comparing
permissions and files and reporting any mismatches or missing/new files.
"""

import argparse
import os


class Get_Folder_Permissions:
    def __init__(self, filepath):
        """Takes a path to a folder and walks that folder, calling get_permissions to store
        permissions in a dictionary indexed by filename."""
        self.pathdict = {}
        self.filepath = filepath
        for dirname, dirs, files in os.walk(self.filepath):
            for f in files:
                self.pathdict[os.path.join(os.path.relpath(dirname, self.filepath), f)] = self.get_permissions(os.path.join(dirname, f))
            for d in dirs:
                self.pathdict[os.path.join(os.path.relpath(dirname, self.filepath), d)] = self.get_permissions(os.path.join(dirname, d))

    def get_permissions(self, filepath):
        """Gives the octal permission of a file."""
        return oct(os.stat(filepath).st_mode & 0o777)


def in_first_not_in_second(first_dict, second_dict):
    """Expects two dictionaries as input. Returns set containing
    all items found in first_dict but not in second_dict."""
    in_first_not_in_second_set = set([])
    in_first_not_in_second_set = set(first_dict.pathdict.keys()) - set(second_dict.pathdict.keys())
    return in_first_not_in_second_set


def print_and_number(first_dict, second_dict, print_string):
    """Takes two dictionaries as input. Prints the number of files found 
    in the first and missing in the second as well as the file paths. Intended
    to be used to find any files missing in an updated build.
    """
    info_set = in_first_not_in_second(first_dict, second_dict)
    if print_string == "add":
        print_string = "%s items added to %s.\n\n\n" % (str(len(info_set)), first_dict.filepath)
    if print_string == "diff":
        print_string = "%s items from %s not found in %s.\n" % (str(len(info_set)), first_dict.filepath, second_dict.filepath)
    print(print_string)
    for files in sorted(info_set):
        print(files)
    print("\n\n\n")


def file_permissions_changed(first_dict, second_dict):
    """Takes two dictionaries with filename/permissions as key/value as input.
    Compares permissions, reporting any mismatches."""
    for key in list(first_dict.pathdict.keys()):
        if key in second_dict.pathdict:
            if first_dict.pathdict[key] != second_dict.pathdict[key]:
                print("Value of %s changed. Old value %s, new value %s." % (key, first_dict.pathdict[key], second_dict.pathdict[key]))


def main(args):
    gp = Get_Folder_Permissions(args.goodpath)
    tp = Get_Folder_Permissions(args.testpath)
    unmatchedfiles = set(gp.pathdict.items()) ^ set(tp.pathdict.items())
    if not (unmatchedfiles):
        print("Files and Permissions match!")
    else:
        print_and_number(gp, tp, "diff")
        print_and_number(tp, gp, "add")
        file_permissions_changed(gp, tp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compares permissions of two paths supplied via commandline.')
    parser.add_argument('goodpath', help='Path to a directory with known-good permissions.')
    parser.add_argument('testpath', help='Path to the directory to be tested.')
    args = parser.parse_args()

main(args)
