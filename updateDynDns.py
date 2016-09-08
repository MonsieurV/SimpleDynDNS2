#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update a DynDNS2 record from a simple Python script.

First check if the current network public IP has changed from the one
registered for the specified subdomain.
If so, update the DNS A record through a provided DynDNS2 API.

The script is intended to be run from a cron table.

For IPv4 only. Ask me for an IPv6 compatible version, althouth I'm not
sure whether DynDNS2 support it.

I use it from a Raspberry Pi to a domain managed by OVH.
Anyway, should be easily adapted.

Rely on:
- Requests package for the... requests;
	http://docs.python-requests.org/en/master/
- ipify to get the current public IP.
	https://www.ipify.org/

Released under MIT License. See LICENSE file.

Created by Yoan Tournade <yoan@ytotech.com>.
"""
import requests
import socket
from parameters import PROVIDER, DOMAIN, LOGIN, PASSWORD

print('Checking the DNS A record for {0}...'.format(DOMAIN))
# Get the current public IP of the network.
publicIp = requests.get('https://api.ipify.org').text
print('The current public IP is {0}'.format(publicIp))
# Get the current IP resolved by the domain name (A record).
domainIp = [addrinfo[4][0] for addrinfo
	in socket.getaddrinfo(DOMAIN, 80) if addrinfo[0] == 2][0]
print('The A record for the domain is {0}'.format(domainIp))
if publicIp == domainIp:
	print('Same public IP than A record, all good!')
else:
	print('IP mismatch, try updating the A record through DynDNS2...')
	r = requests.get(PROVIDER + '/nic/update', auth=(LOGIN, PASSWORD),
		params={
			'system': 'dyndns', 'hostname': DOMAIN, 'myip': ip,
			'wildcard': 'OFF', 'backmx': 'NO'
		})
	print(r.status_code, r.text)
	if 'nochg' in r.text:
		print('The A record was already updated')
	elif 'good' in r.text:
		print('The A record have been updated!')
	else:
		print('Not sure what happened, but the A record hasn\'t changed :((')
