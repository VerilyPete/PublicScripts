#!/usr/bin/python

import os
from subprocess import call
from sys import platform

HOST1 = "146.215.250.206\twww.sonycreativesoftware.com\n"
HOST2 = "146.215.250.207\twww.mediasoftwareapps.com\n"

if platform == 'darwin':
    PATH_TO_HOSTS = "/private/etc/hosts"
    CALL_STRING = (['cat', PATH_TO_HOSTS])
    permission_error = 'Permission denied. Use sudo.'
elif platform == 'win32':
    PATH_TO_HOSTS = os.path.join(os.path.expandvars('%SystemRoot%'), 'system32',
                                 'drivers', 'etc', 'hosts')
    CALL_STRING = (['cmd.exe', '/c', 'type', PATH_TO_HOSTS])
    permission_error = 'Permission denied. Open an admin commandline.'


def checkhosts():
    """ Opens hosts file at supplied path and checks for hosts listed in hostlist.
    If entries in hostlist aren't found in hosts file, they're written. If they are
    found, removehosts is invoked and hostlist & hostsfile objects are passed to it.
    Additional hosts can be added by defining them as constants and adding their name
    to hostlist.

    """
    hostlist = [HOST1, HOST2]
    writtenentries = []
    try:
        with open(PATH_TO_HOSTS, 'r') as readhosts:
            hostsfile = readhosts.readlines()
    except (OSError, IOError, UnboundLocalError):
        print '\nHosts file not found. Is your path correct?\n'
    try:
        with open(PATH_TO_HOSTS, 'a+') as hosts:
            if not any(x in hostlist for x in hostsfile):
                [writtenentries.append(entry.rstrip('\n')) for entry in hostlist
                    if entry not in hostsfile]
                [hosts.write(entry) for entry in hostlist if entry not in hostsfile]
                for x in writtenentries:
                    print '%s added to %s' % (x, PATH_TO_HOSTS)
            else:
                removehosts(hostlist, hostsfile)
    except (IOError, OSError):
        print permission_error
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
        print '%s removed from %s' % (x, PATH_TO_HOSTS)


def main():
    checkhosts()
    print '\n Contents of %s \n' % (PATH_TO_HOSTS)
    call(CALL_STRING)


if __name__ == '__main__':
    main()
