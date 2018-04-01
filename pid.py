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

#using proxy to ...
proxies = {
	'https': 'https://127.0.0.1:1080',
	'http': 'http://127.0.0.1:1080'
}
opener = urlreq.build_opener(urlreq.ProxyHandler(proxies))
urlreq.install_opener(opener)

def searchPID(keywords):
	hasGot = 0
	while hasGot == 0:
		domain = 'https://www.google.com.hk'
		request = urlparse.urlencode({'q': keywords})
		visit = domain + '/search?' + request
		print(visit)
		headers = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"#,
			#"Cookie":cookie
		}
		req = urlreq.Request(visit, headers=headers)
		try:
			html = urlreq.urlopen(req).read()
		except urlerr.URLError as e:
			print(e)
			continue
		except socket.timeout as e:
			print(e)
			continue
		hasGot = 1	
	soup = BeautifulSoup(html,"html.parser")
	debugfile = open('debug.html', 'w')
	debugfile.write(str(soup.encode('utf-8')))
	debugfile.close()
	for div in soup.find_all('div'):
		if(div.get('id') != u'rso'):continue
		for ddiv in div.find_all('div'):
			#if(not ddiv.get('class') or ddiv.get('class')[0] != u'_NId'):continue
			#for anss in div.find_all('div'):
				if(not ddiv.get('class') or ddiv.get('class')[0] != u'srg'):continue
				cnt = 0
				for item in ddiv.children:
					if(not item.get('class') or item.get('class')[0] != u'g'):continue
					#print(item.encode('utf-8'))
					cnt+=1
					if(cnt > 5):
						print('not found: ' + keywords)
						return ''
					for ans in item.find_all('h3'):
						if not ans.get('class'):continue
						#print(ans['class'])
						if not u'r' in ans['class']:continue
						href = ans.a['href']
						print('href: ' + href)
						key = 'scholar.google.'
						if(href.find(key) <= 0):continue
						key = 'citations?user='
						pos = href.find(key)
						#print('pos: ' + str(pos))
						if(pos >= 0):
							pos += len(key)
							return href[pos:].strip().split('&')[0]
	return ''

if __name__ == '__main__':
	filename = 'someDBresearcher'
	read = open(filename + '.txt', 'r', encoding='utf-8')
	contents = read.readlines()
	read.close()
	outlines = ''
	cnt = 0
	for line in contents:
		if(cnt % 50 == 0):
			print(cnt)
		cnt+=1
		'''if line[0] == '#':
			year = int(line[1:].strip())
			outlines += line
		elif line.strip() == '':
			outlines += line
		elif line[0] == '-':
			role = line[1:].strip()
			outlines += line
		else:'''
		if True:
			names = line.split('(')[0][2:].strip()
			keywords = names + ' google scholar '
			#if(len(names) > 1):
				#keywords += names[1].split(',')[0]
			print(keywords)
			pid = searchPID(keywords)
			print(names + ' -> ' + pid)
			#outlines += pid +'*'+ names[0] +  '\n'
			outlines += pid +'*'+ line[2:]
	outfile = open(filename + '_pid.txt', 'w', encoding='utf-8')
	outfile.write(outlines)
	outfile.close()
