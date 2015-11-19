#!/usr/bin/python

import argparse
import json
import os
from subprocess import call
import sys


if sys.platform == 'darwin':
    PATH_TO_HOSTS = "/private/etc/hosts"
    CALL_STRING = (['cat', PATH_TO_HOSTS])
    permission_error = 'Permission denied. Use sudo.'
elif sys.platform == 'win32':
    PATH_TO_HOSTS = os.path.join(os.path.expandvars('%SystemRoot%'), 'system32',
                                 'drivers', 'etc', 'hosts')
    CALL_STRING = (['cmd.exe', '/c', 'type', PATH_TO_HOSTS])
    permission_error = 'Permission denied. Open an admin commandline.'


def buildhosts(json_path):
    entries = []
    try:
        with open(json_path, 'r') as host_json:
            hostlist = json.load(host_json)
    except (IOError, OSError):
        print('Invalid path or permission denied.')
    for host, ip in list(hostlist.items()):
        entries.append(('%s\t%s\n') % (ip, host))
    checkhosts(entries)


def checkhosts(hostlist):
    """ Opens hosts file at supplied path and checks for hosts listed in hostlist.
    If entries in hostlist aren't found in hosts file, they're written. If they are
    found, removehosts is invoked and hostlist & hostsfile objects are passed to it.
    Additional hosts can be added by defining them in iplist.json

    """

    writtenentries = []
    try:
        with open(PATH_TO_HOSTS, 'r') as readhosts:
            hostsfile = readhosts.readlines()
    except (OSError, IOError, UnboundLocalError):
        print('\nHosts file not found. Is your path correct?\n')
    try:
        with open(PATH_TO_HOSTS, 'a+') as hosts:
            if not any(x in hostlist for x in hostsfile):
                [writtenentries.append(entry.rstrip('\n')) for entry in hostlist
                    if entry not in hostsfile]
                [hosts.write(entry) for entry in hostlist if entry not in hostsfile]
                for x in writtenentries:
                    print('%s added to %s' % (x, PATH_TO_HOSTS))
            else:
                removehosts(hostlist, hostsfile)
    except (IOError, OSError):
        print(permission_error)
        exit()


def removehosts(hostlist, hostsfile):
    """Iterates over hostfile, removing anything referenced in hostlist that exists
    in hostsfile before writing hostsfile out to PATH_TO_HOSTS.
    """
    removedentries = []
    [removedentries.append(entry.rstrip('\n')) for entry in hostlist if entry in hostsfile]
    [hostsfile.remove(entry) for entry in hostlist if entry in hostsfile]
    with open(PATH_TO_HOSTS, 'w') as writehosts:
        writehosts.writelines([x for x in hostsfile])
    for x in removedentries:
        print('%s removed from %s' % (x, PATH_TO_HOSTS))


def main(args):
    buildhosts(args.json_path)
    print('\n Contents of %s \n' % (PATH_TO_HOSTS))
    call(CALL_STRING)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add hostsfile entries from iplist.json to your hostsfile.\
                                     Remove them if they\'ve already been entered.')
    parser.add_argument('--json', dest='json_path', default=os.path.join(os.path.dirname(sys.argv[0]), 'iplist.json'),
                        help='Specify the location of your json file of hosts and IP addresses.')
    args = parser.parse_args()
    main(args)
