#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import urllib.error as urlerr
import urllib.request as urlreq
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
pidSet = set()

#using proxy to ...
proxies = {
	'https': 'https://127.0.0.1:1080',
	'http': 'http://127.0.0.1:1080'
}
opener = urlreq.build_opener(urlreq.ProxyHandler(proxies))
urlreq.install_opener(opener)

def get_home(name):
	filename = "someDBresearcher/"+name + '.html'
	if(os.path.exists(filename)):
		return
	hasGot = 0
	while hasGot == 0:
		splits = random.choice(domain_cookie_list).split('\t')
		domain = splits[0].strip()
		cookie = splits[1].strip()
		visit = domain + '/citations?user=' + name + '&hl=en'
		headers = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
			"Cookie":cookie
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
	print(name)
	file = open(filename, 'w', encoding='utf-8')
	file.write(html.decode('utf-8'))
	file.close()
def get_homes(file):
	read = open(file, 'r', encoding='utf-8')
	lines = read.readlines()
	read.close()
	for line in lines:
		sts = line.split('*')
		if(len(sts[0])>0):
			get_home(sts[0])

def get_paper_num(name):
	scope = ''
	endNumber = 0
	for i in range(0,3000,100):
		#time.sleep(random.random())
		hasGot = 0
		while hasGot == 0:
			splits = random.choice(domain_cookie_list).split('\t')
			domain = splits[0].strip()
			cookie = splits[1].strip()
			visit = domain + '/citations?user=' + name + '&hl=en&cstart=' + str(i) + '&pagesize=100'
			headers = {
				"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
				"Cookie":cookie
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
		#print(i)
		isSet = 0
		for div in soup.find_all('div'):
			if div.get('id') == 'gsc_lwp':
				for span in div.find_all('span'):
					if span.get('id') == 'gsc_a_nn':
						scope = span.string
						isSet = 1
						#writer = open('name+'.html','w')
						#writer.write(str(soup.encode('utf-8')))
					if(isSet == 1):break
			if(isSet == 1):break
		if(isSet == 0):break
	scope = str(scope)
	token = b'\xe2\x80\x93'
	token = token.decode('utf-8')
	splits = scope.split(token)
	if(len(splits)<2):
		return 0
	scope = splits[1]
	endNumber = int(scope)
	#endNumber = int(scope[len(scope)-4:len(scope)])
	return endNumber

def update_data(name,endPage):
	for i in range(0,endPage,100):
		print(i)
		splits = random.choice(domain_cookie_list).split('\t')
		domain = splits[0].strip()
		cookie = splits[1].strip()
		visit = domain + '/citations?user=' + name + '&hl=en&cstart=' + str(i) + '&pagesize=100'
		headers = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
			"Cookie":cookie
		}
		req = urlreq.Request(visit, headers=headers)
		html = urlreq.urlopen(req).read()
		soup = BeautifulSoup(html,"html.parser")
		cont = ''
		for table in soup.find_all('table'):
			if table.get('id') == u'gsc_a_t':
				for tbody in table.find_all('tbody'):
					for tuple in tbody.find_all('tr'):	#a paper
						if not(tuple.a): break;
						title = toStr(tuple.a).replace(',',';')
						if title in dataDict:
							dataID = dataDict[title]
							line = contents[dataID]
						else:
							href = tuple.a.get('data-href')
							#print('data-href: ' + href)
							line = parse_paper_info(href)
							#time.sleep(random.random())
						#print('ok : ' + title)
						cont += line#.encode('utf-8')
						"""writer = open('citations/'+name+'.csv','a', encoding='utf-8')
						writer.write(cont)
						writer.close()
						return""" 
		try:
			writer = open('citations/'+name+'.csv','a', encoding='utf-8')
			writer.write(cont)
		except:
			error = open('error.txt','a')
			error.write(name+'\n' + str(error) + '\n')
			error.close()
		finally:
			writer.close()

