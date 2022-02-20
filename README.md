applemac
========

Python script for querying the apple servers for the location of wifi access points.
Most of it is from https://github.com/hubert3/iSniff-GPS.


# Prerequisites

    pip3 install protobuf urllib2

# Usage

    python3 applemac.py 00:1C:10:30:97:00
    # This won't work, try a real mac address.

This will give you the location of the access point.
