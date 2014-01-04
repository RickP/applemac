applemac
========

Python script for querying the apple servers for the location of wifi access points. 
Most of it is from https://github.com/hubert3/iSniff-GPS.


# Prerequisites

    easy_install protobuf requests

# Usage

    python applemac.py 00:1C:10:30:97:00 00:1C:10:30:97:AA [...]  
    # These won't work, try real mac addresses.
    
This will give you the location of these access points and of those arround it as a json hash.