def parse_paper_info(href):
	hasGot = 0
	while hasGot == 0:
		splits = random.choice(domain_cookie_list).split('\t')
		domain = splits[0].strip()
		cookie = splits[1].strip()
		url = domain + href
		headers = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
			"Cookie":cookie
		}
		req = urlreq.Request(url, headers=headers)
		try:
			html = urlreq.urlopen(req, timeout = 3)
			soup = BeautifulSoup(html.read(),"html.parser")
		except urlerr.URLError as e:
			continue
		except socket.timeout as e:
			continue
		except ssl.SSLError as e:
			continue
		hasGot = 1
	#title = author = date = publication = volume = number = pages = publisher = '*'
	title = author = description = venue = year = citedNum = '*'
	for table in soup.find_all('div'):
		if table.get('id') == u'gsc_ocd_view':
			for div in table.find_all('div'):
				if div.get('id') == u'gsc_vcd_title':
					title = div.string.replace(',',';')
				if not(div.get('class')): continue;
				if div.get('class')[0] == u'gsc_vcd_field':
					if div.string == u'Authors':
						author = toStr(div.next_sibling).replace(',',';')
					elif div.string == u'Description':
						description = toStr(div.next_sibling).replace(',',';')
					elif div.string == u'Journal':
						venue = toStr(div.next_sibling).replace(',',';')
					elif div.string == u'Conference':
						venue = toStr(div.next_sibling).replace(',',';')
					elif div.string == u'Publication date':
						year = toStr(div.next_sibling).split('/')[0].replace(',',';')
					elif div.string == u'Total citations':
						for ddiv in div.next_sibling.find_all('div'):
							st = ddiv.a.string.split()
							if(st[0] == u'Cited'):
								citedNum = st[-1].replace(',',';')
							else:
								print('error: ' + st)
							break
	line = title+','+author+','+description+','+venue+','+year+','+citedNum
	line = line.replace('\n','') + '\n'
	#print (line.encode('utf-8'))
	return line#.encode('utf-8')

def get_all_paper(name,dataNum):
	if(dataNum < 1):dataNum = 1
	endPage = int((dataNum-1)/100)*100+100
	print(dataNum)
	global dataDict, contents
	dataDict = {}
	inputFile = 'dataset/'+name+'.csv'
	if os.path.exists(inputFile):
		read = open(inputFile,'r')
		contents = read.readlines()
		read.close()
		count = len(contents)
		if count == dataNum:
			shutil.copy(inputFile,'citations/'+name+'.csv')
		else:
			id = 0
			for content in contents:
				data = content.split(',')
				dataDict[data[0]] = id
				id = id + 1
			update_data(name,endPage)
	else:
		update_data(name,endPage)
		
def toStr(node):
	ans = ''
	for st in node.stripped_strings:
		ans += st + '\n'
	return ans
	
def paperSearch(conf):
	infile = open('PC/'+conf+'_pid.txt','r')
	lines = infile.readlines()
	infile.close()
	for line in lines:
		if line[0] == '#':
			year = line[1:].strip()
		elif line.strip() == '':
			continue
		elif line[0] == '-' and not '*' in line:
			role = line[1:].strip()
		else:
			line = line.split('*')
			if(len(line[0]) > 0):
				pid = line[0]
				print(pid)
				'''if os.path.exists('citations/'+pid+'.csv'):continue
				#if(pid in pidSet):continue
				#pidSet.add(pid)
				dataNum = 3000
				dataNum = get_paper_num(pid)
				
				#if(dataNum >= 1000):
					#print('too many')
					#continue
				get_all_paper(pid, dataNum)'''
				RoleFile = open('dataset/Role.csv','a', encoding='utf-8')
				RoleFile.write(pid+','+role+','+conf+','+year+'\n')
				RoleFile.close()
		
	
	
if __name__ == '__main__':
	paperSearch('sigmod')
	paperSearch('vldb')
	paperSearch('icde')
	#get_homes('someDBresearcher_pid.txt')
	"""
	name = 'poXWlycAAAAJ' #'xcs5JDIAAAAJ'
	print(name)
	dataNum = 3000
	dataNum = get_paper_num(name)
	get_all_paper(name,dataNum)"""
