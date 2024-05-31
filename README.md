applemac
========

Python script for querying the apple servers for the location of wifi access points.
Most of it is from https://github.com/hubert3/iSniff-GPS.


# Prerequisites

    pip3 install -r requirements.txt

# Usage

To get the location of a wifi access point, run the script with the mac address of the access point.

    ./applemac.py 00:1C:10:30:97:00
    # This won't work, try a real mac address.

To additionally open the location in google maps, run the script with the mac address of the access point and the -m flag.

    ./applemac.py -m 00:1C:10:30:97:00


