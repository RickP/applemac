#!/usr/bin/env python3

import argparse
import sys
import code
import requests
import webbrowser
import AppleWLC_pb2
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_argument_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("bssid", type=str, help="display the location of the bssid")
	parser.add_argument("-m", "--map", help="shows the location on google maps", action='store_true')
	return parser
	
def parse_arguments():
	parser = get_argument_parser()
	args = parser.parse_args()
	return args
	
def format_bssid(bssid):
	result = ''
	for e in bssid.split(':'):
		if len(e) == 1:
			e='0%s'%e
		result += e+':'
	return result.strip(':')

def process_result(apple_wloc):
	device_locations = {}
	for wifi_device in apple_wloc.wifi_devices:
		if wifi_device.HasField('location'):
			lat = wifi_device.location.latitude * pow(10,-8)
			lon = wifi_device.location.longitude * pow(10,-8)
			mac = format_bssid(wifi_device.bssid)
			device_locations[mac] = (lat,lon)
	return device_locations

def query_bssid(bssid):
	apple_wloc = AppleWLC_pb2.AppleWLoc()
	wifi_device = apple_wloc.wifi_devices.add()
	wifi_device.bssid = bssid
	apple_wloc.unknown_value1 = 0
	apple_wloc.return_single_result = 1
	serialized_apple_wloc = apple_wloc.SerializeToString()
	length_serialized_apple_wloc = len(serialized_apple_wloc)
	headers = {'Content-Type':'application/x-www-form-urlencoded', 'Accept':'*/*', "Accept-Charset": "utf-8","Accept-Encoding": "gzip, deflate",\
			"Accept-Language":"en-us", 'User-Agent':'locationd/1753.17 CFNetwork/711.1.12 Darwin/14.0.0'}
	data = "\x00\x01\x00\x05"+"en_US"+"\x00\x13"+"com.apple.locationd"+"\x00\x0a"+"8.1.12B411"+"\x00\x00\x00\x01\x00\x00\x00" + chr(length_serialized_apple_wloc) + serialized_apple_wloc.decode();
	r = requests.post('https://gs-loc.apple.com/clls/wloc', headers=headers, data=data, verify=False) # CN of cert on this hostname is sometimes *.ls.apple.com / ls.apple.com, so have to disable SSL verify
	apple_wloc = AppleWLC_pb2.AppleWLoc() 
	apple_wloc.ParseFromString(r.content[10:])
	return process_result(apple_wloc)

def main():
	args = parse_arguments()
	#requests.packages.urllib3.disable_warnings()
	print("Searching for location of bssid: %s" % args.bssid)
	results = query_bssid(args.bssid)
	lat = "-180.0"
	lon = "-180.0"
	if len(results) > 0:
		location = results[args.bssid.lower()]
		lat = str(location[0])
		lon = str(location[1])
	if lat != "-180.0" or lon != "-180.0":
		print("Latitude: %s" % lat)
		print("Longitude: %s" % lon)
		if args.map == True:
			url = "http://www.google.com/maps/place/" + lat + "," + lon
			webbrowser.open(url)
	else:
		print("The bssid was not found.")

if __name__ == '__main__':
    main()