#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
from bs4 import BeautifulSoup
import urllib.error as urlerr
import urllib.request as urlreq
import urllib.parse as urlparse
import re
import os
import shutil
import time
import random
import socket
import ssl

read = open('domain.txt','r')
tmp = read.readlines()
read.close()
domain_cookie_list = []
for content in tmp:
	domain_cookie_list.append(content)

#using proxy to ...
proxies = {
	'https': 'https://127.0.0.1:1080',
	'http': 'http://127.0.0.1:1080'
}
opener = urlreq.build_opener(urlreq.ProxyHandler(proxies))
urlreq.install_opener(opener)

debugfile = open('debug.html', 'w')

ResearcherFile = open('dataset/Researcher.csv','r',encoding='utf8')
lines = ResearcherFile.readlines()
ResearcherFile.close()
pids = set()
for line in lines:
	line = line.strip().split(',')
	if(len(line[0]) > 0):
		pids.add(line[0])

def getInfo(pid):
	hasGot = 0
	cnt = 0
	while hasGot == 0:
		splits = random.choice(domain_cookie_list).split('\t')
		domain = splits[0].strip()
		cookie = splits[1].strip()
		visit = domain + '/citations?user='+pid+'&hl=en'
		headers = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
			"Cookie":cookie
		}
		req = urlreq.Request(visit, headers=headers)
		if(cnt >= 5):#out of time
			ResearcherFile = open('dataset/Researcher.csv','a', encoding='utf-8')
			researcher = pid+',*,*\n'
			print(researcher)
			ResearcherFile.write(researcher)
			ResearcherFile.close()
			return 
		try:
			html = urlreq.urlopen(req).read()
		except urlerr.URLError as e:
			cnt += 1
			print(e)
			continue
		except socket.timeout as e:
			cnt +=1
			print(e)
			continue
		hasGot = 1	
	soup = BeautifulSoup(html,"html.parser")
	name = affiliation = '*'
	for div in soup.find_all('div'):
		if(div.get('id') == u'gsc_prf_in'):
			name = div.string.replace(',',';')
			affiliation = toStr(div.next_sibling)
			ResearcherFile = open('dataset/Researcher.csv','a', encoding='utf-8')
			researcher = pid+','+name+','+affiliation+'\n'
			print(researcher)
			ResearcherFile.write(researcher)
			pids.add(pid)
			ResearcherFile.close()
			return

def toStr(node):
	ans = ''
	for st in node.stripped_strings:
		ans += st
	return ans.replace(',',';')

def getResearchers(conf):
	infile = open('PC/'+conf+'_pid.txt','r')
	lines = infile.readlines()
	infile.close()
	for line in lines:
		if line[0] == '#':continue
		elif line.strip() == '':continue
		elif line[0] == '-':continue
		else:
			line = line.split('*')
			if(len(line[0]) > 0):
				pid = line[0]
				#print(pid)
				if(not pid in pids):
					getInfo(pid)

if __name__ == '__main__':
	getResearchers('sigmod')