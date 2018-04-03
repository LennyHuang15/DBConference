import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
from bs4 import BeautifulSoup
import urllib.error as urlerr
import urllib.request as urlreq
import urllib.parse as urlparse
import re
import os
#import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#using proxy to ...
proxies = {
	'https': 'https://127.0.0.1:1080',
	'http': 'http://127.0.0.1:1080'
}
opener = urlreq.build_opener(urlreq.ProxyHandler(proxies))
urlreq.install_opener(opener)
sys.path.append("C:/Program Files (x86)/Google/Chrome/Application")

def getLocation():
	file = open("Researcher_Loc_Linkedin.csv", 'r', encoding='utf-8')
	lines = file.readlines()
	file.close()
	driver = mdriver()
	#print(driver)
	
	outlines = 'PID, Name, Affiliation, Location\n'
	for line in lines[1:]:
		st = line.strip().split(',')
		if(st[3] == '*'):
			for info in st[2].strip().split(';'):
				#aff = st[2].split(';')[-1].strip().replace(' ', '_')
				aff = st[1] +' '+ info
				#loc = getLoc(aff)
				loc = getLocLinkin(driver, aff)
				if(len(loc) > 0):
					break
			if(len(loc)<=0):
				loc = "*"
			outlines = line[:-2]+loc+'\n'
		else:
			outlines = line
		file = open("Researcher_Loc_Linkedin_1.csv", 'a', encoding='utf-8')
		#file.write(line.strip()+','+loc.replace(",", ';')+'\n')
		file.write(outlines)
		file.close()

def getLocLinkin(driver, info):
	url = "https://www.linkedin.com/search/results/index/?keywords="\
		+info+"&origin=GLOBAL_SEARCH_HEADER"
	print(info)
	driver.get(url)
	try:
		wait = WebDriverWait(driver, 70)
		element = wait.until(EC.presence_of_element_located(\
			(By.CLASS_NAME,'search-results')))
		elements = driver.find_elements(By.CLASS_NAME, "search-result__truncate")
	except Exception as e:
		print(e)
		return ''
	if(len(elements) >= 2):
		return elements[1].text
	else:
		return ''

def mdriver():
	options = webdriver.ChromeOptions()
	options.add_argument('--profile-directory=Default')
	options.add_argument('--user-data-dir=C:/Users/Shine/AppData/Local/Google/Chrome/User Data')
	return webdriver.Chrome(chrome_options=options)

def getLoc(aff):
	hasGot = 0
	while hasGot <= 5:
		domain = 'https://en.wikipedia.org/wiki/'
		#request = urlparse.urlencode({'q': aff})
		#visit = domain + '/search?' + request
		visit = domain + aff
		print(visit)
		headers = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"#,
			#"Cookie":cookie
		}
		req = urlreq.Request(visit, headers=headers)
		try:
			html = urlreq.urlopen(req).read()
		except Exception as e:
			print(e)
			hasGot += 1
			continue
		hasGot = 10
	if(hasGot < 10):
		return '*'
	soup = BeautifulSoup(html,"html.parser")
	'''print(soup)
	debugfile = open('debug.html', 'w')
	debugfile.write(str(soup.encode('utf-8')))
	debugfile.close()'''
	for table in soup.find_all("table"):
		#print(table.get('class'))
		#print("\n")
		if(not table.get('class') or table.get('class')[0] != u"infobox"):
			continue
		for td in table.find_all("td"):
			#print(td)
			if(not td.get('class') or td.get('class')[0] != u"adr"):
				continue
			loc = ''
			for span in td.find_all("span"):
				if(not locSpan(span.get('class'))):
					continue
				if(span.string):
					loc += span.string + ';'
			return loc[:-1]
	return ''
	
def locSpan(span_class):
	if(not span_class):
		return False
	#print(span_class[0])
	if(span_class[0] == u"locality" or span_class[0] == u"state" or span_class[0] == u"country-name"):
		return True
	else: return False

if __name__ == "__main__":
	getLocation()
	