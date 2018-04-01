import os
import sys
import cgi

def getdata(form):
	if(form['title'] == "citations"):
		return getCitations(form['conference'], form['year'], form['number'])
	'''elif(title == ""):
	elif(title == ""):
	elif(title == ""):'''
	
def getCitations(conf, year, num):
	path = "../dataset/"
	#os.system('python '+ path+'PCcitation.py')
	
	file = open(path + "Role.csv", 'r', encoding='utf-8')
	pclines = file.readlines()
	file.close()
	file = open(path + 'PCCitations.csv', 'r', encoding = 'utf-8')
	lines = file.readlines()
	file.close()
	
	pcCitations = {}
	citations = []
	for line in lines:
		st = line.strip().split(',')
		pcCitations[st[0]] = int(st[2])
	for line in pclines:
		st = line.strip().split(',')
		mconf = st[2]
		myear = int(st[3])
		if(mconf == conf and myear == year):
			pid = st[0]
			if(not pid in pcCitations.keys()):
				print(pid + " not found")
			else:
				citations.append({'pid':pid, 'citations':pcCitations[pid]})
	citations = sorted(citations, key=lambda pc: pc['citations'], reverse=True)
	return citations[:num]
	#print(len(citations))
	#for item in citations:
		#print(item['pid'] + ' -> ' + str(item['citations']))
		
if __name__ == '__main__':
	getCitations('sigmod', 2018, 20)
