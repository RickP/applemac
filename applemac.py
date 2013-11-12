#!/usr/bin/python

import sys
import requests
import json
import BSSIDApple_pb2

def padBSSID(bssid):
	result = ''
	for e in bssid.split(':'):
		if len(e) == 1:
			e='0%s'%e
		result += e+':'
	return result.strip(':')

def ListWifiApple(wifi_list):
	apdict = {}
	for wifi in wifi_list.wifi:
		if wifi.HasField('location'):
			lat=wifi.location.latitude*pow(10,-8)
			lon=wifi.location.longitude*pow(10,-8)
			mac=padBSSID(wifi.bssid)
			apdict[mac] = (lat,lon)
		if wifi_list.HasField('unknown1'):
			print 'Unknown1 : ', '%X' % wifi_list.unknown1
		if wifi_list.HasField('unknown2'):
			print 'Unknown2 : ', '%X' % wifi_list.unknown1
		if wifi_list.HasField('APIName'):
			print 'APIName : ', wifi_list.APIName
	return apdict

def QueryBSSID(bssids):
	liste_wifi = BSSIDApple_pb2.BlockBSSIDApple()

	for bssid in bssids:
		wifi = liste_wifi.wifi.add()
		wifi.bssid = bssid

	liste_wifi.unknown1 = 0
	liste_wifi.unknown2 = 0
	liste_wifi.APIName= "com.apple.Maps"
	chaine_liste_wifi = liste_wifi.SerializeToString()
	longueur_chaine_liste_wifi = len(chaine_liste_wifi)
	headers = { 	'Content-Type':'application/x-www-form-urlencoded', 'Accept':'*/*', "Accept-Charset": "utf-8","Accept-Encoding": "gzip, deflate",\
			"Accept-Language":"en-us", 'User-Agent':'locationd (unknown version) CFNetwork/548.1.4 Darwin/11.0.0'}
	data = "\x00\x01\x00\x05"+"en_US"+"\x00\x00\x00\x09"+"5.1.9B176"+"\x00\x00\x00\x01\x00\x00\x00" + chr(longueur_chaine_liste_wifi) + chaine_liste_wifi;

	r = requests.post('https://gs-loc.apple.com/clls/wloc',headers=headers,data=data,verify=False) #the remote SSL cert CN on this server doesn't match hostname anymore

	liste_wifi = BSSIDApple_pb2.BlockBSSIDApple()
	liste_wifi.ParseFromString(r.content[10:])
	return ListWifiApple(liste_wifi)

print json.dumps(QueryBSSID(sys.argv[1:]))
