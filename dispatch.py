#!/usr/local/opt/pypy

"""This file is run by a launchd user agent on my OS X laptop that watches ~/Downloads. The intent is to grab any mp3 or pdf files as they're downloaded and send them (using scp) to the appropriate folder on my linux server.
Since it'd be silly to try and scp those files if I'm not on my local network, the script begins by testing to see if it can find my router at it's (somewhat unique) IP. If it can't find the router, it assumes I'm not at home and the files will wait.  
I use pypy for this script, but regular python will work perfectly as well. Just update the shebang line if needed.
"""

import argparse
import os
import socket
import syslog
from subprocess import call


def getip(routerip):
    """Opens a socket to the first positional argument from the commandline
    and uses this connection to determine the internal NAT'd IP of the host.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((args.routerip,80))
        localip = (s.getsockname()[0])
        s.close()
        return localip
    except IOError:
        syslog.openlog('Dispatch')
        syslog.syslog(syslog.LOG_ERR, 'No route to host. Are you at home?')
        exit()



def dispatch(localip, leasedip):
    """Checks ~/Downloads for mp3s and pdfs, adding them to a list. If the
    list has anything in it, sends those files to envy if tests confirm that you're at home.
    """

    mp3 = []
    pdf = []
    path = os.path.join(os.path.expanduser('~'), 'Downloads')
    [mp3.append(os.path.join(path, x)) for x in os.listdir(path) if x.endswith('.mp3')]
    [pdf.append(os.path.join(path, x)) for x in os.listdir(path) if x.endswith('.pdf')]
    if localip == args.leasedip:
        if mp3:
            for m in mp3:
                call(['scp', m, 'envy:~/pdf/'])
                os.remove(m)
        if pdf:
            for p in pdf:
                call(['scp', p, 'pdf:~/pdf/'])
                os.remove(p)
    else:
        exit()


def main(args):
    """Calls dispatch, spawning getip and handing its output out as the first
    argument, using the commandline leasedip as the second.
    """
    dispatch(getip(args.routerip), args.leasedip)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SCP *.mp3 or *.pdf files to the appropriate user account on envy.')
    parser.add_argument('routerip', help='Specify the IP for sockets to test against. It\'s suggested that you use the internal IP of your own router.')
    parser.add_argument('leasedip', help='Specify the leased IP of the host system.')
    args = parser.parse_args()


main(args)
