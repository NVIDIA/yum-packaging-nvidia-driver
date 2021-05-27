#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Richard Hughes <richard@hughsie.com>
# Licensed under the GNU General Public License Version or later

from __future__ import print_function
import sys
import json

def main():
    if len(sys.argv) != 2:
        print("usage: %s supported-gpus.json" % sys.argv[0])
        return 1

    # open file
    f = open(sys.argv[1])
    data = json.load(f)
    pids = []

    for chip in data['chips']:
        pid = int(chip['devid'], 16)

        if "legacybranch" not in chip.keys():
            if not pid in pids:
                pids.append(pid)

    # output
    for pid in pids:
        vid = 0x10de
        print("pci:v%08Xd%08Xsv*sd*bc*sc*i*" % (vid, pid))

if __name__ == "__main__":
    main()
