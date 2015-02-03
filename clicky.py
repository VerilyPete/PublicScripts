#!/usr/bin/python

"""Quick & dirty script to create screenshots at user-defined intervals for 
a user-defined length of time under OS X.
"""

import argparse
import datetime
import os
import subprocess
import time


def timer(freq, length, delay):
    """Takes user-defined freq/length and (if non-default) delay and fires click() with the
    aforementioned frequency."""

    time.sleep(float(delay))
    rep_count = 0
    while rep_count <= (int(length) / int(freq)):
        click()
        rep_count += 1
        time.sleep(float(freq))


def click():
    """Calls subprocess to run screencapture on the main screen only, dumping files in ~/Desktop/capture"""

    subprocess.call(['screencapture', '-m', os.path.join(os.path.expanduser('~'), 'Desktop', 'capture',
                    ((datetime.datetime.now().time()).isoformat()[0:8]).replace(':', '.') + '.png')])


def main(args):
    timer(args.frequency, args.length, args.delay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Takes screenshots at a user-defined frequency for a user-defined period.')
    parser.add_argument('frequency', help='Frequency of screenshots in seconds.')
    parser.add_argument('length', help='Length of time (in seconds) that screenshots will be taken at a given frequency.')
    parser.add_argument('delay', nargs='?', default=5, help='Delay before the first screenshot, in seconds. Defaults to 5 seconds.')
    args = parser.parse_args()

main(args)
