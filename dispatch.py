#!/usr/local/opt/pypy

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
                call(['scp', m, 'envy:~/music/'])
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
