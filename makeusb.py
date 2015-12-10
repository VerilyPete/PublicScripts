#!/usr/bin/env python

"""A simple utility to automate the process of converting an .iso to a .dmg
and then writing that .dmg to a USB drive via dd as a bootable volume.
Must be run with superuser permissions.
Use great care to ensure that you're writing to the proper disk, as dd will
dutifully write to the requested location, even if it's your boot volume."""

import argparse
import os
import subprocess


def main(args):
    iso_to_img(args.iso_path, args.usb_path)


def iso_to_img(iso_path, usb_path):
    """Calls hdiutil and converts the selected .iso to an .img file before
    sending the usb_path & img path to img_to_usb."""
    img_path = os.path.splitext(iso_path)[0] + '.img'
    dmg_path = img_path + '.dmg'
    subprocess.call(['hdiutil', 'convert', '-format', 'UDRW', '-o', img_path, iso_path])
    img_to_usb(usb_path, dmg_path)


def img_to_usb(usb_path, dmg_path):
    """Writes the newly created img out to the usb drive as a bootable volume."""
    disk_path = '/dev/' + usb_path
    rdisk_path = '/dev/r' + usb_path
    subprocess.call(['diskutil', 'unmountDisk', disk_path])
    subprocess.call(['dd', 'if=' + dmg_path, 'of=' + rdisk_path, 'bs=1m'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Covert a .iso to a .img and write that .img to USB.')
    parser.add_argument('iso_path', help='Path to the .iso file.')
    parser.add_argument('usb_path', help='Path to a USB drive.')
    args = parser.parse_args()

main(args)
